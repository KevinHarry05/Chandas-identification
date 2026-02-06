from fastapi import APIRouter, HTTPException, Security
from pydantic import BaseModel, Field, field_validator
import re
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

from ..core.text.laghu_guru import extract_laghu_guru_pattern
from ..core.ml.predict import predict_proba_with_labels
from ..core.ml.model_loader import model, labels, MODEL_PATH, scaler
from ..core.ml.shap_xai import compute_shap_values
from ..core.ml.decision_path_xai import extract_decision_paths
from ..core.ml.enhanced_features import build_enhanced_feature_df
from ..core.db.db_utils import save_prediction
from ..core.auth import get_api_key

# Configure logger
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Chandas Analysis"])

# Confidence labeling thresholds
MIN_PATTERN_LENGTH_FOR_CONFIDENCE = 12
CONFIDENCE_LABELS = {
    "high": 0.60,
    "medium": 0.35
}


def get_confidence_label(confidence: float) -> str:
    if confidence >= CONFIDENCE_LABELS["high"]:
        return "high"
    if confidence >= CONFIDENCE_LABELS["medium"]:
        return "medium"
    return "low"


# -------------------------
# Health Check Endpoint
# -------------------------
@router.get(
    "/",
    summary="Health Check",
    description="Check if the API is running and healthy",
    response_description="Health status and version information"
)
async def health_check():
    """Health check endpoint to verify server is running"""
    return {
        "status": "healthy",
        "service": "Chandas Identifier API",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "features": {
            "pattern_extraction": True,
            "ml_prediction": True,
            "xai_insights": True,
            "database_persistence": True,
            "bulk_analysis": True
        }
    }


# -------------------------
# Request schema with validation
# -------------------------
class VerseRequest(BaseModel):
    verse: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Sanskrit verse in Devanagari script"
    )

    @field_validator('verse')
    @classmethod
    def validate_verse(cls, v: str) -> str:
        """Validate that verse contains Devanagari characters"""
        v = v.strip()
        if not v:
            raise ValueError("Verse cannot be empty or only whitespace")
        
        # Check for Devanagari characters (U+0900 to U+097F)
        if not re.search(r'[\u0900-\u097F]', v):
            raise ValueError(
                "Verse must contain Devanagari script characters. "
                "Please provide Sanskrit text in Devanagari."
            )
        
        # Remove potentially dangerous characters while keeping Sanskrit punctuation
        # Allow: Devanagari, spaces, danda (।), double danda (॥), newlines
        cleaned = re.sub(r'[^\u0900-\u097F\s।॥\n]', '', v)
        
        if len(cleaned.strip()) < 1:
            raise ValueError("Verse contains no valid Devanagari characters")
        
        return cleaned


class VersesRequest(BaseModel):
    """Request model for bulk verse analysis"""
    verses: List[str] = Field(
        ...,
        min_items=1,
        max_items=50,
        description="List of Sanskrit verses in Devanagari script",
        example=["धर्मो रक्षति रक्षितः", "सत्यं ब्रूयात् प्रियं ब्रूयात्"]
    )


class PredictionResponse(BaseModel):
    """Response model for single verse analysis"""
    verse: str = Field(description="Original input verse")
    laghu_guru_pattern: str = Field(description="Extracted L-G pattern")
    best_prediction: Dict[str, Any] = Field(description="Top prediction with confidence")
    alternatives: List[Dict[str, Any]] = Field(description="Alternative predictions")
    explainability: Optional[Dict[str, Any]] = Field(
        None,
        description="XAI data (SHAP values, decision paths, top features)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "verse": "धर्मो रक्षति रक्षितः",
                "laghu_guru_pattern": "LGLGLLGG",
                "best_prediction": {
                    "class_index": 0,
                    "chandas": "अनुष्टुभ्",
                    "confidence": 0.24
                },
                "alternatives": [
                    {"chandas": "उपेन्द्रवज्रा", "confidence": 0.21}
                ]
            }
        }


