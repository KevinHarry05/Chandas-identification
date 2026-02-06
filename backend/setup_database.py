#!/usr/bin/env python3
"""
Database setup script for Chandas Identifier
Automatically creates database tables if they don't exist
"""

import psycopg2
from psycopg2 import sql
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.db.db_config import DB_CONFIG


def setup_database():
    """Create database tables if they don't exist"""
    
    conn = None
    cur = None
    
    try:
        print("🔧 Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        print("�️  Dropping old table if exists...")
        cur.execute("DROP TABLE IF EXISTS chandas_predictions CASCADE;")
        
        print("📋 Creating chandas_predictions table...")
        
        # Create table with proper schema
        create_table_query = """
        CREATE TABLE chandas_predictions (
            id SERIAL PRIMARY KEY,
            pattern TEXT NOT NULL,
            predicted_chandas TEXT NOT NULL,
            confidence FLOAT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """
        
        cur.execute(create_table_query)
        
        # Create indexes
        print("📊 Creating indexes...")
        
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_predictions_created ON chandas_predictions(created_at DESC);",
            "CREATE INDEX IF NOT EXISTS idx_predictions_chandas ON chandas_predictions(predicted_chandas);",
            "CREATE INDEX IF NOT EXISTS idx_predictions_pattern ON chandas_predictions(pattern);"
        ]
        
        for index_query in indexes:
            cur.execute(index_query)
        
        # Create analytics view (safely)
        print("📈 Creating analytics view...")
        
        # Drop view if exists first
        cur.execute("DROP VIEW IF EXISTS prediction_stats CASCADE;")
        
        view_query = """
        CREATE VIEW prediction_stats AS
        SELECT 
            predicted_chandas,
            COUNT(*) as total_predictions,
            ROUND(AVG(confidence)::numeric, 3) as avg_confidence,
            ROUND(MIN(confidence)::numeric, 3) as min_confidence,
            ROUND(MAX(confidence)::numeric, 3) as max_confidence
        FROM chandas_predictions
        GROUP BY predicted_chandas
        ORDER BY total_predictions DESC;
        """
        
        cur.execute(view_query)
        
        # Commit all changes
        conn.commit()
        
        # Verify table exists
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'chandas_predictions'
            ORDER BY ordinal_position;
        """)
        
        columns = cur.fetchall()
        
        print("\n✅ Database setup complete!")
        print("\n📋 Table structure:")
        for col_name, col_type in columns:
            print(f"  - {col_name}: {col_type}")
        
        # Show existing records
        cur.execute("SELECT COUNT(*) FROM chandas_predictions;")
        count = cur.fetchone()[0]
        print(f"\n📊 Existing predictions: {count}")
        
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ Database setup failed: {e}")
        if conn:
            conn.rollback()
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("🗄️  Chandas Identifier - Database Setup")
    print("=" * 60)
    print()
    
    try:
        success = setup_database()
        
        if success:
            print("\n" + "=" * 60)
            print("🎉 Ready to store predictions!")
            print("=" * 60)
            sys.exit(0)
        else:
            print("\n" + "=" * 60)
            print("⚠️  Database setup incomplete")
            print("=" * 60)
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        sys.exit(1)
