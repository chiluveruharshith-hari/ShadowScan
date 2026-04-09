from fastapi import APIRouter
from app.modules.url_module.service import analyze_url
from app.modules.sms_module.service import analyze_sms
from app.modules.phone_module.service import analyze_phone
from app.fusion.fusion_service import calculate_final_score

router = APIRouter(prefix="/analyze", tags=["Fusion"])


@router.post("/all")
def analyze_all(data: dict):
    url = data.get("url")
    sms = data.get("sms")
    phone = data.get("phone")

    url_score = None
    sms_score = None
    phone_score = None

    if url:
        url_result = analyze_url(url)
        url_score = url_result["score"]

    if sms:
        sms_result = analyze_sms(sms)
        sms_score = sms_result["score"]

    if phone:
        phone_result = analyze_phone(phone)
        phone_score = phone_result["score"]

    final = calculate_final_score(url_score, sms_score, phone_score)

    return {
        "url_score": url_score,
        "sms_score": sms_score,
        "phone_score": phone_score,
        **final
    }