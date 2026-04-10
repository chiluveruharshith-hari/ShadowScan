from app.modules.phone_module.model import call_signal_analysis


def analyze_phone(data: dict) -> dict:
    try:
        result = call_signal_analysis(data)

        return {
            "source": "phone",
            "call_no": data.get("call_no"),
            "risk_score": result.get("final_score", 0.0),
            "risk_level": result.get("risk_level", "UNKNOWN"),
            "is_scam_pred": result.get("is_scam", False),
            "scam_prob": result.get("scam_probability", 0.0),
            "flags": result.get("flags", [])
        }

    except Exception as e:
        return {
            "source": "phone",
            "call_no": data.get("call_no"),
            "risk_score": 0.0,
            "risk_level": "UNKNOWN",
            "is_scam_pred": False,
            "scam_prob": 0.0,
            "flags": [],
            "error": str(e)
        }