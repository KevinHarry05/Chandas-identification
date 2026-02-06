import '../styles/ResultDisplay.css';

function ResultDisplay({ result, onReset }) {
  const { verse, laghu_guru_pattern, best_prediction, alternatives, explainability } = result;

  const getConfidenceClass = (confidence) => {
    if (confidence >= 0.7) return 'high';
    if (confidence >= 0.4) return 'medium';
    return 'low';
  };

  return (
    <div className="result-container">
      {/* Verse Display */}
      <div className="result-card verse-card">
        <h3>📖 Your Verse</h3>
        <p className="verse-text">{verse}</p>
      </div>

      {/* Pattern Display */}
      <div className="result-card pattern-card">
        <h3>🔤 Syllable Pattern</h3>
        <div className="pattern-display">
          {laghu_guru_pattern.split('').map((char, idx) => (
            <span key={idx} className={`syllable ${char === 'L' ? 'laghu' : 'guru'}`}>
              {char}
            </span>
          ))}
        </div>
        <div className="pattern-stats">
          <div className="stat">
            <span className="stat-label">Total</span>
            <span className="stat-value">{laghu_guru_pattern.length}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Laghu (L)</span>
            <span className="stat-value">{(laghu_guru_pattern.match(/L/g) || []).length}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Guru (G)</span>
            <span className="stat-value">{(laghu_guru_pattern.match(/G/g) || []).length}</span>
          </div>
        </div>
      </div>

      {/* Main Prediction */}
      <div className="result-card prediction-card">
        <h2 className="prediction-title">
          🎭 Identified Meter: <span className="chandas-name">{best_prediction.chandas}</span>
        </h2>
        
        <div className={`confidence-display ${getConfidenceClass(best_prediction.confidence)}`}>
          <div className="confidence-label">Confidence</div>
          <div className="confidence-value">
            {(best_prediction.confidence * 100).toFixed(1)}%
          </div>
        </div>

        <div className="confidence-bar">
          <div
            className={`confidence-fill ${getConfidenceClass(best_prediction.confidence)}`}
            style={{ width: `${best_prediction.confidence * 100}%` }}
          ></div>
        </div>
      </div>

      {/* Alternative Predictions */}
      {alternatives && alternatives.length > 0 && (
        <div className="result-card alternatives-card">
          <h3>📊 Alternative Possibilities</h3>
          <div className="alternatives-list">
            {alternatives.map((alt, idx) => (
              <div key={idx} className="alternative-item">
                <div className="alt-info">
                  <span className="alt-rank">#{idx + 2}</span>
                  <span className="alt-name">{alt.chandas}</span>
                </div>
                <div className="alt-confidence">
                  {(alt.confidence * 100).toFixed(1)}%
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Explainability (SHAP) */}
      {explainability && explainability.top_features && (
        <div className="result-card explainability-card">
          <h3>🔍 Why This Prediction?</h3>
          <p className="explainability-desc">
            Top features that influenced the prediction (using SHAP analysis)
          </p>
          
          <div className="features-list">
            {explainability.top_features.map((feature, idx) => (
              <div key={idx} className="feature-item">
                <div className="feature-header">
                  <span className="feature-rank">#{idx + 1}</span>
                  <span className="feature-name">
                    {feature.feature.replace(/_/g, ' ')}
                  </span>
                </div>
                <div className="feature-details">
                  <span className="feature-value">
                    Value: {typeof feature.value === 'number' ? feature.value.toFixed(2) : feature.value}
                  </span>
                  <span className={`feature-impact ${feature.shap_value > 0 ? 'positive' : 'negative'}`}>
                    Impact: {feature.shap_value > 0 ? '+' : ''}{feature.shap_value.toFixed(3)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Reset Button */}
      <button onClick={onReset} className="reset-button">
        ← Analyze Another Verse
      </button>
    </div>
  );
}

export default ResultDisplay;
