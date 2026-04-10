from fastapi import APIRouter
from pydantic import BaseModel
from app.modules.phone_module.service import analyze_phone, simulate_phone_data

router = APIRouter()


class PhoneInput(BaseModel):
    call_no: str
    total_calls_made: int
    unique_numbers_contacted: int
    avg_call_duration_min: float
    calls_per_hour: float
    spam_reports: int


class SimplePhoneInput(BaseModel):
    phone_number: str


@router.post("/analyze/phone")
def analyze_phone_route(data: PhoneInput):
    result = analyze_phone(data.model_dump())
    return {
        "source"      : result["source"],
        "call_no"     : result["call_no"],
        "risk_score"  : result["risk_score"],
        "risk_level"  : result["risk_level"],
        "is_scam_pred": result["is_scam_pred"],
        "scam_prob"   : result["scam_prob"],
        "score"       : result["score"],
        "flags"       : result["flags"],
    }


@router.post("/analyze/phone/simple")
def analyze_phone_simple(data: SimplePhoneInput):
    """Simple endpoint: just pass a phone number, metadata is simulated."""
    result = analyze_phone(data.model_dump())
    return {
        "source"      : result["source"],
        "call_no"     : result["call_no"],
        "risk_score"  : result["risk_score"],
        "risk_level"  : result["risk_level"],
        "is_scam_pred": result["is_scam_pred"],
        "scam_prob"   : result["scam_prob"],
        "score"       : result["score"],
        "flags"       : result["flags"],
    }