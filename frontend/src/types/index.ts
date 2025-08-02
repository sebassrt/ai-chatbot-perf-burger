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
