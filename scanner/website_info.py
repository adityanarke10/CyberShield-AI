import socket
import time
from urllib.parse import urlparse

import requests


def scan_website(url):
    """
    Scan basic information about a website.
    """

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    start_time = time.time()

    response = requests.get(url, timeout=10)

    response_time = round((time.time() - start_time) * 1000, 2)

    parsed = urlparse(response.url)

    ip_address = socket.gethostbyname(parsed.hostname)

    return {
        "url": response.url,
        "status_code": response.status_code,
        "response_time": response_time,
        "ip_address": ip_address,
        "server": response.headers.get("Server", "Unknown"),
        "content_type": response.headers.get("Content-Type", "Unknown"),
        "https": parsed.scheme.upper()
    }