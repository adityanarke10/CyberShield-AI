import requests


def detect_technology(url):

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    response = requests.get(url, timeout=10)

    headers = response.headers
    html = response.text.lower()

    technologies = []

    # Server Detection
    if "Server" in headers:
        technologies.append(f"Server: {headers['Server']}")

    # Framework Detection
    if "react" in html:
        technologies.append("React")

    if "angular" in html:
        technologies.append("Angular")

    if "vue" in html:
        technologies.append("Vue.js")

    if "jquery" in html:
        technologies.append("jQuery")

    if "bootstrap" in html:
        technologies.append("Bootstrap")

    if "wordpress" in html:
        technologies.append("WordPress")

    if "cloudflare" in headers.get("Server", "").lower():
        technologies.append("Cloudflare")

    if "php" in headers.get("X-Powered-By", "").lower():
        technologies.append("PHP")

    if "asp.net" in headers.get("X-Powered-By", "").lower():
        technologies.append("ASP.NET")

    if len(technologies) == 0:
        technologies.append("No common technologies detected")

    return technologies