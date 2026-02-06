import { useState } from 'react';
import '../styles/AnalysisForm.css';

const EXAMPLE_VERSES = [
  { text: 'यो वै स परम ब्रह्म तस्य नाम सत्यम्।', label: 'Indravajra' },
  { text: 'मा गमो यातन प्रिये भरत।', label: 'Mandakranta' },
  { text: 'नमो देवाय सर्वज्ञाय प्रभवे।', label: 'Vasantatilaka' },
  { text: 'रामराज्यं नृपतेः कृतं।', label: 'Anushtubh' },
];

function AnalysisForm({ onAnalyze, loading, disabled }) {
  const [verse, setVerse] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (verse.trim()) {
      onAnalyze(verse.trim());
    }
  };

  const handleExampleClick = (exampleVerse) => {
    setVerse(exampleVerse);
  };

  return (
    <div className="analysis-form-card">
      <div className="form-header">
        <h2>📜 Analyze Sanskrit Verse</h2>
        <p>Enter a verse in Devanagari script to identify its meter (Chandas)</p>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <textarea
            value={verse}
            onChange={(e) => setVerse(e.target.value)}
            placeholder="पश्य योगं विभूतिं च मम भूतमहेश्वर।&#10;&#10;Enter your Sanskrit verse here..."
            rows={5}
            disabled={disabled || loading}
            className="verse-input"
          />
          <div className="char-count">{verse.length} characters</div>
        </div>

        <button
          type="submit"
          disabled={!verse.trim() || disabled || loading}
          className="analyze-button"
        >
          {loading ? (
            <>
              <span className="btn-spinner"></span>
              Analyzing...
            </>
          ) : (
            <>
              🔍 Analyze Verse
            </>
          )}
        </button>
      </form>

      <div className="examples-section">
        <h3>Quick Examples</h3>
        <div className="examples-grid">
          {EXAMPLE_VERSES.map((example, index) => (
            <button
              key={index}
              onClick={() => handleExampleClick(example.text)}
              disabled={disabled || loading}
              className="example-button"
            >
              <span className="example-label">{example.label}</span>
              <span className="example-text">{example.text}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default AnalysisForm;
