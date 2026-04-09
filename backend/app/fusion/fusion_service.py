def calculate_final_score(url_score=None, sms_score=None, phone_score=None):

    weights = {
        "url": 0.4,
        "sms": 0.4,
        "phone": 0.2
    }

    total = 0
    total_weight = 0

    if url_score is not None:
        total += url_score * weights["url"]
        total_weight += weights["url"]

    if sms_score is not None:
        total += sms_score * weights["sms"]
        total_weight += weights["sms"]

    if phone_score is not None:
        total += phone_score * weights["phone"]
        total_weight += weights["phone"]

    if total_weight == 0:
        return {
            "final_score": 0,
            "risk_level": "UNKNOWN"
        }

    final_score = round(min(total / total_weight, 10.0), 2)

    if final_score >= 7:
        risk = "HIGH"
    elif final_score >= 4:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "final_score": final_score,
        "risk_level": risk
    }