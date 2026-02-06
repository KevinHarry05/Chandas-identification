import '../styles/Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h4>About</h4>
          <p>
            Advanced ML system for identifying Sanskrit verse meters using ensemble
            classification with 41 enhanced features and explainable AI.
          </p>
        </div>

        <div className="footer-section">
          <h4>Features</h4>
          <ul>
            <li>Pattern Extraction</li>
            <li>ML Classification</li>
            <li>SHAP Explainability</li>
            <li>10 Meter Types</li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Technology</h4>
          <ul>
            <li>Random Forest + Gradient Boosting</li>
            <li>FastAPI Backend</li>
            <li>React Frontend</li>
            <li>PostgreSQL Database</li>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <p>© 2026 Chandas Identifier | Sanskrit Meter Analysis System</p>
      </div>
    </footer>
  );
}

export default Footer;
