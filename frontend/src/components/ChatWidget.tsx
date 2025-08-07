import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, X, Send, User, Bot, Trash2, ShoppingCart } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { useAuth } from '../contexts/AuthContext';
import apiService from '../services/api';
import type { ChatMessage, ChatState, CreateOrderResponse, OrderLookupResponse } from '../types';

const ChatWidget: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
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

  useEffect(() => {
    // Update chat state when auth state changes
    setChatState(prev => ({
      ...prev,
      isAuthenticated,
      user,
    }));

    // Send welcome message when user becomes authenticated
    if (isAuthenticated && chatState.messages.length === 0) {
      setTimeout(() => {
        sendWelcomeMessage();
      }, 500);
    }
  }, [isAuthenticated, user]);

  useEffect(() => {
    scrollToBottom();
  }, [chatState.messages]);

  const sendWelcomeMessage = () => {
    const userName = user?.first_name || 'usuario';
    
    const welcomeMessage: ChatMessage = {
      id: 'welcome-' + Date.now(),
      content: `¡Hola ${userName}! 👋 Soy el **asistente virtual** de PerfBurger 🍔

Puedo ayudarte con:
• **Nuestro menú** y precios
• **Ingredientes** y información nutricional  
• **Recomendaciones** personalizadas
• **Horarios** y ubicaciones

*Tus conversaciones se guardan automáticamente.*

*¿En qué puedo ayudarte hoy?*`,
      isUser: false,
      timestamp: new Date(),
    };
    
    setChatState(prev => ({
      ...prev,
      messages: [welcomeMessage],
    }));
  };

  const clearChat = () => {
    // Completely reset: clear messages AND session
    setChatState(prev => ({
      ...prev,
      messages: [],
      sessionId: null,
    }));
    setTimeout(() => {
      sendWelcomeMessage();
    }, 100);
  };

  const createOrder = async () => {
    if (!chatState.sessionId) {
      addBotMessage("Lo siento, necesitas tener una conversación activa para crear un pedido. ¡Escríbeme algo primero!");
      return;
    }

    try {
      setChatState(prev => ({ ...prev, isLoading: true }));
      
      addBotMessage("🔍 Analizando nuestra conversación para crear tu pedido...");
      
      const response: CreateOrderResponse = await apiService.createOrder(chatState.sessionId);
      
      const orderSummary = `🎉 **¡Pedido creado exitosamente!**

**ID del Pedido:** ${response.order.id}
**Total:** $${response.order.total_amount.toFixed(2)}
**Estado:** ${response.order.status_description || 'Recibido'}
**Tiempo estimado:** ${response.order.estimated_delivery ? new Date(response.order.estimated_delivery).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }) : '30-40 minutos'}

**Artículos pedidos:**
${response.order.items.map(item => 
  `• ${item.quantity}x ${item.name} - $${(item.price * item.quantity).toFixed(2)}${item.customizations.length > 0 ? ` (${item.customizations.join(', ')})` : ''}`
).join('\n')}

Tu pedido está siendo procesado. ¡Te mantendremos informado del progreso! 🍔✨`;

      addBotMessage(orderSummary);
      
    } catch (error: any) {
      console.error('Error creating order:', error);
      addBotMessage(`❌ **Error al crear el pedido**\n\n${error.message || 'No se pudo crear el pedido. Por favor intenta de nuevo.'}`);
    } finally {
      setChatState(prev => ({ ...prev, isLoading: false }));
    }
  };

  const handleOrderLookup = async (orderId: string) => {
    try {
      setChatState(prev => ({ ...prev, isLoading: true }));
      
      addBotMessage(`🔍 Buscando información del pedido ${orderId}...`);
      
      const response: OrderLookupResponse = await apiService.lookupOrder(orderId);
      
      const orderInfo = `📋 **Información del Pedido ${response.order.id}**

**Estado:** ${response.order.status_description}
**Total:** $${response.order.total_amount.toFixed(2)}
**Creado:** ${new Date(response.order.created_at).toLocaleDateString('es-ES')} a las ${new Date(response.order.created_at).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}
${response.order.estimated_delivery ? `**Entrega estimada:** ${new Date(response.order.estimated_delivery).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}` : ''}

**Artículos:**
${response.order.items.map(item => 
  `• ${item.quantity}x ${item.name} - $${(item.price * item.quantity).toFixed(2)}${item.customizations.length > 0 ? ` (${item.customizations.join(', ')})` : ''}`
).join('\n')}

${response.order.driver_name ? `**Conductor:** ${response.order.driver_name}${response.order.driver_phone ? ` (${response.order.driver_phone})` : ''}` : ''}`;

      addBotMessage(orderInfo);
      
    } catch (error: any) {
      console.error('Error looking up order:', error);
      addBotMessage(`❌ **No se pudo encontrar el pedido ${orderId}**\n\n${error.message || 'Verifica que el ID del pedido sea correcto y que sea tu pedido.'}`);
    } finally {
      setChatState(prev => ({ ...prev, isLoading: false }));
    }
  };

  const addBotMessage = (content: string) => {
    const botMessage: ChatMessage = {
      id: 'bot-' + Date.now(),
      content,
      isUser: false,
      timestamp: new Date(),
    };
    
    setChatState(prev => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));
  };

  const shouldSuggestOrderCreation = (message: string): boolean => {
    const orderKeywords = [
      'quiero', 'ordenar', 'pedir', 'comprar', 'burger', 'hamburguesa', 
      'papas', 'fries', 'bebida', 'drink', 'combo', 'menú'
    ];
    
    const messageLower = message.toLowerCase();
    return orderKeywords.some(keyword => messageLower.includes(keyword));
  };



  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!message.trim() || chatState.isLoading) return;

    const trimmedMessage = message.trim();
    
    // Check for order lookup pattern (e.g., "check order PB123456")
    const orderLookupMatch = trimmedMessage.match(/(?:check|ver|consultar|buscar)\s+(?:order|pedido|orden)\s+(PB\d{6})/i);
    if (orderLookupMatch) {
      const orderId = orderLookupMatch[1];
      
      const userMessage: ChatMessage = {
        id: 'user-' + Date.now(),
        content: trimmedMessage,
        isUser: true,
        timestamp: new Date(),
        sessionId: chatState.sessionId || undefined,
      };

      setChatState(prev => ({
        ...prev,
        messages: [...prev.messages, userMessage],
      }));

      setMessage('');
      await handleOrderLookup(orderId);
      return;
    }

    const userMessage: ChatMessage = {
      id: 'user-' + Date.now(),
      content: trimmedMessage,
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
      const response = await apiService.sendMessage(
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

      // Check if we should suggest order creation
      if (shouldSuggestOrderCreation(trimmedMessage)) {
        setTimeout(() => {
          const suggestionMessage: ChatMessage = {
            id: 'suggestion-' + Date.now(),
            content: `🍔 **¿Te gustaría crear un pedido?**\n\nVeo que mencionaste algunos productos. Puedo analizar nuestra conversación y crear un pedido para ti.\n\n*Haz clic en el botón de carrito (🛒) en la esquina superior derecha para crear tu pedido.*`,
            isUser: false,
            timestamp: new Date(),
          };
          
          setChatState(prev => ({
            ...prev,
            messages: [...prev.messages, suggestionMessage],
          }));
        }, 1000);
      }
      
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
          {!isAuthenticated ? (
            /* Unauthenticated State */
            <div className="chat-auth-required">
              <div className="chat-header">
                <div className="chat-header-info">
                  <div className="chat-avatar">
                    <Bot size={20} />
                  </div>
                  <div className="chat-header-text">
                    <h3>PerfBurger Assistant</h3>
                    <p>Autenticación requerida</p>
                  </div>
                </div>
                <div className="chat-header-actions">
                  <button
                    onClick={() => setIsOpen(false)}
                    className="chat-close-button"
                    aria-label="Cerrar chat"
                  >
                    <X size={20} />
                  </button>
                </div>
              </div>
              
              <div className="chat-auth-message">
                <div className="auth-required-content">
                  <Bot size={48} className="auth-icon" />
                  <h4>¡Hola! 👋</h4>
                  <p>Para usar nuestro asistente virtual de PerfBurger, necesitas registrarte o iniciar sesión.</p>
                  <p>Esto nos permite:</p>
                  <ul>
                    <li>Guardar tu historial de conversaciones</li>
                    <li>Ofrecerte recomendaciones personalizadas</li>
                    <li>Recordar tus preferencias</li>
                  </ul>
                  <p className="auth-cta">
                    <strong>Usa el botón "Registrarse" en la parte superior de la página para comenzar.</strong>
                  </p>
                </div>
              </div>
            </div>
          ) : (
            /* Authenticated State */
            <>
              {/* Header */}
              <div className="chat-header">
            <div className="chat-header-info">
              <div className="chat-avatar">
                <Bot size={20} />
              </div>
              <div className="chat-header-text">
                <h3>PerfBurger Assistant</h3>
                <p>
                  Conectado • 
                  {chatState.sessionId ? ' Sesión activa' : ' Nueva conversación'}
                </p>
              </div>
            </div>
            <div className="chat-header-actions">
              {chatState.sessionId && chatState.messages.length > 0 && (
                <button
                  onClick={createOrder}
                  className="chat-action-button order-button"
                  title="Crear pedido"
                  aria-label="Crear pedido"
                  disabled={chatState.isLoading}
                >
                  <ShoppingCart size={16} />
                </button>
              )}
              {chatState.messages.length > 0 && (
                <button
                  onClick={clearChat}
                  className="chat-action-button"
                  title="Limpiar chat"
                  aria-label="Limpiar chat"
                >
                  <Trash2 size={16} />
                </button>
              )}
              <button
                onClick={() => setIsOpen(false)}
                className="chat-close-button"
                aria-label="Cerrar chat"
              >
                <X size={20} />
              </button>
            </div>
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
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default ChatWidget;
