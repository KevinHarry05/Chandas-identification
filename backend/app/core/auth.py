# backend/app/core/auth.py
"""
Optional API Key Authentication
Enable by setting ENABLE_API_AUTH=true in .env
"""

import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# API Key configuration
ENABLE_API_AUTH = os.getenv("ENABLE_API_AUTH", "false").lower() == "true"
API_KEYS = set(os.getenv("API_KEYS", "").split(",")) if os.getenv("API_KEYS") else set()

# Add default dev key if no keys configured
if not API_KEYS and ENABLE_API_AUTH:
    API_KEYS.add("dev-key-12345")
    logger.warning("No API keys configured, using default dev key")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(api_key: Optional[str] = Security(api_key_header)):
    """
    Validate API key if authentication is enabled.
    
    Returns:
        API key if valid, None if auth disabled
        
    Raises:
        HTTPException 401 if auth enabled and key invalid
    """
    # If authentication is disabled, allow all requests
    if not ENABLE_API_AUTH:
        return None
    
    # If authentication is enabled, validate key
    if not api_key:
        logger.warning("Missing API key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Include X-API-Key header."
        )
    
    if api_key not in API_KEYS:
        logger.warning(f"Invalid API key attempted: {api_key[:8]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    logger.debug(f"Valid API key: {api_key[:8]}...")
    return api_key


def is_auth_enabled() -> bool:
    """Check if API authentication is enabled"""
    return ENABLE_API_AUTH


def get_configured_keys() -> int:
    """Get number of configured API keys"""
    return len(API_KEYS)
