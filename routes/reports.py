from flask import Blueprint, render_template, send_file
from flask_login import login_required
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from models.scan_history import ScanHistory

from scanner.website_info import scan_website
from scanner.header_scan import scan_headers
from scanner.ssl_scan import scan_ssl
from scanner.technology_scan import detect_technology
from scanner.cookie_scan import scan_cookies

reports = Blueprint("reports", __name__)


# ==========================
# Reports Page
# ==========================
@reports.route("/reports")
@login_required
def reports_page():

    scans = (
        ScanHistory.query
        .order_by(ScanHistory.scan_date.desc())
        .all()
    )

    return render_template(
        "reports.html",
        scans=scans
    )


# ==========================
# View Report
# ==========================
@reports.route("/view-report/<int:id>")
@login_required
def view_report(id):

    scan = ScanHistory.query.get_or_404(id)

    website_info = scan_website(scan.website)
    headers = scan_headers(scan.website)
    ssl_info = scan_ssl(scan.website)
    technologies = detect_technology(scan.website)
    cookies = scan_cookies(scan.website)
    # ---------------- Score Breakdown ----------------

    total_headers = len(headers)

    present_headers = sum(
        1 for value in headers.values()
        if value != "Missing"
    )

    header_score = int((present_headers / total_headers) * 100)

    ssl_score = 100 if ssl_info["status"] == "Valid" else 20

    secure_cookies = sum(
        1 for cookie in cookies
        if cookie["secure"] == "Yes"
    )

    cookie_score = int((secure_cookies / len(cookies)) * 100) if cookies else 0

    port_score = 60
    # ==========================
    # AI Analysis
    # ==========================

    ai_analysis = []

    # Analyze Security Headers
    for header, value in headers.items():

        if value == "Missing":
            ai_analysis.append(
                f"Security header '{header}' is missing. This increases the website's exposure to common web attacks."
            )

    # Analyze SSL
    if ssl_info["status"] == "Valid":

        ai_analysis.append(
            f"SSL certificate is valid and secured using {ssl_info['version']}."
        )

    else:

        ai_analysis.append(
            "SSL certificate is invalid or expired. Renew the certificate immediately."
        )

    # Analyze Cookies
    for cookie in cookies:

        if cookie["secure"] == "No":
            ai_analysis.append(
                f"Cookie '{cookie['name']}' is not marked Secure and may be transmitted over unsecured connections."
            )

    # Website Summary
    if scan.security_score >= 90:

        ai_analysis.append(
            "Overall website security posture is excellent with minimal risks detected."
        )


    elif scan.security_score >= 70:

        ai_analysis.append(
            "Website security is good but several improvements are recommended."
        )

    else:

        ai_analysis.append(
            "Website has multiple security weaknesses that should be addressed immediately."
        )

    # If nothing found
    if len(ai_analysis) == 0:
        ai_analysis.append(
            "No major security issues detected during this scan."
        )

    # ---------------- AI Recommendations ----------------

    ai_recommendations = []

    for header, value in headers.items():
        if value == "Missing":
            ai_recommendations.append(
                f"Add the '{header}' security header."
            )

    if ssl_info["status"] != "Valid":
        ai_recommendations.append(
            "Renew or replace the SSL certificate."
        )

    for cookie in cookies:
        if cookie["secure"] == "No":
            ai_recommendations.append(
                f"Mark cookie '{cookie['name']}' as Secure."
            )

    if not ai_recommendations:
        ai_recommendations.append(
            "Continue monitoring your website security regularly."
        )

    return render_template(
        "view_report.html",
        scan=scan,
        website_info=website_info,
        headers=headers,
        ssl_info=ssl_info,
        technologies=technologies,
        cookies=cookies,

        header_score = header_score,
        ssl_score = ssl_score,
        cookie_score = cookie_score,
        port_score = port_score,
        ai_analysis=ai_analysis,
        ai_recommendations=ai_recommendations
    )