# -------------------------
# Response endpoint
# -------------------------
@router.post(
    "/analyze-verse",
    summary="Analyze Single Sanskrit Verse",
    description="""Analyzes a single Sanskrit verse and returns:
    - Laghu-Guru syllable pattern
    - Predicted chandas (meter) with confidence scores
    - Alternative predictions
    - Explainable AI insights (SHAP values, decision paths)
    
    Uses Random Forest classifier with 20 enhanced features.
    """,
    response_description="Prediction results with XAI insights"
)
def analyze_verse(
    request: VerseRequest,
    api_key: str = Security(get_api_key)
):
    verse = request.verse.strip()
    
    logger.info(f"Analyzing verse: {verse[:50]}..." if len(verse) > 50 else f"Analyzing verse: {verse}")

    if not verse:
        logger.warning("Empty verse received")
        raise HTTPException(status_code=400, detail="Verse cannot be empty")

    try:
        # 1. Extract Laghu–Guru pattern
        pattern = extract_laghu_guru_pattern(verse)
        logger.debug(f"Extracted pattern: {pattern}")

        if not isinstance(pattern, str) or len(pattern) == 0:
            logger.error("Invalid Laghu–Guru pattern extracted")
            raise ValueError("Invalid Laghu–Guru pattern")

        # 2. Predict using ML model
        predictions = predict_proba_with_labels(pattern)

        if not predictions:
            logger.error("No predictions returned from model")
            raise ValueError("No predictions returned")

        best_prediction = predictions[0]
        best_prediction["confidence_label"] = get_confidence_label(
            best_prediction["confidence"]
        )
        best_prediction["confidence_threshold_met"] = (
            best_prediction["confidence"] >= CONFIDENCE_LABELS["medium"]
        )
        logger.info(
            f"Prediction: {best_prediction['chandas']} "
            f"(confidence: {best_prediction['confidence']:.2%})"
        )
        
        # 3. Integrate XAI (SHAP values and decision paths)
        explainability = None
        if "enhanced" in str(MODEL_PATH):
            try:
                # Build feature dataframe for XAI
                feature_df = build_enhanced_feature_df(pattern)
                
                # Apply scaling if scaler is available
                if scaler is not None:
                    import pandas as pd
                    feature_df_scaled = pd.DataFrame(
                        scaler.transform(feature_df),
                        columns=feature_df.columns,
                        index=feature_df.index
                    )
                else:
                    feature_df_scaled = feature_df
                
                # Get the actual class index from model classes
                predicted_class_name = best_prediction['chandas']
                class_index = None
                for idx, label in enumerate(labels):
                    if label == predicted_class_name:
                        class_index = idx
                        break
                
                if class_index is not None:
                    # Compute SHAP values on scaled features
                    shap_values = compute_shap_values(
                        feature_df_scaled, 
                        class_index
                    )
                    
                    # Extract decision paths (top 3 trees) - use original feature names
                    decision_paths = extract_decision_paths(
                        model, 
                        feature_df_scaled, 
                        feature_df.columns.tolist()
                    )[:3]
                    
                    explainability = {
                        "shap_values": shap_values,
                        "decision_paths": decision_paths,
                        "top_features": sorted(
                            shap_values, 
                            key=lambda x: abs(x['shap_value']), 
                            reverse=True
                        )[:5]
                    }
                    logger.info(f"XAI computed: {len(shap_values)} SHAP values, {len(decision_paths)} paths")
                else:
                    logger.warning(f"Class index not found for {predicted_class_name}")
            except Exception as xai_err:
                logger.error(f"XAI computation failed: {xai_err}", exc_info=True)
        else:
            print(f"⚠️ XAI skipped - MODEL_PATH doesn't contain 'enhanced': {MODEL_PATH}")
        
        # 4. Save to database (non-blocking - log errors but don't fail)
        try:
            save_prediction(
                pattern=pattern,
                predicted_chandas=best_prediction['chandas'],
                confidence=best_prediction['confidence']
            )
            logger.debug("Prediction saved to database")
        except Exception as db_err:
            logger.warning(f"Failed to save prediction to database: {db_err}")
        
        # 5. Build response CLEANLY (NO STRING CONCATENATION)
        response = {
            "verse": verse,
            "laghu_guru_pattern": pattern,
            "best_prediction": best_prediction,
            "alternatives": predictions[1:3]
        }

        if len(pattern) < MIN_PATTERN_LENGTH_FOR_CONFIDENCE:
            response["analysis_notes"] = [
                "Short verse detected. Confidence may be lower for short patterns."
            ]
        
        if explainability:
            response["explainability"] = explainability

        return response

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post(
    "/analyze-verses",
    summary="Bulk Analyze Multiple Verses",
    description="""Analyzes multiple Sanskrit verses in a single request.
    
    Features:
    - Process 1-50 verses simultaneously
    - Partial success support (continues even if some verses fail)
    - Returns individual results for each verse
    - Includes summary statistics
    
    Useful for batch processing large collections of verses.
    """,
    response_description="Bulk analysis results with summary statistics"
)
def analyze_verses(
    request: VersesRequest,
    api_key: str = Security(get_api_key)
):
    """
    Bulk analysis endpoint - analyze multiple verses in a single request.
    Returns results for all verses, even if some fail.
    """
    logger.info(f"Bulk analysis requested: {len(request.verses)} verses")
    results = []
    
    for verse in request.verses:
        try:
            # Reuse single verse logic
            verse_request = VerseRequest(verse=verse)
            result = analyze_verse(verse_request)
            results.append({
                "success": True,
                "verse": verse,
                "analysis": result
            })
        except HTTPException as http_err:
            results.append({
                "success": False,
                "verse": verse,
                "error": http_err.detail
            })
        except Exception as e:
            results.append({
                "success": False,
                "verse": verse,
                "error": str(e)
            })
    
    # Calculate summary statistics
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    
    logger.info(
        f"Bulk analysis complete: {successful} successful, {failed} failed out of {len(results)} total"
    )
    
    return {
        "total": len(results),
        "successful": successful,
        "failed": failed,
        "results": results
    }
