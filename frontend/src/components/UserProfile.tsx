import React, { useState } from 'react';
import { User, LogOut, Settings, MessageCircle } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import AuthModal from './AuthModal';

const UserProfile: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');

  const handleAuthClick = (mode: 'login' | 'register') => {
    setAuthMode(mode);
    setShowAuthModal(true);
  };

  const handleLogout = () => {
    logout();
  };

  if (!isAuthenticated) {
    return (
      <>
        <div className="user-profile">
          <div className="auth-buttons">
            <button
              onClick={() => handleAuthClick('login')}
              className="auth-button login"
            >
              <User size={16} />
              Sign In
            </button>
            <button
              onClick={() => handleAuthClick('register')}
              className="auth-button register"
            >
              <User size={16} />
              Sign Up
            </button>
          </div>
        </div>
        <AuthModal
          isOpen={showAuthModal}
          onClose={() => setShowAuthModal(false)}
          initialMode={authMode}
        />
      </>
    );
  }

  return (
    <>
      <div className="user-profile authenticated">
        <div className="user-info">
          <div className="user-avatar">
            <User size={20} />
          </div>
          <div className="user-details">
            <span className="user-name">
              {`${user?.first_name} ${user?.last_name}`}
            </span>
            <span className="user-status">
              Connected
            </span>
          </div>
        </div>
        
        <div className="user-actions">
          <button
            onClick={handleLogout}
            className="logout-button"
            title="Sign out"
          >
            <LogOut size={16} />
          </button>
        </div>
      </div>
      
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        initialMode={authMode}
      />
    </>
  );
};

export default UserProfile;
