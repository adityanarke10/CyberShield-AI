import socket
import ssl
from urllib.parse import urlparse
from datetime import datetime


def scan_ssl(url):

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    hostname = urlparse(url).hostname

    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443), timeout=10) as sock:

        with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:

            cert = secure_sock.getpeercert()

            issuer = dict(x[0] for x in cert["issuer"])

            issued_to = dict(x[0] for x in cert["subject"])

            expire_date = datetime.strptime(
                cert["notAfter"],
                "%b %d %H:%M:%S %Y %Z"
            )

            days_left = (expire_date - datetime.utcnow()).days

            return {
                "issuer": issuer.get("organizationName", "Unknown"),
                "issued_to": issued_to.get("commonName", "Unknown"),
                "expires": expire_date.strftime("%d %B %Y"),
                "days_left": days_left,
                "version": secure_sock.version(),
                "status": "Valid" if days_left > 0 else "Expired"
            }