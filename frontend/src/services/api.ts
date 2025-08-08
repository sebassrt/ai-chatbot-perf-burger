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
          error: 'Invalid credentials',
          message: 'Incorrect email or password. Please verify your information and try again.',
        };
      }
      
      if (error.response.status === 409) {
        return {
          error: 'User already exists',
          message: 'An account with this email already exists. Try logging in or use a different email.',
        };
      }
      
      if (error.response.status === 400) {
        // Parse validation errors
        if (errorData.error && typeof errorData.error === 'string') {
          if (errorData.error.toLowerCase().includes('email')) {
            return {
              error: 'Invalid email',
              message: 'Please enter a valid email address.',
            };
          }
          if (errorData.error.toLowerCase().includes('password')) {
            return {
              error: 'Invalid password',
              message: 'Password must be at least 6 characters long.',
            };
          }
        }
        
        return {
          error: 'Invalid data',
          message: errorData.message || 'Please verify that all fields are correct.',
        };
      }
      
      if (error.response.status === 422) {
        return {
          error: 'Validation error',
          message: 'Please verify that all fields are complete and valid.',
        };
      }
      
      if (error.response.status === 500) {
        return {
          error: 'Server error',
          message: 'A server error occurred. Please try again later.',
        };
      }
      
      // Return the original error message if available
      return {
        error: errorData.error || 'Error',
        message: errorData.message || 'An unexpected error occurred.',
      };
    }
    
    // Network errors
    if (error.code === 'ECONNREFUSED' || error.message.includes('Network Error')) {
      return {
        error: 'Connection error',
        message: 'Could not connect to the server. Please check your internet connection.',
      };
    }
    
    return {
      error: 'Network error',
      message: error.message || 'Could not complete the operation. Please check your connection.',
    };
  }
}

// Export singleton instance
export default ApiService.getInstance();
