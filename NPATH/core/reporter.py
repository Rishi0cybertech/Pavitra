from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Flowable
from datetime import datetime

# ── Professional Color Palette ─────────────────────────────────
# Deep navy + slate + clean whites — no cheap colors
C_NAVY      = colors.HexColor("#0D1B2A")   # Primary dark
C_SLATE     = colors.HexColor("#1B2838")   # Section headers
C_STEEL     = colors.HexColor("#2E4057")   # Accent bars
C_MIST      = colors.HexColor("#F4F6F8")   # Row alternating
C_WHITE     = colors.HexColor("#FFFFFF")
C_BORDER    = colors.HexColor("#D0D7DE")   # Subtle borders
C_TEXT      = colors.HexColor("#1C2833")   # Body text
C_SUBTEXT   = colors.HexColor("#5D6D7E")   # Secondary text

# Severity — professional, not garish
C_CRITICAL  = colors.HexColor("#B71C1C")   # Deep crimson
C_HIGH      = colors.HexColor("#BF360C")   # Deep burnt orange
C_MEDIUM    = colors.HexColor("#E65100")   # Deep amber
C_LOW       = colors.HexColor("#1B5E20")   # Deep forest green

C_CRITICAL_BG = colors.HexColor("#FFEBEE")
C_HIGH_BG     = colors.HexColor("#FBE9E7")
C_MEDIUM_BG   = colors.HexColor("#FFF8E1")
C_LOW_BG      = colors.HexColor("#E8F5E9")

SEVERITY_COLOR = {
    "CRITICAL": C_CRITICAL,
    "HIGH":     C_HIGH,
    "MEDIUM":   C_MEDIUM,
    "LOW":      C_LOW,
}
SEVERITY_BG = {
    "CRITICAL": C_CRITICAL_BG,
    "HIGH":     C_HIGH_BG,
    "MEDIUM":   C_MEDIUM_BG,
    "LOW":      C_LOW_BG,
}

PAGE_W = A4[0]
PAGE_H = A4[1]
MARGIN = 0.75 * inch


# ── Custom Horizontal Rule ─────────────────────────────────────
class ThickRule(Flowable):
    def __init__(self, width, thickness=2, color=C_NAVY):
        Flowable.__init__(self)
        self.width     = width
        self.thickness = thickness
        self.color     = color
        self.height    = thickness + 4

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.thickness / 2, self.width, self.thickness / 2)


# ── Style Registry ─────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()
    usable_width = PAGE_W - 2 * MARGIN

    S = {}

    S["report_title"] = ParagraphStyle(
        "ReportTitle",
        fontName="Helvetica-Bold",
        fontSize=26,
        textColor=C_NAVY,
        spaceAfter=2,
        leading=30,
    )
    S["report_subtitle"] = ParagraphStyle(
        "ReportSubtitle",
        fontName="Helvetica",
        fontSize=9,
        textColor=C_SUBTEXT,
        spaceAfter=0,
        leading=14,
    )
    S["section_label"] = ParagraphStyle(
        "SectionLabel",
        fontName="Helvetica-Bold",
        fontSize=7,
        textColor=C_SUBTEXT,
        spaceBefore=18,
        spaceAfter=4,
        leading=10,
        letterSpacing=1.5,
    )
    S["port_title"] = ParagraphStyle(
        "PortTitle",
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=C_WHITE,
        leading=16,
        leftIndent=10,
        spaceAfter=0,
        spaceBefore=0,
    )
    S["severity_label"] = ParagraphStyle(
        "SeverityLabel",
        fontName="Helvetica-Bold",
        fontSize=8,
        textColor=C_WHITE,
        leading=12,
        leftIndent=10,
        spaceAfter=0,
        spaceBefore=0,
        letterSpacing=1.2,
    )
    S["field_key"] = ParagraphStyle(
        "FieldKey",
        fontName="Helvetica-Bold",
        fontSize=8,
        textColor=C_WHITE,
        leading=13,
        leftIndent=6,
        spaceAfter=0,
        letterSpacing=0.5,
    )
    S["field_value"] = ParagraphStyle(
        "FieldValue",
        fontName="Helvetica",
        fontSize=9,
        textColor=C_TEXT,
        leading=14,
        leftIndent=0,
        spaceAfter=0,
    )
    S["fix_step"] = ParagraphStyle(
        "FixStep",
        fontName="Helvetica",
        fontSize=9,
        textColor=C_TEXT,
        leading=15,
        leftIndent=0,
        spaceAfter=2,
    )
    S["learn_header"] = ParagraphStyle(
        "LearnHeader",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=C_WHITE,
        leading=16,
        leftIndent=10,
        spaceAfter=0,
        spaceBefore=0,
    )
    S["learn_key"] = ParagraphStyle(
        "LearnKey",
        fontName="Helvetica-Bold",
        fontSize=8,
        textColor=C_WHITE,
        leading=13,
        leftIndent=6,
        letterSpacing=0.3,
    )
    S["learn_val"] = ParagraphStyle(
        "LearnVal",
        fontName="Helvetica",
        fontSize=9,
        textColor=C_TEXT,
        leading=15,
    )
    S["footer_text"] = ParagraphStyle(
        "FooterText",
        fontName="Helvetica",
        fontSize=7.5,
        textColor=C_SUBTEXT,
        alignment=TA_CENTER,
        leading=11,
    )
    S["summary_key"] = ParagraphStyle(
        "SummaryKey",
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=C_WHITE,
        leading=13,
        leftIndent=6,
    )
    S["summary_val"] = ParagraphStyle(
        "SummaryVal",
        fontName="Helvetica",
        fontSize=9,
        textColor=C_TEXT,
        leading=13,
    )
    S["severity_count"] = ParagraphStyle(
        "SeverityCount",
        fontName="Helvetica-Bold",
        fontSize=18,
        textColor=C_NAVY,
        leading=22,
        alignment=TA_CENTER,
    )
    S["severity_count_label"] = ParagraphStyle(
        "SeverityCountLabel",
        fontName="Helvetica",
        fontSize=7.5,
        textColor=C_SUBTEXT,
        leading=11,
        alignment=TA_CENTER,
        letterSpacing=0.8,
    )

    return S, base, usable_width


