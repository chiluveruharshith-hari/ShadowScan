from app.modules.phone_module.model import call_signal_analysis

def analyze_phone(data: dict) -> dict:
    return call_signal_analysis(data)