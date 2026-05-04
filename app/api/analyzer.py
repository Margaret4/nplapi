import logging
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import AnalysisRequest, AnalysisResponse
from app.services.nlp_service import analyze_text
# Uncomment when auth is required for this endpoint
# from app.api.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_chinese_text(request: AnalysisRequest):
    """
    Analyzes a Chinese text string, returns a word list and mapping
    with grammar type, meanings, pinyin, and HSK level.
    """
    try:
        if not request.text or request.text.strip() == "":
            raise HTTPException(status_code=400, detail="Text cannot be empty.")

        logger.debug("Analyzing text: %r", request.text)
        result = analyze_text(request.text)
        logger.debug("Analysis complete, %d tokens", len(result.wordlist))
        return result
    except HTTPException:
        raise
    except RuntimeError as e:
        logger.exception("RuntimeError during text analysis")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error during text analysis")
        raise HTTPException(status_code=500, detail=f"An error occurred during analysis: {e}")
