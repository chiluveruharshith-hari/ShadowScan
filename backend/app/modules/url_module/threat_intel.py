import os
import requests
from typing import Dict, Any, Union

import os
print("API KEY:", os.getenv("GOOGLE_API_KEY"))
def check_url_safety(url: str) -> Dict[str, Any]:
    """
    Check if a URL is safe using Google Safe Browsing API with detailed debugging.
    Returns a dictionary containing API status and threat detection results.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        return {
            "api_working": False,
            "error": "GOOGLE_API_KEY not found in environment"
        }

    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "client": {"clientId": "shadow-scan", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    print(f"Calling Google Safe Browsing API for URL: {url}")
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=10)
        status_code = response.status_code
        print(f"Response Status Code: {status_code}")

        try:
            raw_data = response.json()
        except Exception:
            raw_data = response.text

        if status_code == 200:
            if isinstance(raw_data, dict):
                has_threat = "matches" in raw_data and bool(raw_data.get("matches"))
            else:
                has_threat = False
                
            if has_threat:
                print(">>> Threat detected! <<<")
            else:
                print("No threat found.")
            
            return {
                "status": status_code,
                "api_working": True,
                "has_threat": has_threat,
                "raw_response": raw_data
            }
        else:
            print(f"API Error: Received status {status_code}")
            return {
                "status": status_code,
                "api_working": False,
                "has_threat": False,
                "raw_response": raw_data
            }

    except Exception as e:
        print(f"Request failed: {str(e)}")
        return {
            "api_working": False,
            "error": str(e)
        }
