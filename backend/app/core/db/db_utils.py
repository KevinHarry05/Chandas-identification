import psycopg2
from psycopg2 import sql, pool
from .db_config import DB_CONFIG
import threading

# Initialize connection pool (lazy loading)
_pool_lock = threading.Lock()
_connection_pool = None

def get_connection_pool():
    """Get or create connection pool (thread-safe)"""
    global _connection_pool
    
    if _connection_pool is None:
        with _pool_lock:
            if _connection_pool is None:
                try:
                    _connection_pool = pool.ThreadedConnectionPool(
                        minconn=2,
                        maxconn=10,
                        **DB_CONFIG
                    )
                except psycopg2.Error as e:
                    raise RuntimeError(f"Failed to create connection pool: {e}")
    
    return _connection_pool

def get_connection():
    """Get database connection from pool with proper error handling"""
    try:
        pool_instance = get_connection_pool()
        return pool_instance.getconn()
    except psycopg2.Error as e:
        raise RuntimeError(f"Database connection failed: {e}")

def return_connection(conn):
    """Return connection to pool"""
    try:
        pool_instance = get_connection_pool()
        pool_instance.putconn(conn)
    except Exception as e:
        print(f"Warning: Failed to return connection to pool: {e}")

def save_prediction(pattern: str, predicted_chandas: str, confidence: float = None):
    """
    Save prediction to database using parameterized query (SQL injection safe).
    Uses connection pooling for performance.
    
    Args:
        pattern: Laghu-Guru pattern string
        predicted_chandas: Predicted chandas name
        confidence: Prediction confidence score (optional)
    """
    if not pattern or not predicted_chandas:
        raise ValueError("Pattern and predicted_chandas cannot be empty")
    
    conn = None
    cur = None
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Parameterized query prevents SQL injection
        query = sql.SQL(
            "INSERT INTO chandas_predictions (pattern, predicted_chandas, confidence, created_at) "
            "VALUES (%s, %s, %s, NOW())"
        )
        
        cur.execute(query, (pattern, predicted_chandas, confidence))
        conn.commit()
        
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        raise RuntimeError(f"Failed to save prediction: {e}")
    
    finally:
        if cur:
            cur.close()
        if conn:
            return_connection(conn)

def test_connection():
    """Test database connection from pool"""
    conn = None
    cur = None
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        return result is not None
    
    except psycopg2.Error as e:
        raise RuntimeError(f"Database connection test failed: {e}")
    
    finally:
        if cur:
            cur.close()
        if conn:
            return_connection(conn)
