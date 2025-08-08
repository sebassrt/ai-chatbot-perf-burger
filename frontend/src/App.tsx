import React from 'react';
import { AuthProvider } from './contexts/AuthContext';
import ChatWidget from './components/ChatWidget';
import UserProfile from './components/UserProfile';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <div className="app-container">
        {/* User Profile */}
        <div className="user-profile-container">
          <UserProfile />
        </div>

        <div className="container">
          {/* Hero Section */}
          <div className="hero-section">
            <h1 className="hero-title">🍔 PerfBurger</h1>
            <p className="hero-subtitle">
              The most delicious artisanal burgers in the city
            </p>
          </div>
          
          {/* Main Content Card */}
          <div className="content-card">
            <h2 className="content-title">Welcome to PerfBurger!</h2>
            <p className="content-description">
              Discover our exquisite menu of artisanal burgers prepared 
              with premium, fresh ingredients of the highest quality.
            </p>
            
            {/* Features Grid */}
            <div className="features-grid">
              <div className="feature-card">
                <span className="feature-icon">🥩</span>
                <h3 className="feature-title">Premium Meat</h3>
                <p className="feature-description">
                  100% natural grass-fed beef, carefully selected
                </p>
              </div>
              
              <div className="feature-card">
                <span className="feature-icon">🥬</span>
                <h3 className="feature-title">Fresh Ingredients</h3>
                <p className="feature-description">
                  Organic vegetables and artisanal sauces prepared daily
                </p>
              </div>
            </div>
            
            {/* Chat Notice */}
            <div className="chat-notice">
              <div className="chat-notice-content">
                <p className="chat-notice-text">
                  💬 Have questions about our menu? 
                  <br />
                  <strong>Chat with our virtual assistant!</strong> 
                  <br />
                  Use the blue button in the bottom right corner.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Chat Widget */}
        <ChatWidget />
      </div>
    </AuthProvider>
  );
}

export default App;