# ── Severity Summary Cards ─────────────────────────────────────
def build_severity_summary(severities, styles, usable_width):
    counts = {
        "CRITICAL": severities.count("CRITICAL"),
        "HIGH":     severities.count("HIGH"),
        "MEDIUM":   severities.count("MEDIUM"),
        "LOW":      severities.count("LOW"),
    }

    cell_w = usable_width / 4

    header_row = [
        Paragraph("CRITICAL", styles["severity_count_label"]),
        Paragraph("HIGH",     styles["severity_count_label"]),
        Paragraph("MEDIUM",   styles["severity_count_label"]),
        Paragraph("LOW",      styles["severity_count_label"]),
    ]
    count_row = [
        Paragraph(str(counts["CRITICAL"]), styles["severity_count"]),
        Paragraph(str(counts["HIGH"]),     styles["severity_count"]),
        Paragraph(str(counts["MEDIUM"]),   styles["severity_count"]),
        Paragraph(str(counts["LOW"]),      styles["severity_count"]),
    ]

    t = Table([header_row, count_row], colWidths=[cell_w] * 4)
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (0, -1), C_CRITICAL_BG),
        ("BACKGROUND",  (1, 0), (1, -1), C_HIGH_BG),
        ("BACKGROUND",  (2, 0), (2, -1), C_MEDIUM_BG),
        ("BACKGROUND",  (3, 0), (3, -1), C_LOW_BG),
        ("ALIGN",       (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING",     (0, 0), (-1, -1), 10),
        ("LINEABOVE",   (0, 0), (0, 0), 3, C_CRITICAL),
        ("LINEABOVE",   (1, 0), (1, 0), 3, C_HIGH),
        ("LINEABOVE",   (2, 0), (2, 0), 3, C_MEDIUM),
        ("LINEABOVE",   (3, 0), (3, 0), 3, C_LOW),
        ("GRID",        (0, 0), (-1, -1), 0.5, C_BORDER),
        ("ROUNDEDCORNERS", [3]),
    ]))
    return t


