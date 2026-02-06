-- Database schema for Chandas Identifier predictions
-- Run this to set up the database for prediction persistence

-- Drop table if exists (for clean reinstall)
DROP TABLE IF EXISTS chandas_predictions CASCADE;

-- Create predictions table
CREATE TABLE chandas_predictions (
    id SERIAL PRIMARY KEY,
    pattern TEXT NOT NULL,
    predicted_chandas TEXT NOT NULL,
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_predictions_created ON chandas_predictions(created_at DESC);
CREATE INDEX idx_predictions_chandas ON chandas_predictions(predicted_chandas);
CREATE INDEX idx_predictions_pattern ON chandas_predictions(pattern);

-- Optional: Create view for analytics
CREATE OR REPLACE VIEW prediction_stats AS
SELECT 
    predicted_chandas,
    COUNT(*) as total_predictions,
    AVG(confidence) as avg_confidence,
    MIN(confidence) as min_confidence,
    MAX(confidence) as max_confidence
FROM chandas_predictions
GROUP BY predicted_chandas
ORDER BY total_predictions DESC;

-- Verify table creation
SELECT 
    table_name, 
    column_name, 
    data_type 
FROM information_schema.columns 
WHERE table_name = 'chandas_predictions'
ORDER BY ordinal_position;

-- Show success message
SELECT 'Database schema created successfully!' as status;
