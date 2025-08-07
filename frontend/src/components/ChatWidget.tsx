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
    const userName = user?.first_name || 'user';
    
    const welcomeMessage: ChatMessage = {
      id: 'welcome-' + Date.now(),
      content: `Hello ${userName}! 👋 I'm the **virtual assistant** for PerfBurger 🍔

I can help you with:
• **Our menu** and prices
• **Ingredients** and nutritional information  
• **Personalized recommendations**
• **Hours** and locations

*Your conversations are automatically saved.*

*How can I help you today?*`,
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
      addBotMessage("Sorry, you need to have an active conversation to create an order. Write me something first!");
      return;
    }

    try {
      setChatState(prev => ({ ...prev, isLoading: true }));
      
      addBotMessage("🔍 Analyzing our conversation to create your order...");
      
      const response: CreateOrderResponse = await apiService.createOrder(chatState.sessionId);
      
      const orderSummary = `🎉 **Order created successfully!**

**Order ID:** ${response.order.id}
**Total:** $${response.order.total_amount.toFixed(2)}
**Status:** ${response.order.status_description || 'Received'}
**Estimated time:** ${response.order.estimated_delivery ? new Date(response.order.estimated_delivery).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }) : '30-40 minutes'}

**Ordered items:**
${response.order.items.map(item => 
  `• ${item.quantity}x ${item.name} - $${(item.price * item.quantity).toFixed(2)}${item.customizations.length > 0 ? ` (${item.customizations.join(', ')})` : ''}`
).join('\n')}

${response.unavailable_items && response.unavailable_items.length > 0 ? 
  `⚠️ **Unavailable products:** ${response.unavailable_items.join(', ')}\n\nThese products are not in our current menu. If you have any questions about our available products, please ask me!\n\n` : 
  ''
}Your order is being processed. We'll keep you informed of the progress! 🍔✨`;

      addBotMessage(orderSummary);
      
    } catch (error: any) {
      console.error('Error creating order:', error);
      addBotMessage(`❌ **Error creating order**\n\n${error.message || 'Could not create order. Please try again.'}`);
    } finally {
      setChatState(prev => ({ ...prev, isLoading: false }));
    }
  };

  const handleOrderLookup = async (orderId: string) => {
    try {
      setChatState(prev => ({ ...prev, isLoading: true }));
      
      addBotMessage(`🔍 Looking up order information for ${orderId}...`);
      
      const response: OrderLookupResponse = await apiService.lookupOrder(orderId);
      
      const orderInfo = `📋 **Order Information ${response.order.id}**

**Status:** ${response.order.status_description}
**Total:** $${response.order.total_amount.toFixed(2)}
**Created:** ${new Date(response.order.created_at).toLocaleDateString('en-US')} at ${new Date(response.order.created_at).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}
${response.order.estimated_delivery ? `**Estimated delivery:** ${new Date(response.order.estimated_delivery).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}` : ''}

**Items:**
${response.order.items.map(item => 
  `• ${item.quantity}x ${item.name} - $${(item.price * item.quantity).toFixed(2)}${item.customizations.length > 0 ? ` (${item.customizations.join(', ')})` : ''}`
).join('\n')}

${response.order.driver_name ? `**Driver:** ${response.order.driver_name}${response.order.driver_phone ? ` (${response.order.driver_phone})` : ''}` : ''}`;

      addBotMessage(orderInfo);
      
    } catch (error: any) {
      console.error('Error looking up order:', error);
      addBotMessage(`❌ **Could not find order ${orderId}**\n\n${error.message || 'Please verify that the order ID is correct and that it is your order.'}`);
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
      'want', 'order', 'buy', 'burger', 'hamburger', 
      'fries', 'drink', 'combo', 'menu'
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
    
    // Check for order lookup pattern (more flexible matching for order IDs)
    const orderLookupMatch = trimmedMessage.match(/\b(PB\d{6})\b/i);
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
      // NOTE: Disabled automatic suggestions since LLM already handles this intelligently
      // if (shouldSuggestOrderCreation(trimmedMessage)) {
      //   setTimeout(() => {
      //     const suggestionMessage: ChatMessage = {
      //       id: 'suggestion-' + Date.now(),
      //       content: `🍔 **Would you like to create an order?**\n\nI see that you mentioned some products. I can analyze our conversation and create an order for you.\n\n*Click the cart button (🛒) in the top right corner to create your order.*`,
      //       isUser: false,
      //       timestamp: new Date(),
      //     };
          
      //     setChatState(prev => ({
      //       ...prev,
      //       messages: [...prev.messages, suggestionMessage],
      //     }));
      //   }, 1000);
      // }
      
    } catch (error: any) {
      console.error('Failed to send message:', error);
      
      const errorMessage: ChatMessage = {
        id: 'error-' + Date.now(),
        content: 'Sorry, there was a problem sending your message. Please try again. 🔄',
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
    return timestamp.toLocaleTimeString('en-US', {
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
        <span className="typing-text">PerfBurger is typing...</span>
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
          aria-label="Open chat"
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
                    <p>Authentication required</p>
                  </div>
                </div>
                <div className="chat-header-actions">
                  <button
                    onClick={() => setIsOpen(false)}
                    className="chat-close-button"
                    aria-label="Close chat"
                  >
                    <X size={20} />
                  </button>
                </div>
              </div>
              
              <div className="chat-auth-message">
                <div className="auth-required-content">
                  <Bot size={48} className="auth-icon" />
                  <h4>Hello! 👋</h4>
                  <p>To use our PerfBurger virtual assistant, you need to register or log in.</p>
                  <p>This allows us to:</p>
                  <ul>
                    <li>Save your conversation history</li>
                    <li>Offer you personalized recommendations</li>
                    <li>Remember your preferences</li>
                  </ul>
                  <p className="auth-cta">
                    <strong>Use the "Sign Up" button at the top of the page to get started.</strong>
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
                  Connected • 
                  {chatState.sessionId ? ' Active session' : ' New conversation'}
                </p>
              </div>
            </div>
            <div className="chat-header-actions">
              {chatState.sessionId && chatState.messages.length > 0 && (
                <button
                  onClick={createOrder}
                  className="chat-action-button order-button"
                  title="Create order"
                  aria-label="Create order"
                  disabled={chatState.isLoading}
                >
                  <ShoppingCart size={16} />
                </button>
              )}
              {chatState.messages.length > 0 && (
                <button
                  onClick={clearChat}
                  className="chat-action-button"
                  title="Clear chat"
                  aria-label="Clear chat"
                >
                  <Trash2 size={16} />
                </button>
              )}
              <button
                onClick={() => setIsOpen(false)}
                className="chat-close-button"
                aria-label="Close chat"
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
              placeholder="Type your message..."
              className="chat-input"
              disabled={chatState.isLoading}
              rows={1}
            />
            <button
              onClick={handleSendMessage}
              disabled={!message.trim() || chatState.isLoading}
              className="chat-send-button"
              aria-label="Send message"
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
