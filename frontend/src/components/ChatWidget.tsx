import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, X, Send, User, Bot } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import ApiService from '../services/api';
import type { ChatMessage, ChatState } from '../types';

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [chatState, setChatState] = useState<ChatState>({
    messages: [],
    isLoading: false,
    isTyping: false,
    sessionId: null,
    isAuthenticated: false,
    user: null,
  });
  const [message, setMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const apiService = useRef(new ApiService());

  useEffect(() => {
    // Initialize anonymous user if not authenticated
    if (!apiService.current.isAuthenticated()) {
      initializeAnonymousUser();
    } else {
      setChatState(prev => ({ ...prev, isAuthenticated: true }));
    }
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [chatState.messages]);

  const initializeAnonymousUser = async () => {
    try {
      setChatState(prev => ({ ...prev, isLoading: true }));
      const authResponse = await apiService.current.createAnonymousUser();
      setChatState(prev => ({
        ...prev,
        isAuthenticated: true,
        user: authResponse.user,
        isLoading: false,
      }));
      
      // Send welcome message
      setTimeout(() => {
        sendWelcomeMessage();
      }, 500);
    } catch (error) {
      console.error('Failed to create anonymous user:', error);
      setChatState(prev => ({ ...prev, isLoading: false }));
    }
  };

  const sendWelcomeMessage = () => {
    const welcomeMessage: ChatMessage = {
      id: 'welcome-' + Date.now(),
      content: `¡Hola! 👋 Soy el **asistente virtual** de PerfBurger 🍔

Puedo ayudarte con:
• **Nuestro menú** y precios
• **Ingredientes** y información nutricional  
• **Recomendaciones** personalizadas
• **Horarios** y ubicaciones

*¿En qué puedo ayudarte hoy?*`,
      isUser: false,
      timestamp: new Date(),
    };
    
    setChatState(prev => ({
      ...prev,
      messages: [welcomeMessage],
    }));
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!message.trim() || chatState.isLoading) return;

    const userMessage: ChatMessage = {
      id: 'user-' + Date.now(),
      content: message.trim(),
      isUser: true,
      timestamp: new Date(),
      sessionId: chatState.sessionId || undefined,
    };

    setChatState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      isTyping: true,
    }));

    setMessage('');

    try {
      const response = await apiService.current.sendMessage(
        userMessage.content,
        chatState.sessionId || undefined
      );

      const botMessage: ChatMessage = {
        id: 'bot-' + Date.now(),
        content: response.message,
        isUser: false,
        timestamp: new Date(response.timestamp),
        sessionId: response.session_id,
      };

      setChatState(prev => ({
        ...prev,
        messages: [...prev.messages, botMessage],
        sessionId: response.session_id,
        isLoading: false,
        isTyping: false,
      }));
    } catch (error: any) {
      console.error('Failed to send message:', error);
      
      const errorMessage: ChatMessage = {
        id: 'error-' + Date.now(),
        content: 'Lo siento, hubo un problema al enviar tu mensaje. Por favor intenta de nuevo. 🔄',
        isUser: false,
        timestamp: new Date(),
      };

      setChatState(prev => ({
        ...prev,
        messages: [...prev.messages, errorMessage],
        isLoading: false,
        isTyping: false,
      }));
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (timestamp: Date) => {
    return timestamp.toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const TypingIndicator = () => (
    <div className="message-container">
      <div className="message-avatar bot">
        <Bot size={16} />
      </div>
      <div className="typing-indicator">
        <div className="typing-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <span className="typing-text">PerfBurger está escribiendo...</span>
      </div>
    </div>
  );

  return (
    <div className="chat-widget-container">
      {/* Chat Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="chat-toggle-button"
          aria-label="Abrir chat"
        >
          <MessageCircle />
        </button>
      )}

      {/* Chat Widget */}
      {isOpen && (
        <div className="chat-widget">
          {/* Header */}
          <div className="chat-header">
            <div className="chat-header-info">
              <div className="chat-avatar">
                <Bot size={20} />
              </div>
              <div className="chat-header-text">
                <h3>PerfBurger Assistant</h3>
                <p>En línea • Respuesta inmediata</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="chat-close-button"
              aria-label="Cerrar chat"
            >
              <X size={20} />
            </button>
          </div>

          {/* Messages */}
          <div className="chat-messages">
            {chatState.messages.map((msg) => (
              <div
                key={msg.id}
                className={`message-container ${msg.isUser ? 'user' : ''}`}
              >
                <div className={`message-avatar ${msg.isUser ? 'user' : 'bot'}`}>
                  {msg.isUser ? <User size={16} /> : <Bot size={16} />}
                </div>
                <div className={`message-bubble ${msg.isUser ? 'user' : 'bot'}`}>
                  {msg.isUser ? (
                    <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
                  ) : (
                    <div className="markdown-content">
                      <ReactMarkdown
                        components={{
                          p: ({ children }) => <p>{children}</p>,
                          strong: ({ children }) => <strong>{children}</strong>,
                          em: ({ children }) => <em>{children}</em>,
                          ul: ({ children }) => <ul>{children}</ul>,
                          ol: ({ children }) => <ol>{children}</ol>,
                          li: ({ children }) => <li>{children}</li>,
                          code: ({ children }) => <code>{children}</code>,
                          h3: ({ children }) => <h3>{children}</h3>,
                          h4: ({ children }) => <h4>{children}</h4>,
                          blockquote: ({ children }) => <blockquote>{children}</blockquote>,
                        }}
                      >
                        {msg.content}
                      </ReactMarkdown>
                    </div>
                  )}
                  <div className="message-time">
                    {formatTime(msg.timestamp)}
                  </div>
                </div>
              </div>
            ))}
            
            {chatState.isTyping && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="chat-input-container">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Escribe tu mensaje..."
              className="chat-input"
              disabled={chatState.isLoading}
              rows={1}
            />
            <button
              onClick={handleSendMessage}
              disabled={!message.trim() || chatState.isLoading}
              className="chat-send-button"
              aria-label="Enviar mensaje"
            >
              <Send />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;
