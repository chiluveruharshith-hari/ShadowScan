import hashlib
from app.modules.phone_module.model import call_signal_analysis


def simulate_phone_data(phone_number: str) -> dict:
    """
    Generate deterministic but realistic call metadata from a phone number.
    Uses hash-based seeding so the same number always produces the same result.
    """
    # Create a deterministic seed from the phone number
    digest = hashlib.sha256(phone_number.encode()).hexdigest()
    seed_val = int(digest[:8], 16)

    # Derive features from the hash — different bits for different features
    total_calls = 5 + (seed_val % 146)                          # 5-150
    unique_numbers = max(1, int(total_calls * (0.2 + (seed_val % 80) / 100)))
    avg_duration = round(0.1 + ((seed_val >> 8) % 140) / 10, 2) # 0.1-14.1
    calls_per_hour = round(0.1 + ((seed_val >> 16) % 300) / 10, 2)  # 0.1-30.1
    spam_reports = (seed_val >> 24) % (total_calls + 1)

    return {
        "call_no": phone_number,
        "total_calls_made": total_calls,
        "unique_numbers_contacted": unique_numbers,
        "avg_call_duration_min": avg_duration,
        "calls_per_hour": calls_per_hour,
        "spam_reports": spam_reports,
    }


def analyze_phone(data: dict) -> dict:
    """
    Analyze phone risk. Accepts either:
      - Full metadata dict (with total_calls_made, etc.)
      - Simple dict with just 'call_no' or 'phone_number'
    """
    try:
        # If only a phone number string was passed, simulate the data
        if isinstance(data, str):
            data = simulate_phone_data(data)
        elif "total_calls_made" not in data:
            phone = data.get("call_no") or data.get("phone_number", "0000000000")
            data = simulate_phone_data(phone)

        result = call_signal_analysis(data)

        return {
            "source": result.get("source", "call"),
            "call_no": result.get("call_no", "Unknown"),
            "risk_score": result.get("risk_score", 0.0),
            "risk_level": result.get("risk_level", "UNKNOWN"),
            "is_scam_pred": result.get("is_scam_pred", 0),
            "scam_prob": result.get("scam_prob", 0.0),
            "score": result.get("risk_score", 0.0),
            "flags": result.get("flags", []),
        }

    except Exception as e:
        return {
            "source": "call",
            "call_no": "Unknown",
            "risk_score": 0.0,
            "risk_level": "UNKNOWN",
            "is_scam_pred": 0,
            "scam_prob": 0.0,
            "score": 0.0,
            "flags": [],
            "error": str(e),
        }