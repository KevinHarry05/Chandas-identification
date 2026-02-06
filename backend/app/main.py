# backend/app/main.py

import logging
import sys
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from .api.routes import router

# ============================================================
# Configure Structured Logging
# ============================================================
# Ensure logs directory exists
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True, parents=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('backend/logs/chandas_api.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Chandas Identifier API",
    description="""AI-powered Sanskrit Chandas (meter) identification with Explainable AI.
    
    ## Features
    - **Pattern Extraction**: Laghu-Guru syllable pattern extraction from Devanagari text
    - **ML Prediction**: Random Forest classifier with 20 enhanced features
    - **Explainable AI**: SHAP values and decision paths for interpretability
    - **Database Persistence**: Automatic storage of predictions with connection pooling
    - **Bulk Analysis**: Process multiple verses in a single request
    
    ## Authentication
    Optional API key authentication can be enabled via X-API-Key header.
    """,
    version="2.0.0",
    contact={
        "name": "Chandas Identifier Support",
        "email": "support@chandas.example.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# CORS Configuration - Allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Request Logging Middleware
# ============================================================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all API requests with timing and status"""
    start_time = time.time()
    
    # Log request
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"from {request.client.host if request.client else 'unknown'}"
    )
    
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        
        # Log response
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"Status={response.status_code} Time={process_time:.2f}ms"
        )
        
        # Add custom headers
        response.headers["X-Process-Time"] = str(process_time)
        return response
        
    except Exception as e:
        process_time = (time.time() - start_time) * 1000
        logger.error(
            f"Error: {request.method} {request.url.path} "
            f"Time={process_time:.2f}ms Error={str(e)}",
            exc_info=True
        )
        raise

# ============================================================
# Global Exception Handler
# ============================================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch all unhandled exceptions and return proper error response"""
    logger.error(
        f"Unhandled exception: {request.method} {request.url.path}",
        exc_info=exc
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again.",
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url.path)
        }
    )

# ============================================================
# Startup/Shutdown Events
# ============================================================
@app.on_event("startup")
async def startup_event():
    """Log application startup"""
    logger.info("=" * 70)
    logger.info("Chandas Identifier API Starting...")
    logger.info(f"Version: {app.version}")
    logger.info(f"Time: {datetime.utcnow().isoformat()}")
    logger.info("=" * 70)

@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown"""
    logger.info("=" * 70)
    logger.info("Chandas Identifier API Shutting Down...")
    logger.info(f"Time: {datetime.utcnow().isoformat()}")
    logger.info("=" * 70)

app.include_router(router)