# ── Scan Summary Table ─────────────────────────────────────────
def build_scan_summary(scan_data, styles, usable_width):
    col1 = usable_width * 0.22
    col2 = usable_width * 0.28
    col3 = usable_width * 0.22
    col4 = usable_width * 0.28

    rows = [
        [
            Paragraph("TARGET IP",   styles["summary_key"]),
            Paragraph(scan_data.get("ip", "N/A"), styles["summary_val"]),
            Paragraph("HOSTNAME",    styles["summary_key"]),
            Paragraph(scan_data.get("hostname", "N/A") or "N/A", styles["summary_val"]),
        ],
        [
            Paragraph("HOST STATE",  styles["summary_key"]),
            Paragraph(scan_data.get("state", "N/A").upper(), styles["summary_val"]),
            Paragraph("OPEN PORTS",  styles["summary_key"]),
            Paragraph(str(len(scan_data.get("ports", []))), styles["summary_val"]),
        ],
        [
            Paragraph("SCAN ENGINE", styles["summary_key"]),
            Paragraph("NMAP via NPath v1.0", styles["summary_val"]),
            Paragraph("SCAN MODE",   styles["summary_key"]),
            Paragraph("Service Version Detection (-sV --open)", styles["summary_val"]),
        ],
    ]

    t = Table(rows, colWidths=[col1, col2, col3, col4])
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (0, -1), C_SLATE),
        ("BACKGROUND",     (2, 0), (2, -1), C_SLATE),
        ("TEXTCOLOR",      (0, 0), (0, -1), C_WHITE),
        ("TEXTCOLOR",      (2, 0), (2, -1), C_WHITE),
        ("ROWBACKGROUNDS", (1, 0), (1, -1), [C_MIST, C_WHITE]),
        ("ROWBACKGROUNDS", (3, 0), (3, -1), [C_MIST, C_WHITE]),
        ("GRID",           (0, 0), (-1, -1), 0.4, C_BORDER),
        ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING",        (0, 0), (-1, -1), 8),
        ("FONTSIZE",       (0, 0), (-1, -1), 9),
    ]))
    return t


# ── Per-Port Section ───────────────────────────────────────────
def build_port_section(port_info, styles, usable_width):
    elements = []

    intel     = port_info.get("intel", {})
    severity  = intel.get("severity", "MEDIUM")
    sev_color = SEVERITY_COLOR.get(severity, C_STEEL)
    sev_bg    = SEVERITY_BG.get(severity, C_MIST)
    version   = port_info.get("version", "Unknown")
    service   = intel.get("service", port_info.get("service", "Unknown")).upper()

    # Port header bar
    header_data = [[
        Paragraph(
            f"PORT {port_info['port']}/TCP  —  {service}",
            styles["port_title"]
        ),
        Paragraph(
            f"VERSION DETECTED: {version}",
            ParagraphStyle(
                "VersionRight",
                fontName="Helvetica",
                fontSize=8,
                textColor=colors.HexColor("#B0BEC5"),
                leading=12,
                alignment=TA_RIGHT,
            )
        ),
    ]]
    header_t = Table(header_data, colWidths=[usable_width * 0.65, usable_width * 0.35])
    header_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_NAVY),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING",    (0, 0), (-1, -1), 10),
        ("LINEBELOW",  (0, 0), (-1, -1), 3, sev_color),
    ]))
    elements.append(header_t)

    # Severity badge row
    badge_data = [[
        Paragraph(f"SEVERITY: {severity}", styles["severity_label"]),
        Paragraph(
            _severity_description(severity),
            ParagraphStyle(
                "SevDesc",
                fontName="Helvetica",
                fontSize=8,
                textColor=colors.HexColor("#CFD8DC"),
                leading=12,
                alignment=TA_RIGHT,
            )
        ),
    ]]
    badge_t = Table(badge_data, colWidths=[usable_width * 0.35, usable_width * 0.65])
    badge_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), sev_color),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING",    (0, 0), (-1, -1), 6),
    ]))
    elements.append(badge_t)

    # Intelligence table
    fix_steps = intel.get("how_to_fix", ["No remediation data available."])
    fix_content = Paragraph(
        "".join([f"<b>{i+1}.</b> {s}<br/>" for i, s in enumerate(fix_steps)]),
        styles["fix_step"]
    )

    detail_rows = [
        [
            Paragraph("WHAT IS THIS PORT?", styles["field_key"]),
            Paragraph(
                f"{intel.get('service', 'N/A')} — {intel.get('why_open', 'No data available.')}",
                styles["field_value"]
            ),
        ],
        [
            Paragraph("WHO USES IT?", styles["field_key"]),
            Paragraph(intel.get("who_uses", "N/A"), styles["field_value"]),
        ],
        [
            Paragraph("WHO EXPLOITS IT?", styles["field_key"]),
            Paragraph(intel.get("who_exploits", "N/A"), styles["field_value"]),
        ],
        [
            Paragraph("RISK IMPACT", styles["field_key"]),
            Paragraph(intel.get("risk", "N/A"), styles["field_value"]),
        ],
        [
            Paragraph("REMEDIATION STEPS", styles["field_key"]),
            fix_content,
        ],
        [
            Paragraph("CVE REFERENCE", styles["field_key"]),
            Paragraph(intel.get("real_world_example", "N/A"), styles["field_value"]),
        ],
    ]

    col_key = usable_width * 0.22
    col_val = usable_width * 0.78

    dt = Table(detail_rows, colWidths=[col_key, col_val])
    dt.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (0, -1), C_STEEL),
        ("TEXTCOLOR",      (0, 0), (0, -1), C_WHITE),
        ("ROWBACKGROUNDS", (1, 0), (1, -1), [C_WHITE, C_MIST]),
        ("BACKGROUND",     (1, 4), (1, 4), sev_bg),
        ("GRID",           (0, 0), (-1, -1), 0.4, C_BORDER),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("PADDING",        (0, 0), (-1, -1), 9),
        ("LINEAFTER",      (0, 0), (0, -1), 2, sev_color),
    ]))
    elements.append(dt)
    elements.append(Spacer(1, 0.2 * inch))

    return KeepTogether(elements)


