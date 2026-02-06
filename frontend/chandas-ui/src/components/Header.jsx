import api from '../services/api';
import '../styles/Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo-section">
          <span className="logo-icon">🕉️</span>
          <div>
            <h1 className="logo-title">Chandas Identifier</h1>
            <p className="logo-subtitle">AI-Powered Sanskrit Meter Analysis</p>
          </div>
        </div>

        <div className="header-actions">
          <a
            href={api.getDocsUrl()}
            target="_blank"
            rel="noopener noreferrer"
            className="header-link"
          >
            📚 API Docs
          </a>
        </div>
      </div>

      <div className="header-info">
        <div className="info-badge">
          <span>🎯</span> ML Powered
        </div>
        <div className="info-badge">
          <span>🔍</span> Explainable AI
        </div>
        <div className="info-badge">
          <span>📊</span> 41 Features
        </div>
        <div className="info-badge">
          <span>⚡</span> Real-time
        </div>
      </div>
    </header>
  );
}

export default Header;
