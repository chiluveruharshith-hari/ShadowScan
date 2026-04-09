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
	features: Dict, google_flag: bool, sms_text: Optional[str] = None
) -> Dict:
	score = 0.0
	reasons: List[str] = []

	if features.get("url_length", 0) > 75:
		score += 0.15
		reasons.append("URL is unusually long")

	if features.get("has_at_symbol"):
		score += 0.25
		reasons.append("URL contains '@' which can hide real destination")

	keyword_count = features.get("suspicious_keyword_count", 0)
	if keyword_count > 0:
		keyword_weight = min(0.2, keyword_count * 0.08)
		score += keyword_weight
		reasons.append(
			f"Suspicious URL keywords detected: {', '.join(features.get('suspicious_keywords', []))}"
		)

	if features.get("dot_count", 0) >= 4:
		score += 0.15
		reasons.append("URL has many subdomains")

	if google_flag:
		score += 0.25
		reasons.append("Threat-intel rules flagged this URL")

	if sms_text:
		lowered_sms = sms_text.lower()
		sms_hits = [term for term in SMS_RISK_TERMS if term in lowered_sms]
		if sms_hits:
			score += 0.10
			reasons.append("SMS context contains urgency/phishing language")

	score = min(1.0, round(score, 3))

	if score < 0.5:
		risk = "LOW"
	elif score <= 0.8:
		risk = "MEDIUM"
	else:
		risk = "HIGH"

	if not reasons:
		reasons.append("No major phishing indicators detected")

	return {
		"score": score,
		"risk": risk,
		"reasons": reasons,
	}
