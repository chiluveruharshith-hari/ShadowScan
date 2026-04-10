from typing import Dict, List, Optional

SMS_RISK_TERMS = (
    "urgent", "click", "verify", "account",
    "suspend", "limited time", "prize",
    "password", "bank", "login"
)

SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "goo.gl"]


def compute_url_score(
    features: Dict,
    google_data: Optional[Dict],
    sms_text: Optional[str] = None
) -> Dict:

    score_float = 2.0
    reasons: List[str] = []

    # 1. Long URL
    if features.get("url_length", 0) > 75:
        score_float += 1.5
        reasons.append("URL length is unusually long")

    # 2. @ symbol
    if features.get("has_at_symbol"):
        score_float += 2.5
        reasons.append("Contains '@' symbol (masking attack)")

    # 3. Phishing keywords in URL
    keyword_count = features.get("suspicious_keyword_count", 0)
    if keyword_count > 0:
        score_float += min(2.5, keyword_count * 0.8)
        reasons.append(
            f"Phishing keywords in URL: {', '.join(features.get('suspicious_keywords', []))}"
        )

    # 4. Too many dots
    if features.get("dot_count", 0) >= 4:
        score_float += 1.5
        reasons.append("Too many subdomains")

    # 5. Shortened URL
    if features.get("is_shortened"):
        score_float += 3.0
        reasons.append("Shortened URL detected")

    # 6. SMS analysis
    if sms_text:
        sms_lower = sms_text.lower()
        matched_terms = [term for term in SMS_RISK_TERMS if term in sms_lower]

        if matched_terms:
            score_float += min(3.0, len(matched_terms) * 0.7)
            reasons.append(
                f"Suspicious SMS keywords: {', '.join(matched_terms)}"
            )

    # 7. Google Safe Browsing (STRUCTURED)
    google_matches = google_data.get("matches", []) if google_data else []

    if google_matches:
        threat_types = list(set(
            match.get("threatType", "") for match in google_matches
        ))

        for threat in threat_types:
            if threat == "MALWARE":
                score_float += 5.0
                reasons.append("Google: Malware detected")

            elif threat == "SOCIAL_ENGINEERING":
                score_float += 4.5
                reasons.append("Google: Phishing detected")

            elif threat == "UNWANTED_SOFTWARE":
                score_float += 3.5
                reasons.append("Google: Unwanted software detected")

            else:
                score_float += 3.0
                reasons.append(f"Google: {threat}")

        # Ensure Google dominates scoring
        score_float = max(score_float, 7.0)

    # FINAL SCORE
    final_score = int(min(10, round(score_float)))

    # Thresholds
    if final_score <= 3:
        risk = "LOW"
    elif final_score <= 5:
        risk = "MEDIUM"
    elif final_score <= 7:
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