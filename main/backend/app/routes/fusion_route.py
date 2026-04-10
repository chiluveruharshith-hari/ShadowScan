from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.modules.url_module.service import analyze_url
from app.modules.sms_module.service import analyze_sms
from app.modules.phone_module.service import analyze_phone
from app.fusion.fusion_service import calculate_final_score

router = APIRouter(prefix="/analyze", tags=["Fusion"])


class PhoneData(BaseModel):
    call_no: str = ""
    total_calls_made: int = 0
    unique_numbers_contacted: int = 0
    avg_call_duration_min: float = 0.0
    calls_per_hour: float = 0.0
    spam_reports: int = 0


class FusionInput(BaseModel):
    url: Optional[str] = None
    sms: Optional[str] = None
    phone: Optional[PhoneData] = None


@router.post("/all")
def analyze_all(data: FusionInput):
    url_score = None
    sms_score = None
    phone_score = None

    url_result = {}
    sms_result = {}
    phone_result = {}

    # --- URL Analysis ---
    if data.url and data.url.strip():
        url_result = analyze_url(data.url.strip())
        url_score = url_result.get("score", 0.0)

    # --- SMS Analysis ---
    if data.sms and data.sms.strip():
        sms_result = analyze_sms(data.sms.strip())
        sms_score = sms_result.get("score", 0.0)

    # --- Phone Analysis (pass the full dict directly to the model) ---
    if data.phone and data.phone.call_no.strip():
        phone_dict = data.phone.model_dump()
        phone_result = analyze_phone(phone_dict)
        phone_score = phone_result.get("score", 0.0)

    # --- Fusion ---
    final = calculate_final_score(url_score, sms_score, phone_score)

    # Convert scores to percentages (0-10 → 0-100)
    def to_pct(score):
        if score is None:
            return None
        return round(min(score * 10, 100), 1)

    def get_level(pct):
        if pct is None:
            return "N/A"
        if pct >= 70:
            return "HIGH"
        elif pct >= 40:
            return "MEDIUM"
        else:
            return "LOW"

    sms_pct = to_pct(sms_score)
    phone_pct = to_pct(phone_score)
    url_pct = to_pct(url_score)

    # Boost URL risk: url_pct += (100 - url_pct) / 2
    if url_pct is not None:
        url_pct = round(url_pct + (100 - url_pct) / 2, 1)

    # Weighted final risk: url*0.2 + sms*0.4 + phone*0.4
    weighted_sum = 0.0
    total_weight = 0.0
    if url_pct is not None:
        weighted_sum += url_pct * 0.2
        total_weight += 0.2
    if sms_pct is not None:
        weighted_sum += sms_pct * 0.4
        total_weight += 0.4
    if phone_pct is not None:
        weighted_sum += phone_pct * 0.4
        total_weight += 0.4

    avg_pct = round(weighted_sum / total_weight, 1) if total_weight > 0 else 0

    avg_level = get_level(avg_pct)

    return {
        # Individual raw scores (0-10)
        "url_score": url_score,
        "sms_score": sms_score,
        "phone_score": phone_score,

        # Individual percentages (0-100)
        "sms_pct": sms_pct,
        "phone_pct": phone_pct,
        "url_pct": url_pct,

        # Individual risk levels
        "sms_level": get_level(sms_pct),
        "phone_level": get_level(phone_pct),
        "url_level": get_level(url_pct),

        # Individual detailed results
        "sms_result": sms_result,
        "phone_result": phone_result,
        "url_result": url_result,

        # Aggregate
        "avg_pct": avg_pct,
        "avg_level": avg_level,

        # Fusion engine result
        **final,
    }