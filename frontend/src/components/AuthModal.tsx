import React, { useState, useEffect } from 'react';
import { X, Mail, Lock, User as UserIcon, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialMode?: 'login' | 'register';
}

const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose, initialMode = 'login' }) => {
  const [mode, setMode] = useState<'login' | 'register'>(initialMode);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    firstName: '',
    lastName: '',
    confirmPassword: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const { login, register } = useAuth();

  // Update mode when initialMode changes or when modal opens
  useEffect(() => {
    if (isOpen) {
      setMode(initialMode);
    }
  }, [isOpen, initialMode]);

  if (!isOpen) return null;

  const resetForm = () => {
    setFormData({
      email: '',
      password: '',
      firstName: '',
      lastName: '',
      confirmPassword: '',
    });
    setError(null);
    setIsLoading(false);
  };

  const handleModeSwitch = (newMode: 'login' | 'register') => {
    setMode(newMode);
    resetForm();
  };

  const handleClose = () => {
    resetForm();
    onClose();
  };

  const validateForm = () => {
    if (!formData.email || !formData.password) {
      setError('Por favor completa todos los campos obligatorios');
      return false;
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setError('Please enter a valid email (example: user@email.com)');
      return false;
    }

    // Password validation
    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters long');
      return false;
    }

    if (mode === 'register') {
      if (!formData.firstName || !formData.lastName) {
        setError('Please complete your first and last name');
        return false;
      }

      if (formData.firstName.length < 2) {
        setError('First name must be at least 2 characters long');
        return false;
      }

      if (formData.lastName.length < 2) {
        setError('Last name must be at least 2 characters long');
        return false;
      }

      if (!formData.confirmPassword) {
        setError('Please confirm your password');
        return false;
      }

      if (formData.password !== formData.confirmPassword) {
        setError('Passwords do not match. Please verify they are the same.');
        return false;
      }

      // Strong password validation for registration
      if (formData.password.length < 8) {
        setError('For better security, password must be at least 8 characters long');
        return false;
      }
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!validateForm()) return;

    setIsLoading(true);

    try {
      if (mode === 'login') {
        await login(formData.email, formData.password);
      } else {
        await register(formData.email, formData.password, formData.firstName, formData.lastName);
      }
      handleClose();
    } catch (error: any) {
      console.error('Auth error:', error);
      
      // Check if it's our custom ApiError with specific messages
      if (error.message && typeof error.message === 'string' && error.error) {
        // This is our ApiError object from the API service
        setError(error.message);
      } else if (error.error && typeof error.error === 'string') {
        // Fallback to error property
        setError(error.error);
      } else if (error.message && typeof error.message === 'string') {
        // Generic axios error message
        setError(error.message);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (error) setError(null);
  };

  return (
    <div className="auth-modal-overlay" onClick={handleClose}>
      <div className="auth-modal" onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div className="auth-modal-header">
          <h2>{mode === 'login' ? 'Sign In' : 'Sign Up'}</h2>
          <button onClick={handleClose} className="auth-modal-close" aria-label="Cerrar">
            <X size={20} />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="auth-form">
          {mode === 'register' && (
            <>
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="firstName">First Name *</label>
                  <div className="input-with-icon">
                    <UserIcon size={18} />
                    <input
                      id="firstName"
                      type="text"
                      value={formData.firstName}
                      onChange={(e) => handleInputChange('firstName', e.target.value)}
                      placeholder="Your first name"
                      required
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="lastName">Last Name *</label>
                  <div className="input-with-icon">
                    <UserIcon size={18} />
                    <input
                      id="lastName"
                      type="text"
                      value={formData.lastName}
                      onChange={(e) => handleInputChange('lastName', e.target.value)}
                      placeholder="Your last name"
                      required
                    />
                  </div>
                </div>
              </div>
            </>
          )}

          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <div className="input-with-icon">
              <Mail size={18} />
              <input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                placeholder="your@email.com"
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password">Password *</label>
            <div className="input-with-icon">
              <Lock size={18} />
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                value={formData.password}
                onChange={(e) => handleInputChange('password', e.target.value)}
                placeholder="Your password"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="password-toggle"
                aria-label={showPassword ? 'Hide password' : 'Show password'}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          {mode === 'register' && (
            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password *</label>
              <div className="input-with-icon">
                <Lock size={18} />
                <input
                  id="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  value={formData.confirmPassword}
                  onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                  placeholder="Confirm your password"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="password-toggle"
                  aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
                >
                  {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>
          )}

          {error && (
            <div className="auth-error">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="auth-submit-button"
            disabled={isLoading}
          >
            {isLoading ? 'Loading...' : (mode === 'login' ? 'Sign In' : 'Sign Up')}
          </button>
        </form>

        {/* Mode Switch */}
        <div className="auth-mode-switch">
          {mode === 'login' ? (
            <p>
              Don't have an account?{' '}
              <button type="button" onClick={() => handleModeSwitch('register')}>
                Sign up here
              </button>
            </p>
          ) : (
            <p>
              Already have an account?{' '}
              <button type="button" onClick={() => handleModeSwitch('login')}>
                Sign in here
              </button>
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthModal;
