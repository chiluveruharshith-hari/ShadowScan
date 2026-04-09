from urllib.parse import urlparse


SUSPICIOUS_KEYWORDS = ("login", "verify", "bank", "secure")


def _extract_host(url: str) -> str:
	parsed = urlparse(url)
	if parsed.netloc:
		return parsed.netloc.lower()
	return parsed.path.split("/")[0].lower()


def extract_url_features(url: str) -> dict:
	lowered_url = url.lower()
	host = _extract_host(url)

	matched_keywords = [
		keyword for keyword in SUSPICIOUS_KEYWORDS if keyword in lowered_url
	]

	return {
		"url_length": len(url),
		"has_at_symbol": "@" in url,
		"suspicious_keywords": matched_keywords,
		"suspicious_keyword_count": len(matched_keywords),
		"dot_count": host.count("."),
	}
