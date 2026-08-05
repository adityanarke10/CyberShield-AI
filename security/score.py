def calculate_security_score(result, headers, ssl_info, cookies):

    score = 100
    issues = []

    # HTTPS Check
    if result.get("https") != "HTTPS":
        score -= 20
        issues.append("Website is not using HTTPS.")

    # HTTP Status
    if result.get("status_code") != 200:
        score -= 5
        issues.append("Website returned a non-200 status code.")

    # Security Headers
    for header, status in headers.items():
        if status == "Missing":
            score -= 5
            issues.append(f"{header} header is missing.")

    # SSL Certificate
    if ssl_info:
        if ssl_info.get("status") != "Valid":
            score -= 25
            issues.append("SSL Certificate is expired or invalid.")

    # Cookies
    if cookies:
        for cookie in cookies:
            if cookie.get("secure") == "No":
                score -= 2
                issues.append(f"Cookie '{cookie['name']}' is not Secure.")

    # Minimum Score
    if score < 0:
        score = 0

    # Risk Level
    if score >= 90:
        risk = "Low"

    elif score >= 70:
        risk = "Medium"

    elif score >= 50:
        risk = "High"

    else:
        risk = "Critical"

    return {
        "score": score,
        "risk": risk,
        "issues": issues
    }