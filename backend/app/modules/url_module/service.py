from typing import Dict, Optional

from .features import extract_url_features
from .scoring import compute_url_score
from .threat_intel import check_url_safety


def analyze_url_service(url: str, sms_text: Optional[str] = None) -> Dict:
	features = extract_url_features(url)
	google_flag = check_url_safety(url)
	score_result = compute_url_score(
		features=features, google_flag=google_flag, sms_text=sms_text
	)

	return {
		"score": score_result["score"],
		"risk": score_result["risk"],
		"reasons": score_result["reasons"],
		"source": "url",
	}
