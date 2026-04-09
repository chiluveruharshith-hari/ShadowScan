from fastapi import APIRouter
from .models.common_models import SMSRequest
from .service import final_sms_risk_analysis

router = APIRouter()

@router.post("/sms/analyze")
def analyze_sms(request: SMSRequest):
    result = final_sms_risk_analysis(request.text)
    return result