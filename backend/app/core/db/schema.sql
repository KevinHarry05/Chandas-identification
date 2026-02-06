-- ============================================================
-- Chandas Identifier Database Schema
-- ============================================================

-- Create database (run as postgres superuser)
-- CREATE DATABASE chandas_db;
-- \c chandas_db

-- Drop existing tables if recreating
DROP TABLE IF EXISTS chandas_predictions CASCADE;

-- Main predictions table
CREATE TABLE chandas_predictions (
    id SERIAL PRIMARY KEY,
    pattern VARCHAR(1000) NOT NULL,
    predicted_chandas VARCHAR(100) NOT NULL,
    confidence FLOAT CHECK (confidence >= 0 AND confidence <= 1),
    verse_text TEXT,
    source_info JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_predicted_chandas ON chandas_predictions(predicted_chandas);
CREATE INDEX idx_created_at ON chandas_predictions(created_at DESC);
CREATE INDEX idx_confidence ON chandas_predictions(confidence DESC);
CREATE INDEX idx_pattern ON chandas_predictions(pattern);

-- Optional: Full-text search on verse_text
CREATE INDEX idx_verse_text_fts ON chandas_predictions USING gin(to_tsvector('simple', verse_text));

-- Comments
COMMENT ON TABLE chandas_predictions IS 'Stores historical chandas predictions for analysis';
COMMENT ON COLUMN chandas_predictions.pattern IS 'Laghu-Guru pattern (e.g., LLGLGLLG)';
COMMENT ON COLUMN chandas_predictions.predicted_chandas IS 'Predicted Sanskrit meter name';
COMMENT ON COLUMN chandas_predictions.confidence IS 'ML model confidence score (0-1)';
COMMENT ON COLUMN chandas_predictions.verse_text IS 'Original Sanskrit verse text';
COMMENT ON COLUMN chandas_predictions.source_info IS 'Additional metadata in JSON format';

-- Sample query to check installation
SELECT 'Database schema created successfully!' AS status;

-- View for statistics
CREATE OR REPLACE VIEW chandas_statistics AS
SELECT 
    predicted_chandas,
    COUNT(*) as total_predictions,
    AVG(confidence) as avg_confidence,
    MIN(confidence) as min_confidence,
    MAX(confidence) as max_confidence
FROM chandas_predictions
GROUP BY predicted_chandas
ORDER BY total_predictions DESC;

COMMENT ON VIEW chandas_statistics IS 'Statistical summary of predictions by chandas type';
