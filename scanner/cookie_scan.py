import requests


def scan_cookies(url):

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    response = requests.get(url, timeout=10)

    cookies = []

    for cookie in response.cookies:

        cookies.append({
            "name": cookie.name,
            "secure": "Yes" if cookie.secure else "No",
            "domain": cookie.domain,
            "path": cookie.path
        })

    if not cookies:
        cookies.append({
            "name": "No Cookies Found",
            "secure": "-",
            "domain": "-",
            "path": "-"
        })

    return cookies