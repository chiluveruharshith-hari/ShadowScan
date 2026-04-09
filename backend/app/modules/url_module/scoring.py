from typing import Dict, List, Optional


SMS_RISK_TERMS = (
	"urgent",
	"click",
	"verify",
	"account",
	"suspend",
	"limited time",
	"prize",
	"password",
)


def compute_url_score(
    features: Dict, google_flag: bool,
) -> Dict:
    # Base score of 1 (Very Low Risk)
    score_float = 1.0
    reasons: List[str] = []

    # Analysis
    if features.get("url_length", 0) > 75:
        score_float += 1.5
        reasons.append("URL length is unusually long (> 75 chars)")

    if features.get("has_at_symbol"):
        score_float += 2.5
        reasons.append("URL contains '@' symbol (potential destination masking)")

    keyword_count = features.get("suspicious_keyword_count", 0)
    if keyword_count > 0:
        keyword_weight = min(2.0, keyword_count * 0.8)
        score_float += keyword_weight
        reasons.append(
            f"Phishing keywords detected: {', '.join(features.get('suspicious_keywords', []))}"
        )

    if features.get("dot_count", 0) >= 4:
        score_float += 1.5
        reasons.append("Excessive subdomains detected (potential phishing pattern)")

    if google_flag:
        score_float += 4.0
        reasons.append("Google Safe Browsing / Threat-intel flagged this URL")

    # Convert to 1-10 integer
    final_score = int(min(10, max(1, round(score_float))))

    # Risk categorization
    if final_score <= 4:
        risk = "LOW"
    elif final_score <= 6:
        risk = "MEDIUM"
    elif final_score <= 8:
        risk = "HIGH"
    else:
        risk = "CRITICAL"

    if not reasons:
        reasons.append("No suspicious indicators detected")

    return {
        "score": final_score,
        "risk": risk,
        "reasons": reasons,
    }
