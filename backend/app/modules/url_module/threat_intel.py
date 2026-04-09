from urllib.parse import urlparse


SUSPICIOUS_KEYWORDS = ("login", "verify", "bank", "secure", "update", "password")
SHORTENER_DOMAINS = ("bit.ly", "tinyurl.com", "t.co", "goo.gl")


def _extract_host(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc:
        return parsed.netloc.lower()

    # Handles URLs without a scheme (for example: example.com/login)
    return parsed.path.split("/")[0].lower()


def check_url_safety(url: str) -> bool:
    """Return True when the URL matches suspicious patterns."""
    lowered_url = url.lower()
    host = _extract_host(url)

    rules_triggered = 0

    if "@" in lowered_url:
        rules_triggered += 1

    if any(keyword in lowered_url for keyword in SUSPICIOUS_KEYWORDS):
        rules_triggered += 1

    if any(shortener in host for shortener in SHORTENER_DOMAINS):
        rules_triggered += 1

    if host.count(".") >= 4:
        rules_triggered += 1

    if "xn--" in host:
        rules_triggered += 1

    has_ip_like_host = host.replace(".", "").isdigit() and host.count(".") == 3
    if has_ip_like_host:
        rules_triggered += 1

    return rules_triggered >= 2
