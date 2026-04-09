from app.modules.phone_module.model import call_signal_analysis


def analyze_phone(data: dict) -> dict:
    try:
        result = call_signal_analysis(data)

        return {
            "score": result.get("final_score", 0.0),
            "risk_level": result.get("risk_level", "UNKNOWN")
        }

    except Exception as e:
        return {
            "score": 0.0,
            "risk_level": "UNKNOWN",
            "error": str(e)
        }