def _severity_description(severity):
    descriptions = {
        "CRITICAL": "Immediate action required — high probability of exploitation",
        "HIGH":     "Address within 24 hours — significant exposure risk",
        "MEDIUM":   "Schedule remediation — moderate risk in current context",
        "LOW":      "Monitor and review — minimal risk in isolated environment",
    }
    return descriptions.get(severity, "")


# ── Learning Section ───────────────────────────────────────────
def build_learning_section(scan_data, styles, usable_width):
    elements = []

    # Header
    header_data = [[Paragraph("HOW NPATH SCANNED THIS TARGET", styles["learn_header"])]]
    header_t = Table(header_data, colWidths=[usable_width])
    header_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), C_NAVY),
        ("PADDING",    (0, 0), (-1, -1), 10),
        ("LINEBELOW",  (0, 0), (-1, -1), 2, C_STEEL),
    ]))
    elements.append(header_t)

    concepts = [
        [
            Paragraph("COMMAND ISSUED", styles["learn_key"]),
            Paragraph(
                f"<font name='Courier'><b>nmap -sV --open {scan_data.get('ip', '')}</b></font><br/>"
                "This is the exact command NPath executed internally to discover open ports "
                "and identify the software version running behind each one.",
                styles["learn_val"]
            ),
        ],
        [
            Paragraph("-sV FLAG", styles["learn_key"]),
            Paragraph(
                "<b>Service Version Detection.</b> Probes each open port to identify the "
                "exact software and version running — e.g., OpenSSH 7.4, Apache 2.4.6. "
                "Version information is critical because older versions frequently carry "
                "known, documented vulnerabilities (CVEs).",
                styles["learn_val"]
            ),
        ],
        [
            Paragraph("--OPEN FLAG", styles["learn_key"]),
            Paragraph(
                "<b>Open ports only.</b> Instructs NMAP to display only ports in an OPEN "
                "state. Ports can exist in three states: <b>Open</b> (actively accepting "
                "connections), <b>Closed</b> (port accessible but no service listening), "
                "or <b>Filtered</b> (firewall is blocking probe packets). NPath focuses "
                "on open ports — these are the attack surface.",
                styles["learn_val"]
            ),
        ],
        [
            Paragraph("TCP HANDSHAKE", styles["learn_key"]),
            Paragraph(
                "<b>Three-way handshake protocol.</b> To verify a port is open, NPath "
                "sends a SYN packet. An open port responds with SYN-ACK; NPath completes "
                "with ACK. This is the foundational mechanism of all TCP communication "
                "and the basis of port scanning.",
                styles["learn_val"]
            ),
        ],
        [
            Paragraph("LOOPBACK ADDRESS", styles["learn_key"]),
            Paragraph(
                "<b>127.0.0.1 — Your own machine.</b> Scanning the loopback address means "
                "you are scanning yourself. No packets leave your computer. This is the "
                "safest way to test NPath, understand what services you are running, and "
                "learn how scanning works without any legal or ethical concerns.",
                styles["learn_val"]
            ),
        ],
        [
            Paragraph("WHAT IS A PORT?", styles["learn_key"]),
            Paragraph(
                "<b>A numbered communication endpoint.</b> Every service on a computer "
                "listens on a specific port number. SSH uses port 22, HTTP uses port 80, "
                "databases use 3306 or 5432. An open, unprotected port is an entry point — "
                "understanding which ports are exposed and why is fundamental to network security.",
                styles["learn_val"]
            ),
        ],
    ]

    col_key = usable_width * 0.18
    col_val = usable_width * 0.82

    ct = Table(concepts, colWidths=[col_key, col_val])
    ct.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (0, -1), C_SLATE),
        ("TEXTCOLOR",      (0, 0), (0, -1), C_WHITE),
        ("ROWBACKGROUNDS", (1, 0), (1, -1), [C_WHITE, C_MIST]),
        ("GRID",           (0, 0), (-1, -1), 0.4, C_BORDER),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("PADDING",        (0, 0), (-1, -1), 10),
        ("LINEAFTER",      (0, 0), (0, -1), 2, C_STEEL),
    ]))
    elements.append(ct)

    return elements


