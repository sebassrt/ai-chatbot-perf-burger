import React, { useState } from 'react';
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
      setError('Por favor ingresa un email válido (ejemplo: usuario@correo.com)');
      return false;
    }

    // Password validation
    if (formData.password.length < 6) {
      setError('La contraseña debe tener al menos 6 caracteres');
      return false;
    }

    if (mode === 'register') {
      if (!formData.firstName || !formData.lastName) {
        setError('Por favor completa tu nombre y apellido');
        return false;
      }

      if (formData.firstName.length < 2) {
        setError('El nombre debe tener al menos 2 caracteres');
        return false;
      }

      if (formData.lastName.length < 2) {
        setError('El apellido debe tener al menos 2 caracteres');
        return false;
      }

      if (!formData.confirmPassword) {
        setError('Por favor confirma tu contraseña');
        return false;
      }

      if (formData.password !== formData.confirmPassword) {
        setError('Las contraseñas no coinciden. Por favor verifica que sean iguales.');
        return false;
      }

      // Strong password validation for registration
      if (formData.password.length < 8) {
        setError('Para mayor seguridad, la contraseña debe tener al menos 8 caracteres');
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
        setError('Ha ocurrido un error inesperado. Por favor intenta de nuevo.');
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
          <h2>{mode === 'login' ? 'Iniciar Sesión' : 'Registrarse'}</h2>
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
                  <label htmlFor="firstName">Nombre *</label>
                  <div className="input-with-icon">
                    <UserIcon size={18} />
                    <input
                      id="firstName"
                      type="text"
                      value={formData.firstName}
                      onChange={(e) => handleInputChange('firstName', e.target.value)}
                      placeholder="Tu nombre"
                      required
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="lastName">Apellido *</label>
                  <div className="input-with-icon">
                    <UserIcon size={18} />
                    <input
                      id="lastName"
                      type="text"
                      value={formData.lastName}
                      onChange={(e) => handleInputChange('lastName', e.target.value)}
                      placeholder="Tu apellido"
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
                placeholder="tu@email.com"
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password">Contraseña *</label>
            <div className="input-with-icon">
              <Lock size={18} />
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                value={formData.password}
                onChange={(e) => handleInputChange('password', e.target.value)}
                placeholder="Tu contraseña"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="password-toggle"
                aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          {mode === 'register' && (
            <div className="form-group">
              <label htmlFor="confirmPassword">Confirmar Contraseña *</label>
              <div className="input-with-icon">
                <Lock size={18} />
                <input
                  id="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  value={formData.confirmPassword}
                  onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                  placeholder="Confirma tu contraseña"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="password-toggle"
                  aria-label={showConfirmPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
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
            {isLoading ? 'Cargando...' : (mode === 'login' ? 'Iniciar Sesión' : 'Registrarse')}
          </button>
        </form>

        {/* Mode Switch */}
        <div className="auth-mode-switch">
          {mode === 'login' ? (
            <p>
              ¿No tienes cuenta?{' '}
              <button type="button" onClick={() => handleModeSwitch('register')}>
                Regístrate aquí
              </button>
            </p>
          ) : (
            <p>
              ¿Ya tienes cuenta?{' '}
              <button type="button" onClick={() => handleModeSwitch('login')}>
                Inicia sesión aquí
              </button>
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthModal;
