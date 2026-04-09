from typing import Dict, Optional

from .features import extract_url_features
from .scoring import compute_url_score
from .threat_intel import check_url_safety


def analyze_url_service(url: str, sms_text: Optional[str] = None) -> Dict:
    features = extract_url_features(url)

    # Full Google Safe Browsing response
    threat_intel_response = check_url_safety(url)

    # Pass FULL response instead of boolean flag
    score_result = compute_url_score(
        features=features,
        google_data=threat_intel_response,
        sms_text=sms_text
    )

    # Extract quick summary for output (optional but useful)
    google_matches = threat_intel_response.get("matches", []) if threat_intel_response else []

    return {
        "score": score_result["score"],
        "risk": score_result["risk"],
        "reasons": score_result["reasons"],
        "source": "url",
        "google_summary": {
            "has_threat": bool(google_matches),
            "threat_count": len(google_matches)
        },
        "debug": threat_intel_response
    }
# =========================
# WRAPPER FOR FUSION
# =========================

def analyze_url(url: str, sms_text: str = None) -> dict:
    result = analyze_url_service(url, sms_text)

    return {
        "score": result.get("score", 0.0),
        "risk_level": result.get("risk", "UNKNOWN")
    }