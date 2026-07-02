from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether
)
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.platypus import Flowable
from datetime import datetime

C_DARK      = colors.HexColor("#0A0E1A")
C_PURPLE    = colors.HexColor("#1A1040")
C_VIOLET    = colors.HexColor("#2D1B69")
C_TEAL      = colors.HexColor("#0D7377")
C_MIST      = colors.HexColor("#F0F4F8")
C_WHITE     = colors.HexColor("#FFFFFF")
C_BORDER    = colors.HexColor("#C8D0E0")
C_TEXT      = colors.HexColor("#1A1A2E")
C_SUBTEXT   = colors.HexColor("#6B7280")
C_SAFE      = colors.HexColor("#065F46")
C_SAFE_BG   = colors.HexColor("#ECFDF5")
C_WARN      = colors.HexColor("#92400E")
C_WARN_BG   = colors.HexColor("#FFFBEB")
C_DANGER    = colors.HexColor("#991B1B")
C_DANGER_BG = colors.HexColor("#FEF2F2")

PAGE_W = A4[0]
MARGIN = 0.75 * inch


class ThickRule(Flowable):
    def __init__(self, width, thickness=2, color=C_DARK):
        Flowable.__init__(self)
        self.width     = width
        self.thickness = thickness
        self.color     = color
        self.height    = thickness + 4

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.thickness / 2, self.width, self.thickness / 2)


def build_styles():
    usable_width = PAGE_W - 2 * MARGIN
    S = {}
    S["title"] = ParagraphStyle(
        "Title", fontName="Helvetica-Bold", fontSize=26,
        textColor=C_DARK, spaceAfter=2, leading=30
    )
    S["subtitle"] = ParagraphStyle(
        "Subtitle", fontName="Helvetica", fontSize=9,
        textColor=C_SUBTEXT, spaceAfter=0, leading=14
    )
    S["section"] = ParagraphStyle(
        "Section", fontName="Helvetica-Bold", fontSize=7,
        textColor=C_SUBTEXT, spaceBefore=18, spaceAfter=4,
        leading=10, letterSpacing=1.5
    )
    S["key"] = ParagraphStyle(
        "Key", fontName="Helvetica-Bold", fontSize=8,
        textColor=C_WHITE, leading=13, leftIndent=6
    )
    S["val"] = ParagraphStyle(
        "Val", fontName="Helvetica", fontSize=9,
        textColor=C_TEXT, leading=14
    )
    S["learn_key"] = ParagraphStyle(
        "LearnKey", fontName="Helvetica-Bold", fontSize=8,
        textColor=C_WHITE, leading=13, leftIndent=6
    )
    S["learn_val"] = ParagraphStyle(
        "LearnVal", fontName="Helvetica", fontSize=9,
        textColor=C_TEXT, leading=15
    )
    S["packet_row"] = ParagraphStyle(
        "PacketRow", fontName="Helvetica", fontSize=8,
        textColor=C_TEXT, leading=12
    )
    return S, usable_width


def _on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(C_TEAL)
    canvas.rect(0, h - 6*mm, w, 6*mm, fill=1, stroke=0)
    canvas.setFillColor(C_SUBTEXT)
    canvas.setFont("Helvetica", 7)
    footer = (
        f"WaveTrace v1.0  |  Network Analysis Report  |  "
        f"Page {doc.page}  |  "
        f"Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  "
        f"github.com/Rishi0cybertech/Pavitra"
    )
    canvas.drawCentredString(w / 2, 10*mm, footer)
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 16*mm, w - MARGIN, 16*mm)
    canvas.restoreState()


