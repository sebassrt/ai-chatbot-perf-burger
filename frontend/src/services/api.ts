import axios from 'axios';
import type { AxiosInstance, AxiosResponse } from 'axios';
import type { AuthResponse, ChatResponse, ApiError, CreateOrderResponse, OrderLookupResponse } from '../types';

class ApiService {
  private static instance: ApiService;
  private api: AxiosInstance;
  private token: string | null = null;

  constructor() {
    // Automatically detect the backend URL based on environment
    const baseURL = this.getBackendUrl();
    
    this.api = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Load token from localStorage if available
    this.token = localStorage.getItem('auth_token');
    if (this.token) {
      this.setAuthHeader(this.token);
    }

    // Add response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.logout();
        }
        return Promise.reject(error);
      }
    );
  }

  // Singleton pattern
  public static getInstance(): ApiService {
    if (!ApiService.instance) {
      ApiService.instance = new ApiService();
    }
    return ApiService.instance;
  }

  private getBackendUrl(): string {
    // Check if we're in development mode
    if (import.meta.env.DEV) {
      return 'http://localhost:5000';
    }
    
    // In production, use the correct Azure backend URL
    return 'https://perfburger-chatbot-a6eph3fsavbwc5bm.westeurope-01.azurewebsites.net';
  }

  private setAuthHeader(token: string) {
    this.api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  private removeAuthHeader() {
    delete this.api.defaults.headers.common['Authorization'];
  }

  // Authentication methods
  async registerUser(email: string, password: string, firstName: string, lastName: string): Promise<AuthResponse> {
    try {
      const response: AxiosResponse<AuthResponse> = await this.api.post('/users/register', {
        email,
        password,
        first_name: firstName,
        last_name: lastName,
      });
      
      this.token = response.data.access_token;
      localStorage.setItem('auth_token', this.token);
      this.setAuthHeader(this.token);
      
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  async loginUser(email: string, password: string): Promise<AuthResponse> {
    try {
      const response: AxiosResponse<AuthResponse> = await this.api.post('/users/login', {
        email,
        password,
      });
      
      this.token = response.data.access_token;
      localStorage.setItem('auth_token', this.token);
      this.setAuthHeader(this.token);
      
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  logout() {
    this.token = null;
    localStorage.removeItem('auth_token');
    this.removeAuthHeader();
  }

  // Chat methods
  async sendMessage(message: string, sessionId?: string): Promise<ChatResponse> {
    try {
      const payload: any = { message };
      if (sessionId) {
        payload.session_id = sessionId;
      }

      const response: AxiosResponse<ChatResponse> = await this.api.post('/chat/', payload);
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  // Order methods
  async createOrder(sessionId: string): Promise<CreateOrderResponse> {
    try {
      const response: AxiosResponse<CreateOrderResponse> = await this.api.post('/orders/', {
        session_id: sessionId
      });
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  async lookupOrder(orderId: string): Promise<OrderLookupResponse> {
    try {
      const response: AxiosResponse<OrderLookupResponse> = await this.api.get(`/orders/lookup/${orderId}`);
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  async getUserOrders(): Promise<any> {
    try {
      const response = await this.api.get('/orders/');
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  // Health check
  async checkHealth(): Promise<{ status: string }> {
    try {
      const response = await this.api.get('/health');
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!this.token;
  }

  private handleError(error: any): ApiError {
    if (error.response?.data) {
      const errorData = error.response.data;
      
      // Handle specific error cases
      if (error.response.status === 401) {
        return {
          error: 'Credenciales incorrectas',
          message: 'Email o contraseña incorrectos. Por favor verifica tus datos e intenta de nuevo.',
        };
      }
      
      if (error.response.status === 409) {
        return {
          error: 'Usuario ya existe',
          message: 'Ya existe una cuenta con este email. Intenta iniciar sesión o usa otro email.',
        };
      }
      
      if (error.response.status === 400) {
        // Parse validation errors
        if (errorData.error && typeof errorData.error === 'string') {
          if (errorData.error.toLowerCase().includes('email')) {
            return {
              error: 'Email inválido',
              message: 'Por favor ingresa un email válido.',
            };
          }
          if (errorData.error.toLowerCase().includes('password')) {
            return {
              error: 'Contraseña inválida',
              message: 'La contraseña debe tener al menos 6 caracteres.',
            };
          }
        }
        
        return {
          error: 'Datos inválidos',
          message: errorData.message || 'Por favor verifica que todos los campos estén correctos.',
        };
      }
      
      if (error.response.status === 422) {
        return {
          error: 'Datos de validación incorrectos',
          message: 'Por favor verifica que todos los campos estén completos y sean válidos.',
        };
      }
      
      if (error.response.status === 500) {
        return {
          error: 'Error del servidor',
          message: 'Ocurrió un problema en el servidor. Por favor intenta de nuevo más tarde.',
        };
      }
      
      // Return the original error message if available
      return {
        error: errorData.error || 'Error',
        message: errorData.message || 'Ha ocurrido un error inesperado.',
      };
    }
    
    // Network errors
    if (error.code === 'ECONNREFUSED' || error.message.includes('Network Error')) {
      return {
        error: 'Error de conexión',
        message: 'No se pudo conectar con el servidor. Verifica tu conexión a internet.',
      };
    }
    
    return {
      error: 'Error de red',
      message: error.message || 'No se pudo completar la operación. Verifica tu conexión.',
    };
  }
}

// Export singleton instance
export default ApiService.getInstance();