# ==========================
# Download PDF
# ==========================
@reports.route("/download-report/<int:id>")
@login_required
def download_report(id):

    scan = ScanHistory.query.get_or_404(id)
    website_info = scan_website(scan.website)
    headers = scan_headers(scan.website)
    ssl_info = scan_ssl(scan.website)
    technologies = detect_technology(scan.website)
    cookies = scan_cookies(scan.website)
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER

    story = []

    # ===========================
    # TITLE
    # ===========================

    story.append(Paragraph("CyberShield AI", title))
    story.append(
        Paragraph(
            "Website Security Assessment Report",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 20))

    # ===========================
    # SUMMARY
    # ===========================

    summary = [

        ["Website", scan.website],

        ["Security Score", f"{scan.security_score}/100"],

        ["Risk Level", scan.risk_level],

        ["Scan Date", scan.scan_date.strftime("%d %b %Y %I:%M %p")]

    ]

    table = Table(summary, colWidths=[170, 320])

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#0ea5e9")),

        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.grey),

        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),

        ("BOTTOMPADDING", (0, 0), (-1, -1), 8)

    ]))

    story.append(table)

    story.append(Spacer(1, 20))

    # ===========================
    # WEBSITE INFORMATION
    # ===========================

    story.append(
        Paragraph(
            "<b>Website Information</b>",
            styles["Heading2"]
        )
    )

    website = [

        ["IP Address", website_info["ip_address"]],

        ["Server", website_info["server"]],

        ["Status Code", website_info["status_code"]],

        ["HTTPS", website_info["https"]],

        ["Response Time", f'{website_info["response_time"]} ms']

    ]

    table = Table(website, colWidths=[170, 320])

    table.setStyle(TableStyle([

        ("GRID", (0, 0), (-1, -1), 1, colors.grey),

        ("BACKGROUND", (0, 0), (0, -1), colors.beige)

    ]))

    story.append(table)

    story.append(Spacer(1, 20))

    # ===========================
    # SSL
    # ===========================

    story.append(
        Paragraph(
            "<b>SSL Certificate</b>",
            styles["Heading2"]
        )
    )

    ssl_table = [

        ["Status", ssl_info["status"]],

        ["Issuer", ssl_info["issuer"]],

        ["TLS Version", ssl_info["version"]],

        ["Expiry", ssl_info["expires"]]

    ]

    table = Table(ssl_table, colWidths=[170, 320])

    table.setStyle(TableStyle([

        ("GRID", (0, 0), (-1, -1), 1, colors.grey),

        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey)

    ]))

    story.append(table)

    story.append(Spacer(1, 20))

    # ===========================
    # SECURITY HEADERS
    # ===========================

    story.append(
        Paragraph(
            "<b>Security Headers</b>",
            styles["Heading2"]
        )
    )

    for h, v in headers.items():
        story.append(
            Paragraph(
                f"• <b>{h}</b> : {v}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 20))

    # ===========================
    # TECHNOLOGIES
    # ===========================

    story.append(
        Paragraph(
            "<b>Technologies Detected</b>",
            styles["Heading2"]
        )
    )

    for tech in technologies:
        story.append(
            Paragraph(
                f"• {tech}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 20))

    # ===========================
    # COOKIES
    # ===========================

    story.append(
        Paragraph(
            "<b>Cookie Analysis</b>",
            styles["Heading2"]
        )
    )

    for cookie in cookies:
        story.append(
            Paragraph(
                f"• {cookie['name']} | Secure: {cookie['secure']} | Domain: {cookie['domain']}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 20))

    # ===========================
    # FOOTER
    # ===========================

    story.append(
        Paragraph(
            "<b>Generated by CyberShield AI</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "This report was automatically generated from the latest security scan.",
            styles["BodyText"]
        )
    )

    doc.build(story)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"CyberShield_Report_{scan.id}.pdf",
        mimetype="application/pdf"
    )