from urllib.parse import urlparse
import re

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "bank", "account", "secure",
    "update", "free", "offer", "win", "prize", "password"
]

SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "goo.gl"]


def extract_url_features(url: str) -> dict:
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    features = {}

    features["url_length"] = len(url)
    features["has_at_symbol"] = "@" in url
    features["dot_count"] = url.count(".")
    features["domain"] = domain

    # keyword detection
    found_keywords = [kw for kw in SUSPICIOUS_KEYWORDS if kw in url.lower()]
    features["suspicious_keywords"] = found_keywords
    features["suspicious_keyword_count"] = len(found_keywords)

    # shortened URL detection
    features["is_shortened"] = any(short in domain for short in SHORTENERS)

    return features