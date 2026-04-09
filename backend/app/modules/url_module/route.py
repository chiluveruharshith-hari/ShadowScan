from typing import List, Optional, Dict, Any

from fastapi import APIRouter
from pydantic import BaseModel

from .service import analyze_url_service


router = APIRouter(tags=["url-analysis"])


class URLAnalysisRequest(BaseModel):
	url: str
	sms_text: Optional[str] = None


class URLAnalysisResponse(BaseModel):
    score: float
    risk: str
    reasons: List[str]
    source: str
    debug: Optional[Dict[str, Any]] = None


@router.post("/analyze/url", response_model=URLAnalysisResponse)
def analyze_url(payload: URLAnalysisRequest) -> URLAnalysisResponse:
    result = analyze_url_service(url=payload.url, sms_text=payload.sms_text)
    return URLAnalysisResponse(**result)