def generate_report(stats: dict, output_file: str = "wavetrace_report.pdf"):
    doc = SimpleDocTemplate(
        output_file, pagesize=A4,
        rightMargin=MARGIN, leftMargin=MARGIN,
        topMargin=0.9*inch, bottomMargin=0.9*inch
    )
    S, usable_width = build_styles()
    story = []

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("WaveTrace", S["title"]))
    story.append(Paragraph(
        "Network Packet Analysis Report",
        ParagraphStyle("Sub2", fontName="Helvetica", fontSize=13,
                       textColor=C_TEAL, spaceAfter=2, leading=18)
    ))
    story.append(Paragraph(
        f"Captured on {datetime.now().strftime('%B %d, %Y')} at "
        f"{stats.get('start_time', 'N/A')}  ·  "
        f"Interface: {stats.get('interface', 'N/A')}  ·  "
        f"Tool: WaveTrace v1.0",
        S["subtitle"]
    ))
    story.append(Spacer(1, 0.08*inch))
    story.append(ThickRule(usable_width, thickness=2, color=C_TEAL))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("CAPTURE SUMMARY", S["section"]))
    packets    = stats.get("packets", [])
    protocols  = stats.get("protocols", {})
    suspicious = stats.get("suspicious", [])

    summary_rows = [
        [Paragraph("INTERFACE",      S["key"]),
         Paragraph(stats.get("interface", "N/A"), S["val"]),
         Paragraph("START TIME",     S["key"]),
         Paragraph(stats.get("start_time", "N/A"), S["val"])],
        [Paragraph("TOTAL PACKETS",  S["key"]),
         Paragraph(str(stats.get("total", 0)), S["val"]),
         Paragraph("END TIME",       S["key"]),
         Paragraph(stats.get("end_time", "N/A"), S["val"])],
        [Paragraph("PROTOCOLS SEEN", S["key"]),
         Paragraph(str(len(protocols)), S["val"]),
         Paragraph("SUSPICIOUS",     S["key"]),
         Paragraph(str(len(suspicious)), S["val"])],
        [Paragraph("UNIQUE SOURCES", S["key"]),
         Paragraph(str(len(stats.get("src_ips", {}))), S["val"]),
         Paragraph("UNIQUE DESTS",   S["key"]),
         Paragraph(str(len(stats.get("dst_ips", {}))), S["val"])],
    ]

    col = usable_width / 4
    st = Table(summary_rows, colWidths=[col*0.85, col*1.15, col*0.85, col*1.15])
    st.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (0, -1), C_VIOLET),
        ("BACKGROUND",     (2, 0), (2, -1), C_VIOLET),
        ("TEXTCOLOR",      (0, 0), (0, -1), C_WHITE),
        ("TEXTCOLOR",      (2, 0), (2, -1), C_WHITE),
        ("ROWBACKGROUNDS", (1, 0), (1, -1), [C_MIST, C_WHITE]),
        ("ROWBACKGROUNDS", (3, 0), (3, -1), [C_MIST, C_WHITE]),
        ("GRID",           (0, 0), (-1, -1), 0.4, C_BORDER),
        ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING",        (0, 0), (-1, -1), 8),
    ]))
    story.append(st)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("PROTOCOL BREAKDOWN", S["section"]))

    enriched = stats.get("enriched_protocols", {})
    total = max(stats.get("total", 1), 1)

    SEVERITY_DISPLAY_COLOR = {
        "CRITICAL": C_DANGER,
        "HIGH":     C_DANGER,
        "MEDIUM":   C_WARN,
        "LOW":      C_SAFE,
    }

    proto_header = [[
        Paragraph("PROTOCOL", S["key"]),
        Paragraph("PACKETS",  S["key"]),
        Paragraph("SHARE",    S["key"]),
        Paragraph("RISK",     S["key"]),
    ]]

    proto_rows = []
    sorted_protos = sorted(enriched.items(), key=lambda x: x[1]["count"], reverse=True)

    for proto, data in sorted_protos:
        count = data["count"]
        severity = data["intel"].get("severity", "MEDIUM")
        color = SEVERITY_DISPLAY_COLOR.get(severity, C_SUBTEXT)
        share = f"{(count/total)*100:.1f}%"
        proto_rows.append([
            Paragraph(proto, ParagraphStyle(
                "P", fontName="Helvetica-Bold", fontSize=9,
                textColor=C_DARK, leading=13)),
            Paragraph(str(count), S["val"]),
            Paragraph(share,      S["val"]),
            Paragraph(severity, ParagraphStyle(
                "R", fontName="Helvetica-Bold", fontSize=8,
                textColor=color, leading=13)),
        ])

    pt = Table(proto_header + proto_rows,
               colWidths=[usable_width*0.3, usable_width*0.2,
                          usable_width*0.2,  usable_width*0.3])
    pt.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0), C_PURPLE),
        ("TEXTCOLOR",      (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME",       (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, C_MIST]),
        ("GRID",           (0, 0), (-1, -1), 0.4, C_BORDER),
        ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING",        (0, 0), (-1, -1), 8),
    ]))
    story.append(pt)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("PROTOCOL INTELLIGENCE", S["section"]))

    for proto, data in sorted_protos:
        intel = data["intel"]
        severity = intel.get("severity", "MEDIUM")
        color = SEVERITY_DISPLAY_COLOR.get(severity, C_SUBTEXT)

        red_flags = intel.get("red_flags", ["No known red flags on file"])
        flags_text = "".join([f"• {f}<br/>" for f in red_flags])

        detail_rows = [
            [Paragraph(f"{proto} — {intel.get('protocol_name', proto)}",
                       ParagraphStyle("PH", fontName="Helvetica-Bold", fontSize=10,
                                      textColor=C_WHITE, leading=14)),
             ""],
            [Paragraph("WHY SEEN", S["key"]),
             Paragraph(intel.get("why_seen", "N/A"), S["val"])],
            [Paragraph("WHO USES IT", S["key"]),
             Paragraph(intel.get("who_uses", "N/A"), S["val"])],
            [Paragraph("WHO EXPLOITS IT", S["key"]),
             Paragraph(intel.get("who_exploits", "N/A"), S["val"])],
            [Paragraph("RISK", S["key"]),
             Paragraph(intel.get("risk", "N/A"), S["val"])],
            [Paragraph("RED FLAGS TO WATCH", S["key"]),
             Paragraph(flags_text, S["val"])],
            [Paragraph("REAL WORLD EXAMPLE", S["key"]),
             Paragraph(intel.get("real_world_example", "N/A"), S["val"])],
        ]

        dt = Table(detail_rows, colWidths=[usable_width*0.22, usable_width*0.78])
        dt.setStyle(TableStyle([
            ("BACKGROUND",     (0, 0), (-1, 0), color),
            ("SPAN",           (0, 0), (-1, 0)),
            ("BACKGROUND",     (0, 1), (0, -1), C_VIOLET),
            ("TEXTCOLOR",      (0, 1), (0, -1), C_WHITE),
            ("ROWBACKGROUNDS", (1, 1), (1, -1), [C_WHITE, C_MIST]),
            ("GRID",           (0, 0), (-1, -1), 0.4, C_BORDER),
            ("VALIGN",         (0, 0), (-1, -1), "TOP"),
            ("PADDING",        (0, 0), (-1, -1), 8),
        ]))
        story.append(KeepTogether([dt, Spacer(1, 0.15*inch)]))

    if suspicious:
        story.append(Paragraph("SUSPICIOUS TRAFFIC DETECTED", S["section"]))
        sus_header = [[
            Paragraph("PKT #",  S["key"]),
            Paragraph("SOURCE", S["key"]),
            Paragraph("DEST",   S["key"]),
            Paragraph("PORT",   S["key"]),
            Paragraph("REASON", S["key"]),
        ]]
        sus_rows = []
        for s in suspicious:
            sus_rows.append([
                Paragraph(str(s["packet"]), S["val"]),
                Paragraph(s["src"],         S["val"]),
                Paragraph(s["dst"],         S["val"]),
                Paragraph(str(s["port"]),   S["val"]),
                Paragraph(s["reason"],      S["val"]),
            ])
        sus_t = Table(
            sus_header + sus_rows,
            colWidths=[usable_width*0.08, usable_width*0.22,
                       usable_width*0.22, usable_width*0.1,
                       usable_width*0.38]
        )
        sus_t.setStyle(TableStyle([
            ("BACKGROUND",     (0, 0), (-1, 0), C_DANGER),
            ("TEXTCOLOR",      (0, 0), (-1, 0), C_WHITE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_DANGER_BG, C_WHITE]),
            ("GRID",           (0, 0), (-1, -1), 0.4, C_BORDER),
            ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
            ("PADDING",        (0, 0), (-1, -1), 8),
        ]))
        story.append(sus_t)
        story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("PACKET CAPTURE LOG", S["section"]))
    pkt_header = [[
        Paragraph("#",        S["key"]),
        Paragraph("TIME",     S["key"]),
        Paragraph("PROTOCOL", S["key"]),
        Paragraph("SOURCE",   S["key"]),
        Paragraph("DEST",     S["key"]),
        Paragraph("LENGTH",   S["key"]),
        Paragraph("STATUS",   S["key"]),
    ]]
    pkt_rows = []
    for p in packets:
        status_style = ParagraphStyle(
            "PS", fontName="Helvetica-Bold", fontSize=8,
            textColor=C_DANGER if p["suspicious"] else C_SAFE,
            leading=12
        )
        pkt_rows.append([
            Paragraph(str(p["num"]),    S["packet_row"]),
            Paragraph(p["time"],        S["packet_row"]),
            Paragraph(p["protocol"],    S["packet_row"]),
            Paragraph(p["src"],         S["packet_row"]),
            Paragraph(p["dst"],         S["packet_row"]),
            Paragraph(str(p["length"]), S["packet_row"]),
            Paragraph("SUSPICIOUS" if p["suspicious"] else "NORMAL", status_style),
        ])
    pkt_t = Table(
        pkt_header + pkt_rows,
        colWidths=[usable_width*0.05, usable_width*0.1,
                   usable_width*0.1,  usable_width*0.2,
                   usable_width*0.2,  usable_width*0.08,
                   usable_width*0.27]
    )
    pkt_t.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0), C_PURPLE),
        ("TEXTCOLOR",      (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME",       (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, C_MIST]),
        ("GRID",           (0, 0), (-1, -1), 0.3, C_BORDER),
        ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING",        (0, 0), (-1, -1), 5),
        ("FONTSIZE",       (0, 1), (-1, -1), 8),
    ]))
    story.append(pkt_t)
    story.append(Spacer(1, 0.2*inch))

    story.append(ThickRule(usable_width, thickness=0.5, color=C_BORDER))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("WHAT DID WAVETRACE CAPTURE?", S["section"]))

    concepts = [
        [Paragraph("DNS TRAFFIC",    S["learn_key"]),
         Paragraph(
             "<b>Domain Name System.</b> Your computer converts website names "
             "like google.com into IP addresses. Every time you open a website, "
             "a DNS request is made first. This is completely normal traffic.",
             S["learn_val"])],
        [Paragraph("TLS TRAFFIC",    S["learn_key"]),
         Paragraph(
             "<b>Transport Layer Security.</b> Encrypted HTTPS communication. "
             "Content is fully encrypted and cannot be read by anyone intercepting. "
             "Seeing TLS means your apps are communicating securely.",
             S["learn_val"])],
        [Paragraph("TCP TRAFFIC",    S["learn_key"]),
         Paragraph(
             "<b>Transmission Control Protocol.</b> Foundation of most internet "
             "communication. TCP ensures packets arrive in order and without errors. "
             "SYN/ACK packets are the handshake establishing connections.",
             S["learn_val"])],
        [Paragraph("PACKET LENGTH",  S["learn_key"]),
         Paragraph(
             "<b>Size of each packet in bytes.</b> Small packets under 100 bytes "
             "are control packets — handshakes, acknowledgments. "
             "Large packets 1000+ bytes carry actual data.",
             S["learn_val"])],
        [Paragraph("IP ADDRESS",     S["learn_key"]),
         Paragraph(
             "<b>Unique address identifying every device on a network.</b> "
             "Your IP is your local address assigned by your router. "
             "External IPs belong to servers you are communicating with.",
             S["learn_val"])],
    ]

    col_key = usable_width * 0.18
    col_val = usable_width * 0.82
    ct = Table(concepts, colWidths=[col_key, col_val])
    ct.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (0, -1), C_VIOLET),
        ("TEXTCOLOR",      (0, 0), (0, -1), C_WHITE),
        ("ROWBACKGROUNDS", (1, 0), (1, -1), [C_WHITE, C_MIST]),
        ("GRID",           (0, 0), (-1, -1), 0.4, C_BORDER),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("PADDING",        (0, 0), (-1, -1), 10),
        ("LINEAFTER",      (0, 0), (0, -1), 2, C_TEAL),
    ]))
    story.append(ct)

    story.append(Spacer(1, 0.25*inch))
    story.append(ThickRule(usable_width, thickness=0.5, color=C_BORDER))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "LEGAL DISCLAIMER: WaveTrace is for authorized network analysis only. "
        "Capturing network traffic without explicit permission is illegal. "
        "Only analyze networks you own or have written authorization to test.",
        ParagraphStyle("Disc", fontName="Helvetica", fontSize=7.5,
                       textColor=C_SUBTEXT, leading=12, alignment=TA_CENTER)
    ))

    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    print(f"[✓] Report saved: {output_file}")
