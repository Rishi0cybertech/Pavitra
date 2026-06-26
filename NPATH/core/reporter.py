from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from datetime import datetime

SEVERITY_COLORS = {
    "CRITICAL": colors.HexColor("#FF0000"),
    "HIGH":     colors.HexColor("#FF6600"),
    "MEDIUM":   colors.HexColor("#FFA500"),
    "LOW":      colors.HexColor("#00AA00"),
}

def add_learning_section(story, styles, scan_data):
    learn_style = ParagraphStyle(
        "Learn", fontSize=13,
        textColor=colors.white,
        backColor=colors.HexColor("#1a1a2e"),
        fontName="Helvetica-Bold",
        spaceAfter=4, spaceBefore=12, leftIndent=6
    )
    story.append(Paragraph("How NPath Scanned This Target", learn_style))
    story.append(Spacer(1, 0.1*inch))

    concepts = [
        ["NMAP Command",  f"nmap -sV --open {scan_data.get('ip','')}"],
        ["-sV flag",      "Port ke peeche kaunsa software chal raha hai — version detect karta hai"],
        ["--open flag",   "Sirf open ports dikhata hai — filtered aur closed ignore karta hai"],
        ["TCP Handshake", "SYN → SYN-ACK → ACK — connection establish hone ka process"],
        ["Port States",   "Open = service active | Closed = koi service nahi | Filtered = firewall block kar raha hai"],
        ["127.0.0.1",     "Loopback address — apna khud ka machine scan karta hai, network pe nahi jaata"],
    ]

    ct = Table(concepts, colWidths=[1.8*inch, 4.7*inch])
    ct.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (0, -1), colors.HexColor("#2d2d44")),
        ("TEXTCOLOR",      (0, 0), (0, -1), colors.white),
        ("FONTNAME",       (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE",       (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (1, 0), (-1, -1), [colors.HexColor("#f0f4ff"), colors.white]),
        ("GRID",           (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("PADDING",        (0, 0), (-1, -1), 7),
    ]))
    story.append(ct)


def generate_report(scan_data: dict, output_file: str = "npath_report.pdf"):
    doc = SimpleDocTemplate(
        output_file, pagesize=A4,
        rightMargin=0.75*inch, leftMargin=0.75*inch,
        topMargin=0.75*inch,   bottomMargin=0.75*inch
    )
    styles = getSampleStyleSheet()
    story  = []

    # ── Title ──────────────────────────────────────────
    title_style = ParagraphStyle(
        "Title", fontSize=24,
        textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=6, fontName="Helvetica-Bold"
    )
    story.append(Paragraph("NPath — Network Scan Report", title_style))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles["Normal"]
    ))
    story.append(Spacer(1, 0.2*inch))

    # ── Target Summary ─────────────────────────────────
    target_data = [
        ["Target IP",  scan_data.get("ip",       "N/A")],
        ["Hostname",   scan_data.get("hostname",  "N/A")],
        ["Host State", scan_data.get("state",     "N/A")],
        ["Open Ports", str(len(scan_data.get("ports", [])))],
    ]
    t = Table(target_data, colWidths=[2*inch, 4*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (0, -1), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR",      (0, 0), (0, -1), colors.white),
        ("FONTNAME",       (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE",       (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (1, 0), (-1, -1), [colors.HexColor("#f5f5f5"), colors.white]),
        ("GRID",           (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING",        (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*inch))

    # ── Per Port ───────────────────────────────────────
    for port_info in scan_data.get("ports", []):
        intel     = port_info.get("intel", {})
        severity  = intel.get("severity", "MEDIUM")
        sev_color = SEVERITY_COLORS.get(severity, colors.grey)

        header_style = ParagraphStyle(
            "PortHeader", fontSize=13,
            textColor=colors.white,
            backColor=colors.HexColor("#1a1a2e"),
            fontName="Helvetica-Bold",
            spaceAfter=4, spaceBefore=12, leftIndent=6
        )
        story.append(Paragraph(
            f"Port {port_info['port']}/tcp — "
            f"{intel.get('service', port_info['service'])}",
            header_style
        ))

        badge_style = ParagraphStyle(
            "Badge", fontSize=10,
            textColor=colors.white,
            backColor=sev_color,
            fontName="Helvetica-Bold",
            spaceAfter=8, leftIndent=6
        )
        story.append(Paragraph(f"Severity: {severity}", badge_style))

        fix_steps = intel.get("how_to_fix", ["N/A"])
        fix_text  = "<br/>".join([f"• {s}" for s in fix_steps])

        details = [
            ["Why Open",      intel.get("why_open",           "N/A")],
            ["Who Uses",      intel.get("who_uses",           "N/A")],
            ["Who Exploits",  intel.get("who_exploits",       "N/A")],
            ["Risk",          intel.get("risk",               "N/A")],
            ["How to Fix",    Paragraph(fix_text, styles["Normal"])],
            ["Real CVE",      intel.get("real_world_example", "N/A")],
            ["Version Found", port_info.get("version",        "Unknown")],
        ]

        dt = Table(details, colWidths=[1.5*inch, 5*inch])
        dt.setStyle(TableStyle([
            ("BACKGROUND",     (0, 0), (0, -1), colors.HexColor("#2d2d44")),
            ("TEXTCOLOR",      (0, 0), (0, -1), colors.white),
            ("FONTNAME",       (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE",       (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (1, 0), (-1, -1), [colors.HexColor("#f9f9f9"), colors.white]),
            ("GRID",           (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("VALIGN",         (0, 0), (-1, -1), "TOP"),
            ("PADDING",        (0, 0), (-1, -1), 7),
        ]))
        story.append(dt)
        story.append(Spacer(1, 0.1*inch))

    # ── Learning Section ───────────────────────────────
    add_learning_section(story, styles, scan_data)

    doc.build(story)
    print(f"[✓] Report saved: {output_file}")
