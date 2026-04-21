import re

def b_analyze_python_code (code: str):
    issues = []

    if re.search(r"sk-[a-zA-Z0-9]{10,}", code):     # SPECIFIC API KEY (ex. OpenAI) HARDCODED
        issues.append({
            "type": "API Key Exposure",
            "severity": "high",
            "description": "Possible API Key hardcoded"
        })

    if re.search(r"password\s*=\s*['\"].+['\"]", code, re.IGNORECASE):  # PASSWORD HARDCODED
        issues.append ({
            "type": "hardcoded secret",
            "severity": "high",
            "description": "Password hardcoded"
        })

    if re.search(r"(api_key|token)\s*=\s*['\"].+['\"]", code, re.IGNORECASE):     # API KEY HARDCODED
        issues.append ({
            "type": "API Key Exposure",
            "severity": "high",
            "description": "Token/API key inside the code"
        })

    if "input(" in code:
        issues.append({
            "type": "User Input",
            "severity": "low",
            "description": "Input() detected"
        })

    return issues