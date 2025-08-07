// API Types
export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface AuthResponse {
  access_token: string;
  user: User;
}

export interface Message {
  id: string;
  message: string;
  session_id: string;
  timestamp: string;
  isUser: boolean;
}

export interface ChatResponse {
  message: string;
  session_id: string;
  timestamp: string;
}

export interface ApiError {
  error: string;
  message?: string;
}

// Chat Widget Types
export interface ChatWidgetProps {
  isOpen: boolean;
  onToggle: () => void;
  apiUrl?: string;
}

export interface ChatMessage {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  sessionId?: string;
}

export interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  isTyping: boolean;
  sessionId: string | null;
  isAuthenticated: boolean;
  user: User | null;
}

// Order Types
export interface OrderItem {
  name: string;
  price: number;
  quantity: number;
  customizations: string[];
  category: string;
}

export interface Order {
  id: string;
  status: string;
  items: OrderItem[];
  total_amount: number;
  delivery_address: string;
  estimated_delivery: string | null;
  actual_delivery: string | null;
  created_at: string;
  driver_name?: string;
  driver_phone?: string;
  status_description?: string;
  chat_friendly_summary?: string;
}

export interface CreateOrderResponse {
  message: string;
  order: Order;
  analysis_method?: string;
  llm_confidence?: number;
  unavailable_items?: string[];
  llm_reasoning?: string;
}

export interface OrderLookupResponse {
  order: Order;
}
