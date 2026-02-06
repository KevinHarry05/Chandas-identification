import { useState, useEffect } from 'react';
import api from './services/api';
import AnalysisForm from './components/AnalysisForm';
import ResultDisplay from './components/ResultDisplay';
import Header from './components/Header';
import Footer from './components/Footer';
import './styles/App.css';

function App() {
  const [isBackendHealthy, setIsBackendHealthy] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    try {
      await api.healthCheck();
      setIsBackendHealthy(true);
    } catch {
      setIsBackendHealthy(false);
    }
  };

  const handleAnalyze = async (verse) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await api.analyzeVerse(verse);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="app">
      <Header />
      
      <main className="main-content">
        <div className="container">
          {/* Status Banner */}
          <div className={`status-banner ${isBackendHealthy ? 'online' : 'offline'}`}>
            <div className="status-indicator"></div>
            <span>
              {isBackendHealthy ? 'Backend Connected' : 'Backend Offline'}
            </span>
            {!isBackendHealthy && (
              <button onClick={checkBackendHealth} className="retry-btn">
                Retry
              </button>
            )}
          </div>

          {/* Analysis Form */}
          <AnalysisForm
            onAnalyze={handleAnalyze}
            loading={loading}
            disabled={!isBackendHealthy}
          />

          {/* Error Display */}
          {error && (
            <div className="error-message">
              <div className="error-icon">⚠️</div>
              <div>
                <strong>Error:</strong> {error}
                {!isBackendHealthy && (
                  <p className="error-hint">
                    Make sure the backend is running on http://localhost:8000
                  </p>
                )}
              </div>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="loading-container">
              <div className="spinner"></div>
              <p>Analyzing verse...</p>
            </div>
          )}

          {/* Result Display */}
          {result && !loading && (
            <ResultDisplay result={result} onReset={handleReset} />
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;
