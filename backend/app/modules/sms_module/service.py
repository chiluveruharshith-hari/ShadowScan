import pickle
import re
from pathlib import Path
import re
from app.modules.url_module.service import analyze_url  # adjust import if needed

URL_REGEX = r'(https?://[^\s]+)'

# =========================
# MODEL LOADING
# =========================

MODEL_DIR = Path(__file__).parent / "models"

def load_pickle(path):
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")
    with open(path, "rb") as f:
        return pickle.load(f)

# Load model + vectorizer safely
model = load_pickle(MODEL_DIR / "sms_model.pkl")
vectorizer = load_pickle(MODEL_DIR / "vectorizer.pkl")


# =========================
# KEYWORDS
# =========================

SCAM_KEYWORDS = [
    'bank', 'account', 'verify', 'update', 'blocked',
    'urgent', 'click', 'link', 'otp', 'password'
]

PHISHING_WORDS = [
    'click here', 'login', 'verify now', 'update details'
]


# =========================
# ML PREDICTION (FIXED)
# =========================

def ml_predict(text: str) -> float:
    try:
        vec = vectorizer.transform([text])

        # If model supports probability
        if hasattr(model, "predict_proba"):
            return model.predict_proba(vec)[0][1]

        # Fallback if no probability
        prediction = model.predict(vec)[0]
        return float(prediction)

    except Exception as e:
        print("ML ERROR:", e)
        return 0.0


# =========================
# FEATURE EXTRACTION
# =========================

def extract_sms_features(text: str) -> dict:
    text_lower = text.lower()

    return {
        'has_url': int(bool(re.search(r'http[s]?://', text_lower))),
        'has_phone': int(bool(re.search(r'\d{10}', text_lower))),
        'keyword_count': sum(1 for w in SCAM_KEYWORDS if w in text_lower),
        'phishing_flag': int(any(w in text_lower for w in PHISHING_WORDS)),
        'urgency_flag': int('urgent' in text_lower or 'immediately' in text_lower)
    }


# =========================
# RULE SCORE
# =========================

def calculate_sms_risk(features: dict) -> float:
    score = 0.0

    if features['has_url']:
        score += 3.0

    if features['phishing_flag']:
        score += 2.5

    if features['urgency_flag']:
        score += 1.5

    score += min(features['keyword_count'] * 0.5, 2.0)

    if features['has_phone']:
        score += 1.0

    return min(score, 10.0)


# =========================
# FINAL ANALYSIS (SAFE)
# =========================

def final_sms_risk_analysis(text: str) -> dict:
    try:
        features = extract_sms_features(text)
        rule_score = calculate_sms_risk(features)

        ml_prob = ml_predict(text)

        final_score = round(
            min((0.6 * ml_prob * 10) + (0.4 * rule_score), 10.0), 2
        )

        level = (
            "HIGH" if final_score >= 7
            else "MEDIUM" if final_score >= 4
            else "LOW"
        )

        return {
            "text": text,
            "rule_score": round(rule_score, 2),
            "ml_probability": round(ml_prob * 100, 2),
            "final_score": final_score,
            "risk_level": level
        }

    except Exception as e:
        print("FINAL ERROR:", e)
        return {
            "error": str(e)
        }
# =========================
# WRAPPER FOR API (IMPORTANT)
# =========================

def extract_urls(text: str):
    return re.findall(URL_REGEX, text)


def analyze_sms(text: str) -> dict:
    try:
        # 1. Existing SMS analysis (unchanged)
        result = final_sms_risk_analysis(text)

        sms_score = result.get("final_score", 0.0)
        sms_risk = result.get("risk_level", "UNKNOWN")

        # 2. Extract URLs from message
        urls = extract_urls(text)

        # 3. Send URLs to URL module
        url_results = []
        for url in urls:
            url_result = analyze_url(url)
            url_results.append({
                "url": url,
                "score": url_result.get("score", 0.0),
                "risk": url_result.get("risk", "UNKNOWN")
            })

        # 4. Fusion logic (simple but effective)
        max_url_score = max([u["score"] for u in url_results], default=0.0)
        final_score = max(sms_score, max_url_score)

        # Optional: derive final risk level
        final_risk = sms_risk
        if max_url_score > sms_score:
            final_risk = "HIGH" if max_url_score >= 7 else "MEDIUM"

        return {
            "score": final_score,
            "risk_level": final_risk,
            "sms_score": sms_score,
            "urls": url_results
        }

    except Exception as e:
        return {
            "score": 0.0,
            "risk_level": "UNKNOWN",
            "error": str(e)
        }