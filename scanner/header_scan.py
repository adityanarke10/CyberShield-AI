import requests


def scan_headers(url):

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    response = requests.get(url, timeout=10)

    headers = response.headers

    security_headers = {
        "Content-Security-Policy": headers.get("Content-Security-Policy", "Missing"),
        "Strict-Transport-Security": headers.get("Strict-Transport-Security", "Missing"),
        "X-Frame-Options": headers.get("X-Frame-Options", "Missing"),
        "X-Content-Type-Options": headers.get("X-Content-Type-Options", "Missing"),
        "Referrer-Policy": headers.get("Referrer-Policy", "Missing"),
        "Permissions-Policy": headers.get("Permissions-Policy", "Missing")
    }

    return security_headers