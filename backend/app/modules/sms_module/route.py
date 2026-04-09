from fastapi import APIRouter
from .models.common_models import SMSRequest
from .service import analyze_sms, final_sms_risk_analysis

router = APIRouter()

@router.post("/sms/analyze")
def analyze(request: SMSRequest):
    return analyze_sms(request.text)