# ── Page Header/Footer ─────────────────────────────────────────
def _on_page(canvas, doc):
    canvas.saveState()
    w, h = A4

    # Top accent line
    canvas.setFillColor(C_NAVY)
    canvas.rect(0, h - 6*mm, w, 6*mm, fill=1, stroke=0)

    # Footer
    canvas.setFillColor(C_SUBTEXT)
    canvas.setFont("Helvetica", 7)
    footer = (
        f"NPath v1.0  |  Confidential Scan Report  |  "
        f"Page {doc.page}  |  "
        f"Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  "
        f"github.com/Rishi0cybertech/Pavitra"
    )
    canvas.drawCentredString(w / 2, 10*mm, footer)

    # Footer line
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 16*mm, w - MARGIN, 16*mm)

    canvas.restoreState()


# ── Main Generator ─────────────────────────────────────────────
def generate_report(scan_data: dict, output_file: str = "npath_report.pdf"):
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        rightMargin=MARGIN,
        leftMargin=MARGIN,
        topMargin=0.9 * inch,
        bottomMargin=0.9 * inch,
    )

    styles, base, usable_width = build_styles()
    story = []

    # ── Cover Header ───────────────────────────────────────────
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("NPath", styles["report_title"]))
    story.append(Paragraph(
        "Network Vulnerability Scan Report",
        ParagraphStyle(
            "SubHead",
            fontName="Helvetica",
            fontSize=13,
            textColor=C_STEEL,
            spaceAfter=2,
            leading=18,
        )
    ))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y')} at "
        f"{datetime.now().strftime('%H:%M:%S')}  ·  "
        f"Classification: Internal Use Only  ·  Tool: NPath v1.0",
        styles["report_subtitle"]
    ))
    story.append(Spacer(1, 0.08 * inch))
    story.append(ThickRule(usable_width, thickness=2, color=C_NAVY))
    story.append(Spacer(1, 0.2 * inch))

    # ── Scan Summary ───────────────────────────────────────────
    story.append(Paragraph("SCAN SUMMARY", styles["section_label"]))
    story.append(build_scan_summary(scan_data, styles, usable_width))
    story.append(Spacer(1, 0.2 * inch))

    # ── Severity Overview ──────────────────────────────────────
    open_ports = scan_data.get("ports", [])
    severities = [p["intel"].get("severity", "MEDIUM") for p in open_ports]

    story.append(Paragraph("SEVERITY OVERVIEW", styles["section_label"]))
    story.append(build_severity_summary(severities, styles, usable_width))
    story.append(Spacer(1, 0.25 * inch))

    # ── Per-Port Intelligence ──────────────────────────────────
    if open_ports:
        story.append(ThickRule(usable_width, thickness=0.5, color=C_BORDER))
        story.append(Spacer(1, 0.15 * inch))
        story.append(Paragraph("PORT INTELLIGENCE REPORT", styles["section_label"]))
        story.append(Spacer(1, 0.05 * inch))

        for port_info in open_ports:
            story.append(build_port_section(port_info, styles, usable_width))

    # ── Learning Section ───────────────────────────────────────
    story.append(Spacer(1, 0.1 * inch))
    story.append(ThickRule(usable_width, thickness=0.5, color=C_BORDER))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("EDUCATIONAL REFERENCE", styles["section_label"]))
    story.append(Spacer(1, 0.05 * inch))
    story.extend(build_learning_section(scan_data, styles, usable_width))

    # ── Disclaimer ─────────────────────────────────────────────
    story.append(Spacer(1, 0.25 * inch))
    story.append(ThickRule(usable_width, thickness=0.5, color=C_BORDER))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        "LEGAL DISCLAIMER: This report was generated by NPath for authorized use only. "
        "Scanning networks or systems without explicit written permission is illegal under "
        "the Information Technology Act, 2000 (India) and equivalent legislation globally. "
        "NPath and its authors assume no liability for unauthorized use of this tool or its output.",
        ParagraphStyle(
            "Disclaimer",
            fontName="Helvetica",
            fontSize=7.5,
            textColor=C_SUBTEXT,
            leading=12,
            alignment=TA_CENTER,
        )
    ))

    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    print(f"[✓] Report saved: {output_file}")
