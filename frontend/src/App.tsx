import ChatWidget from './components/ChatWidget';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <div className="container">
        {/* Hero Section */}
        <div className="hero-section">
          <h1 className="hero-title">🍔 PerfBurger</h1>
          <p className="hero-subtitle">
            Las hamburguesas artesanales más deliciosas de la ciudad
          </p>
        </div>
        
        {/* Main Content Card */}
        <div className="content-card">
          <h2 className="content-title">¡Bienvenido a PerfBurger!</h2>
          <p className="content-description">
            Descubre nuestro exquisito menú de hamburguesas artesanales preparadas 
            con ingredientes premium y frescos de la más alta calidad.
          </p>
          
          {/* Features Grid */}
          <div className="features-grid">
            <div className="feature-card">
              <span className="feature-icon">🥩</span>
              <h3 className="feature-title">Carne Premium</h3>
              <p className="feature-description">
                Carne de res grass-fed 100% natural, seleccionada cuidadosamente
              </p>
            </div>
            
            <div className="feature-card">
              <span className="feature-icon">🥬</span>
              <h3 className="feature-title">Ingredientes Frescos</h3>
              <p className="feature-description">
                Vegetales orgánicos y salsas artesanales preparadas diariamente
              </p>
            </div>
          </div>
          
          {/* Chat Notice */}
          <div className="chat-notice">
            <div className="chat-notice-content">
              <p className="chat-notice-text">
                💬 ¿Tienes preguntas sobre nuestro menú? 
                <br />
                <strong>¡Chatea con nuestro asistente virtual!</strong> 
                <br />
                Usa el botón naranja en la esquina inferior derecha.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Chat Widget */}
      <ChatWidget />
    </div>
  );
}

export default App;
