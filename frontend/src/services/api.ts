import axios from 'axios';
import type { AxiosInstance, AxiosResponse } from 'axios';
import type { AuthResponse, ChatResponse, ApiError } from '../types';

class ApiService {
  private api: AxiosInstance;
  private token: string | null = null;

  constructor(baseURL: string = 'http://localhost:5000') {
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

  // Health check
  async checkHealth(): Promise<{ status: string }> {
    try {
      const response = await this.api.get('/health');
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  // Auto-register anonymous user for demo purposes
  async createAnonymousUser(): Promise<AuthResponse> {
    const randomId = Math.random().toString(36).substring(2, 15);
    const email = `demo-${randomId}@perfburger.com`;
    const password = 'demo123';
    
    return this.registerUser(email, password, 'Demo', 'User');
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!this.token;
  }

  private handleError(error: any): ApiError {
    if (error.response?.data) {
      return error.response.data;
    }
    return {
      error: 'Network error',
      message: error.message || 'Unable to connect to server',
    };
  }
}

export default ApiService;
