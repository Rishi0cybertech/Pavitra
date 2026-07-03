# Pavitra Brain

Snapshot date: 2026-07-02

This file is a project memory for the current Pavitra workspace. It records what exists right now, what each file contains, how the pieces connect, and important current-state notes for future work.

## Workspace Summary

Root: `/home/rishi/Desktop/Pavitra`

Main projects:

- `NPATH`: Nmap-based network scan report generator.
- `WaveTrace`: TShark/Pyshark-based live packet capture analyzer.

Ignored/generated areas:

- `.git/`: Git repository metadata.
- `venv/`, `NPATH/venv/`: Python virtual environments.
- `*.pdf`: Generated reports, ignored by `.gitignore`.
- `__pycache__/`, `*.pyc`: Python runtime cache files.
- `.env`: ignored local environment file.

Current dirty git status when this memory was made:

```text
 M NPATH/core/reporter.py
 M NPATH/core/scanner.py
 M NPATH/data/port_intel.json
 M WaveTrace/core/analyzer.py
 M WaveTrace/core/reporter.py
 M WaveTrace/data/protocol_intel.json
 M WaveTrace/wavetrace.py
```

## File Inventory

```text
NPATH/README.md
NPATH/requirements.txt
NPATH/npath.py
NPATH/test_report.py
NPATH/core/scanner.py
NPATH/core/analyzer.py
NPATH/core/reporter.py
NPATH/data/port_intel.json
NPATH/screenshots/report_page1.png
NPATH/screenshots/report_page2.png
NPATH/screenshots/terminal_ui.png
NPATH/npath_report_20260702_115110.pdf

WaveTrace/README.md
WaveTrace/requirements.txt
WaveTrace/wavetrace.py
WaveTrace/core/capture.py
WaveTrace/core/analyzer.py
WaveTrace/core/reporter.py
WaveTrace/data/protocol_intel.json
WaveTrace/screenshots/report_page1.png
WaveTrace/screenshots/report_page2.png
WaveTrace/screenshots/terminal_ui_1.png
WaveTrace/screenshots/terminal_ui_2.png
WaveTrace/reports/wavetrace_report_20260630_112830.pdf
WaveTrace/reports/wavetrace_report_20260702_122957.pdf
WaveTrace/reports/wavetrace_report_20260702_124638.pdf

.gitignore
brain.md
```

Binary/generated files are recorded by path and purpose, not embedded as byte content.

## Root Files

### `.gitignore`

Purpose: keeps local/runtime/generated files out of Git.

Current content:

```gitignore
venv/
__pycache__/
*.pyc
*.pdf
.env
```

### `brain.md`

Purpose: this memory file.

## NPATH Project

### Product Identity

NPath is a beginner-friendly network scan report generator. It wraps Nmap, enriches open ports with a local intelligence database, and produces professional PDF reports that explain ports, risks, remediation, and scanning concepts.

Core tagline from README:

```text
NMAP tells you what ports are open. NPath tells you what that actually means.
```

### `NPATH/README.md`

Contains:

- Centered project title: `NPath -- Network Scan Report Generator`.
- Shields for Python, MIT license, network scanner, active status, CLI, and port intel.
- Screenshots:
  - `screenshots/terminal_ui.png`
  - `screenshots/report_page1.png`
  - `screenshots/report_page2.png`
- Problem statement explaining raw Nmap output confusion.
- Product explanation: runs Nmap internally, matches open ports against intelligence DB, calculates risk score, generates timestamped PDF.
- Real scan example with ports `631/tcp` and `5432/tcp`.
- Report contents:
  - Scan summary header.
  - Risk score and grade.
  - Per-port intelligence.
  - Learning section explaining Nmap concepts.
- Installation:
  - Python 3.10+
  - Nmap installed
  - Linux recommended
  - `python3 -m venv venv`
  - `pip install -r requirements.txt`
  - `sudo apt install nmap`
- Usage:
  - `python3 npath.py scan 127.0.0.1`
  - `python3 npath.py scan 127.0.0.1 --report`
  - `python3 npath.py scan 192.168.1.1 --report`
  - `python3 npath.py scan 192.168.1.1 -r`
  - `python3 npath.py --help`
- Project structure block.
- Port intelligence database section.
- Database schema:

```json
{
  "PORT_NUMBER": {
    "service": "Service name",
    "why_open": "Why this port runs",
    "who_uses": "Legitimate users",
    "who_exploits": "Attack vectors",
    "risk": "Impact if compromised",
    "severity": "LOW | MEDIUM | HIGH | CRITICAL",
    "how_to_fix": ["Step 1", "Step 2", "Step 3"],
    "real_world_example": "CVE reference"
  }
}
```

- Dependencies:
  - `python-nmap`
  - `reportlab`
  - `rich`
  - `typer`
- Roadmap completed:
  - Nmap wrapper.
  - PDF report generation.
  - Severity color coding.
  - Rich terminal UI.
  - Port intelligence DB with CVEs.
  - Learning section.
  - Timestamped PDFs.
  - Working CLI.
  - 12-port database.
  - Company-grade PDF layout.
  - Risk scoring engine.
  - Port prioritization.
- Roadmap future:
  - Expand port intel to 20+ ports.
  - Subnet scanning.
  - OS detection.
  - HTML report export.
  - Auto-update CVE database from NVD API.
- Legal disclaimer for authorized use only.
- Contribution guidance for adding ports.

### `NPATH/requirements.txt`

Current content:

```text
python-nmap
reportlab
rich
typer
```

### `NPATH/npath.py`

Purpose: CLI entry point.

Imports:

- `sys`
- `scan_target` from `core.scanner`
- `generate_report` from `core.reporter`
- `datetime`
- `rich.console.Console`
- `rich.panel.Panel`

Current behavior:

- Creates a Rich `Console`.
- `main()` reads `sys.argv[1:]`.
- With no args, `--help`, or `-h`, prints help panel:
  - `python3 npath.py scan [TARGET]`
  - `python3 npath.py scan [TARGET] --report`
- Supports command: `scan`.
- Requires a target argument.
- Detects report mode with `--report` or `-r`.
- Calls `scan_target(target)`.
- If report requested:
  - Creates filename `npath_report_YYYYMMDD_HHMMSS.pdf`.
  - Calls `generate_report(data, filename)`.
- Otherwise prints scan complete and says to use `--report`.
- Unknown commands show an error and help hint.

Important current contract:

- `scan_target()` currently returns a list of host dictionaries.
- `generate_report()` accepts a list and has dict fallback protection.

### `NPATH/test_report.py`

Purpose: direct test script for scanning localhost and generating a PDF.

Current content summary:

- Imports `scan_target`, `generate_report`, `calculate_risk_score`, `prioritize_fixes`, and `datetime`.
- Sets `target = "127.0.0.1"`.
- Calls `data = scan_target(target)`.
- Then treats `data` as a dictionary:
  - `data["risk_analysis"] = calculate_risk_score(data.get("ports", []))`
  - `data["ports"] = prioritize_fixes(data.get("ports", []))`
- Generates timestamped `npath_report_YYYYMMDD_HHMMSS.pdf`.
- Calls `generate_report(data, filename)`.

Known current issue:

- This file is stale relative to `NPATH/core/scanner.py`.
- `scan_target()` now returns a list, but `test_report.py` still treats the result as a dict.

### `NPATH/core/scanner.py`

Purpose: Nmap wrapper and terminal scan UI.

Imports:

- `nmap`
- `json`
- `Path`
- Rich `Console`, `Progress`, `SpinnerColumn`, `TextColumn`, `Panel`

Main functions:

#### `load_intel()`

- Looks for `data/port_intel.json` relative to the current working directory.
- If missing, returns `{}`.
- Otherwise reads JSON and returns the loaded dict.

Important path note:

- Because it uses `Path("data/port_intel.json")`, the script expects to be run from inside `NPATH/`.

#### `scan_target(target: str) -> list`

Current docstring says:

```text
Always returns a LIST of host dicts -- even a single IP scan
returns a one-item list. Callers must not treat this as a dict.
```

Current behavior:

- Creates `nmap.PortScanner()`.
- Loads port intelligence.
- Prints Rich panel:
  - `NPath Scanner v1.0`
  - target
  - mode: service detection
- Runs:

```text
nmap -sV --open
```

through:

```python
nm.scan(hosts=target, arguments="-sV --open")
```

- If no hosts respond, prints an error and returns an empty list.
- For each host:
  - Builds `host_data`:

```python
{
    "ip": host,
    "hostname": nm[host].hostname(),
    "state": nm[host].state(),
    "ports": []
}
```

  - Prints host and state.
  - Iterates protocols and ports.
  - For each service:
    - Pulls intel from `port_intel.json` using string port number.
    - Uses fallback intel if port is missing:
      - service name from Nmap
      - why open: no data available
      - who uses: N/A
      - who exploits: research manually
      - risk: unknown investigate
      - severity: MEDIUM
      - how to fix: research manually
      - real world example: N/A
    - Prints one line with port, severity, service, and version.
    - Appends port data:

```python
{
    "port": port,
    "protocol": proto,
    "state": service["state"],
    "service": service["name"],
    "version": service.get("version", "Unknown"),
    "intel": intel_data
}
```

- Prints total hosts scanned.
- Returns `all_hosts`.

Severity terminal colors:

```python
{
    "CRITICAL": "red",
    "HIGH": "orange1",
    "MEDIUM": "yellow",
    "LOW": "green"
}
```

### `NPATH/core/analyzer.py`

Purpose: risk scoring and port prioritization.

Imports:

- `List`
- `Dict`

Risk weights:

```python
SEVERITY_SCORES = {
    "CRITICAL": 10,
    "HIGH":     7,
    "MEDIUM":   4,
    "LOW":      1,
}
```

#### `calculate_risk_score(ports: List[Dict]) -> Dict`

Behavior:

- If no ports:
  - score `100`
  - risk level `SECURE`
  - grade `A`
  - summary: no open ports detected
- Otherwise:
  - Computes total possible weight as sum of all severity scores times number of ports.
  - Computes actual weight from each port's `intel.severity`.
  - Converts to inverse score out of 100.
  - Grades:
    - `>= 90`: A / LOW RISK
    - `>= 75`: B / MODERATE RISK
    - `>= 50`: C / HIGH RISK
    - `>= 25`: D / CRITICAL RISK
    - else: F / SEVERE RISK
  - Counts critical/high/medium/low.
  - Builds summary like:

```text
Found N open ports with X critical issues, Y high severity issues...
```

Returns:

```python
{
    "score": raw_score,
    "risk_level": risk_level,
    "grade": grade,
    "summary": summary,
    "breakdown": {
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
    }
}
```

#### `prioritize_fixes(ports: List[Dict]) -> List[Dict]`

- Sorts ports by severity order:
  - CRITICAL
  - HIGH
  - MEDIUM
  - LOW

### `NPATH/core/reporter.py`

Purpose: professional PDF generator for NPath.

Major imports:

- ReportLab A4, colors, styles, platypus elements, units, enums.
- `datetime`.

Color palette:

- Navy/slate/steel base:
  - `C_NAVY = #0D1B2A`
  - `C_SLATE = #1B2838`
  - `C_STEEL = #2E4057`
- Neutral:
  - `C_MIST = #F4F6F8`
  - `C_WHITE = #FFFFFF`
  - `C_BORDER = #D0D7DE`
  - `C_TEXT = #1C2833`
  - `C_SUBTEXT = #5D6D7E`
- Severity:
  - CRITICAL `#B71C1C`
  - HIGH `#BF360C`
  - MEDIUM `#E65100`
  - LOW `#1B5E20`
- Severity backgrounds:
  - CRITICAL `#FFEBEE`
  - HIGH `#FBE9E7`
  - MEDIUM `#FFF8E1`
  - LOW `#E8F5E9`

Global page values:

- `PAGE_W = A4[0]`
- `PAGE_H = A4[1]`
- `MARGIN = 0.75 * inch`

Main classes/functions:

#### `ThickRule`

- Custom ReportLab `Flowable`.
- Draws a horizontal line with given width, thickness, and color.

#### `build_styles()`

Returns:

```python
S, base, usable_width
```

Defines paragraph styles:

- `report_title`
- `report_subtitle`
- `section_label`
- `port_title`
- `severity_label`
- `field_key`
- `field_value`
- `fix_step`
- `learn_header`
- `learn_key`
- `learn_val`
- `footer_text`
- `summary_key`
- `summary_val`
- `severity_count`
- `severity_count_label`

#### `build_severity_summary(severities, styles, usable_width)`

- Counts CRITICAL/HIGH/MEDIUM/LOW.
- Creates a four-column severity summary table.
- Uses colored backgrounds and top lines.

#### `build_scan_summary(host_data, styles, usable_width, host_index=None, total_hosts=None)`

- Builds target/host summary table.
- Fields:
  - Target IP
  - Hostname
  - Host state
  - Open ports
  - Scan engine
  - Scan mode
- If multiple hosts, labels target as `TARGET IP (idx/total)`.

#### `build_subnet_overview(all_hosts, styles, usable_width)`

- Creates overview table for multiple hosts.
- Columns:
  - HOST
  - STATE
  - OPEN PORTS
  - HIGHEST SEVERITY
- Computes worst severity using rank:
  - CRITICAL 4
  - HIGH 3
  - MEDIUM 2
  - LOW 1

#### `build_port_section(port_info, styles, usable_width)`

- Builds a full intelligence section for one open port.
- Header:
  - `PORT <port>/TCP -- <SERVICE>`
  - right side version detected
- Severity badge:
  - `SEVERITY: <severity>`
  - severity description
- Detail rows:
  - WHAT IS THIS PORT?
  - WHO USES IT?
  - WHO EXPLOITS IT?
  - RISK IMPACT
  - REMEDIATION STEPS
  - CVE REFERENCE
- Remediation steps are numbered with `<b>1.</b> ...<br/>`.
- Returns a `KeepTogether`.

#### `_severity_description(severity)`

Descriptions:

- CRITICAL: immediate action required, high probability of exploitation.
- HIGH: address within 24 hours.
- MEDIUM: schedule remediation.
- LOW: monitor and review.

#### `build_learning_section(scan_data, styles, usable_width)`

Creates the educational reference section titled:

```text
HOW NPATH SCANNED THIS TARGET
```

Concept rows:

- COMMAND ISSUED: `nmap -sV --open <ip>`
- `-sV FLAG`
- `--OPEN FLAG`
- TCP HANDSHAKE
- LOOPBACK ADDRESS
- WHAT IS A PORT?

#### `_on_page(canvas, doc)`

Adds every-page styling:

- Top navy strip.
- Footer:

```text
NPath v1.0 | Confidential Scan Report | Page <n> | Generated <timestamp> | github.com/Rishi0cybertech/Pavitra
```

- Bottom divider line.

#### `generate_report(scan_data, output_file="npath_report.pdf")`

Current data contract:

- Expects `scan_data` to be a list of host dicts.
- Has fallback: if a dict is provided, wraps it in a list.
- If empty list, prints no-hosts message and returns.

Main PDF flow:

1. Title: `NPath`.
2. Subtitle:
   - `Network Vulnerability Scan Report` for one host.
   - `Subnet Vulnerability Scan Report -- N Hosts` for multiple hosts.
3. Generated date/time/classification/tool line.
4. If multiple hosts:
   - `SUBNET OVERVIEW`.
5. `SEVERITY OVERVIEW -- ALL HOSTS`.
6. For each host:
   - Page break between hosts.
   - `SCAN SUMMARY` or `HOST X OF N`.
   - Scan summary table.
   - If open ports:
     - `PORT INTELLIGENCE REPORT`.
     - One port intelligence section per port.
   - Else: no open ports message.
7. `EDUCATIONAL REFERENCE`.
8. Legal disclaimer.
9. Builds PDF with `_on_page`.
10. Prints saved path.

Important note:

- `generate_report()` does not currently calculate risk score itself.
- It shows severity overview and port intelligence, but no separate risk grade card in current file.

### `NPATH/data/port_intel.json`

Purpose: local port intelligence database used by `scanner.py`.

Current schema per port:

- `service`
- `why_open`
- `who_uses`
- `who_exploits`
- `risk`
- `severity`
- `how_to_fix`
- `real_world_example`

Current ports present:

```text
21   FTP -- File Transfer Protocol                  CRITICAL
22   SSH -- Secure Shell                            HIGH
23   Telnet -- Unencrypted Remote Access            CRITICAL
25   SMTP -- Simple Mail Transfer Protocol          HIGH
53   DNS -- Domain Name System                      MEDIUM
80   HTTP -- Hypertext Transfer Protocol            MEDIUM
161  SNMP -- Simple Network Management Protocol     HIGH
443  HTTPS -- HTTP over TLS                         LOW
445  SMB -- Server Message Block                    CRITICAL
631  IPP -- Internet Printing Protocol (CUPS)       LOW
3306 MySQL -- Database Server                       CRITICAL
3389 RDP -- Remote Desktop Protocol                 CRITICAL
5432 PostgreSQL -- Database Server                  CRITICAL
8080 HTTP Alternate -- Development/Proxy Web Server MEDIUM
```

Notable CVE examples recorded:

- SSH: CVE-2018-15473
- FTP: CVE-2011-2523
- Telnet: CVE-2020-10188
- SMTP: CVE-2020-7247
- HTTP: CVE-2021-41773
- HTTPS/OpenSSL: CVE-2014-0160 Heartbleed
- MySQL: CVE-2012-2122
- PostgreSQL: CVE-2019-9193
- CUPS/IPP: CVE-2023-32360
- RDP: CVE-2019-0708 BlueKeep
- SMB: CVE-2017-0144 EternalBlue
- HTTP alternate/Tomcat: CVE-2020-1938 Ghostcat
- DNS: CVE-2020-1350 SIGRed
- SNMP: CVE-2017-7921

Important current note:

- README still says 12 ports, but the JSON currently contains 14 port entries.

### NPATH Binary/Generated Assets

```text
NPATH/screenshots/report_page1.png       126805 bytes
NPATH/screenshots/report_page2.png       138679 bytes
NPATH/screenshots/terminal_ui.png        197163 bytes
NPATH/npath_report_20260702_115110.pdf     7786 bytes
```

These are not embedded in this Markdown because they are binary/generated artifacts.

## WaveTrace Project

### Product Identity

WaveTrace is a beginner-friendly network packet analyzer. It captures live packets through TShark/Pyshark, classifies protocols, flags suspicious ports, enriches protocols with intelligence, calculates session risk, and generates a professional PDF report.

Core tagline from README:

```text
Wireshark shows you packets. WaveTrace tells you what they mean.
```

### `WaveTrace/README.md`

Contains:

- Centered project title: `WaveTrace -- Network Packet Analyzer`.
- Shields for Python, MIT license, packet analyzer, in-development status, and TShark/Pyshark engine.
- Screenshots:
  - `screenshots/terminal_ui_1.png`
  - `screenshots/terminal_ui_2.png`
  - `screenshots/report_page1.png`
  - `screenshots/report_page2.png`
- Problem statement explaining that Wireshark can overwhelm beginners.
- Product explanation:
  - Select network interface.
  - Capture live packets via TShark.
  - Classify packet protocol/source/destination/risk.
  - Flag suspicious traffic.
  - Generate PDF report.
- Real capture example:
  - 15 packets.
  - 3 protocols: DNS, TCP, TLS.
  - 4 unique sources.
  - 0 suspicious traffic.
- PDF report contents:
  - Capture summary.
  - Protocol breakdown.
  - Suspicious traffic detection.
  - Full packet log.
  - Educational reference.
- Installation:
  - Python 3.10+
  - TShark
  - Linux recommended
  - Root/sudo for packet capture
  - `python3 -m venv venv`
  - `pip install -r requirements.txt`
  - `sudo apt install tshark -y`
- Usage:
  - `sudo venv/bin/python3 wavetrace.py`
- Interactive flow:
  - Select interface.
  - Choose packet count.
  - Live capture with table.
  - Capture summary.
  - Choose PDF generation.
- Project structure block.
- Dependencies:
  - `pyshark`
  - `scapy`
  - `reportlab`
  - `rich`
  - `psutil`
- Completed so far:
  - Interface detection.
  - Live packet capture.
  - Rich live table.
  - Protocol classification.
  - Suspicious port detection.
  - PDF report generation.
  - Protocol breakdown with risk levels.
  - Full packet log.
  - Educational reference.
  - Distinct purple/teal visual identity.
- Roadmap:
  - Full protocol knowledge DB with CVEs.
  - HTTP/HTTPS payload inspection where legal.
  - Bandwidth graphs.
  - Top talkers.
  - PCAP import.
  - Capture comparison.
  - JSON export.
  - ARP spoofing detection.
  - DNS tunneling detection.
  - Port scan detection.
  - NPath integration.
  - Web dashboard.
  - DRISHTI AI integration.
  - NETRA Labs integration.
- Legal disclaimer and contribution guidance.

### `WaveTrace/requirements.txt`

Current content:

```text
scapy
pyshark
reportlab
rich
psutil
```

### `WaveTrace/wavetrace.py`

Purpose: CLI entry point for live packet capture.

Imports:

- `sys`
- Rich `Console`, `Panel`, `Prompt`, `IntPrompt`, `box`
- `display_interfaces`, `capture_packets`
- `generate_report`
- `enrich_protocols`, `calculate_session_risk`
- `datetime`

Main behavior:

#### `show_banner()`

- Prints a large ASCII-art `WAVETRACE` banner in a cyan double-edge Rich panel.
- Subtitle:

```text
Network Packet Analyzer -- Part of Pavitra Security Suite
Built by Rishi Gauttam | github.com/Rishi0cybertech
```

#### `main()`

Flow:

1. Shows banner.
2. Prints `STEP 1 -- Select a network interface`.
3. Calls `display_interfaces()`.
4. Asks interface number with default `1`.
5. Validates selected number.
6. Prints selected interface.
7. Asks packet count with default `50`.
8. Calls:

```python
stats = capture_packets(interface=selected, packet_count=count)
```

9. Adds:

```python
stats["interface"] = selected
```

10. Enrichment and risk layer:

```python
stats["enriched_protocols"] = enrich_protocols(stats["protocols"])
stats["risk_analysis"] = calculate_session_risk(
    stats["enriched_protocols"],
    suspicious_count=len(stats.get("suspicious", []))
)
```

11. Prints session risk:

```text
Session Risk: <grade> -- <risk_level> (<score>/100)
<summary>
```

12. Asks whether to generate PDF.
13. If yes:
    - Saves to `reports/wavetrace_report_YYYYMMDD_HHMMSS.pdf`.
    - Calls `generate_report(stats, filename)`.
14. Else prints report skipped.

### `WaveTrace/core/capture.py`

Purpose: interface detection, live packet capture, terminal table, suspicious port flagging.

Imports:

- `pyshark`
- `psutil`
- Rich `Console`, `Table`, `Panel`, `Live`, `Layout`, `Text`, `box`
- `defaultdict`
- `datetime`

Note:

- `Layout` and `Text` are currently imported but not used.

#### `get_interfaces()`

- Uses `psutil.net_if_addrs().items()`.
- Returns a list of interface names.

#### `display_interfaces()`

- Gets interfaces.
- Builds Rich table:
  - Title: `Available Network Interfaces`
  - double-edge box
  - columns: No., Interface, Status
- Status uses `psutil.net_if_stats()`:
  - UP in green
  - DOWN in red
- Prints table and returns interface list.

#### `capture_packets(interface: str, packet_count: int = 50) -> list`

Docstring says it captures packets and returns analyzed data.

Important note:

- Type hint currently says `-> list`, but function returns a stats dictionary.

Initial `stats` shape:

```python
{
    "total": 0,
    "protocols": defaultdict(int),
    "src_ips": defaultdict(int),
    "dst_ips": defaultdict(int),
    "suspicious": [],
    "packets": [],
    "start_time": "<timestamp>",
}
```

Suspicious ports map:

```python
{
    23: "Telnet -- Unencrypted",
    21: "FTP -- Cleartext",
    4444: "Metasploit Default",
    1337: "Hacker Port",
    31337: "Elite Hacker Port",
    6667: "IRC -- Botnet C2",
    9001: "Tor Default",
}
```

Capture flow:

- Prints capture panel showing interface, count, and start time.
- Creates a Rich live table with columns:
  - `#`
  - `TIME`
  - `PROTOCOL`
  - `SOURCE`
  - `DEST`
  - `LENGTH`
  - `STATUS`
- Uses:

```python
pyshark.LiveCapture(interface=interface)
```

- Iterates `capture.sniff_continuously()`.
- Stops after requested packet count.
- For each packet:
  - `proto = packet.highest_layer`
  - gets `src_ip`/`dst_ip` from `packet.ip` if present, else `N/A`
  - `length = packet.length`
  - `time = datetime.now().strftime("%H:%M:%S")`
  - increments protocol/source/destination counters
  - checks TCP source/destination ports against suspicious map
  - appends suspicious entries if matched:

```python
{
    "packet": count,
    "src": src_ip,
    "dst": dst_ip,
    "port": port,
    "reason": reason
}
```

  - appends packet log rows:

```python
{
    "num": count,
    "time": time,
    "protocol": proto,
    "src": src_ip,
    "dst": dst_ip,
    "length": length,
    "suspicious": is_suspicious
}
```

- On exception, prints capture error.
- After capture, prints capture summary panel.
- Adds `end_time`.
- Returns `stats`.

### `WaveTrace/core/analyzer.py`

Purpose: protocol intelligence enrichment and session risk scoring.

Imports:

- `List`, `Dict`
- `Path`
- `json`

Risk weights:

```python
SEVERITY_SCORES = {
    "CRITICAL": 10,
    "HIGH":     7,
    "MEDIUM":   4,
    "LOW":      1,
}
```

#### `load_protocol_intel()`

- Looks for `data/protocol_intel.json` relative to current working directory.
- If missing, returns `{}`.
- Otherwise reads JSON.

Important path note:

- Like NPATH, this expects the app to be run from inside `WaveTrace/`.

#### `enrich_protocols(protocols: dict) -> dict`

Input:

- Raw protocol counter from `capture.py` stats, usually `stats["protocols"]`.

Output shape:

```python
{
    "PROTOCOL_NAME": {
        "count": int,
        "intel": {...}
    }
}
```

Behavior:

- Loads protocol intel DB.
- Uses uppercase protocol key.
- Fallback intel:
  - protocol name is raw protocol
  - no intelligence data available
  - who uses N/A
  - who exploits research manually
  - risk unknown investigate
  - severity MEDIUM
  - red flags manual review recommended
  - real world example N/A

#### `calculate_session_risk(enriched_protocols: dict, suspicious_count: int) -> dict`

Behavior:

- If no protocols:
  - score 100
  - risk level SECURE
  - grade A
  - summary no traffic captured
- Otherwise:
  - Calculates total packets.
  - Computes weighted risk by protocol severity times packet count.
  - Computes base score as inverse risk.
  - Applies suspicious penalty:

```python
suspicious_penalty = min(suspicious_count * 15, 60)
```

  - Final score = base score minus penalty.
  - Grades:
    - `>= 90`: A / LOW RISK
    - `>= 75`: B / MODERATE RISK
    - `>= 50`: C / HIGH RISK
    - `>= 25`: D / CRITICAL RISK
    - else: F / SEVERE RISK
  - Summary includes:
    - number of protocols observed
    - suspicious packets if any
    - critical-severity protocol count if any
    - high-severity protocol count if any

#### `prioritize_protocols(enriched_protocols: dict) -> list`

- Sorts protocol items by severity:
  - CRITICAL
  - HIGH
  - MEDIUM
  - LOW

### `WaveTrace/core/reporter.py`

Purpose: professional PDF report generator for WaveTrace.

Major imports:

- ReportLab A4, colors, paragraph styles, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, units, enums, Flowable.
- `datetime`.

Unused imports currently present:

- `getSampleStyleSheet`
- `TA_RIGHT`

Color palette:

- `C_DARK = #0A0E1A`
- `C_PURPLE = #1A1040`
- `C_VIOLET = #2D1B69`
- `C_TEAL = #0D7377`
- `C_MIST = #F0F4F8`
- `C_WHITE = #FFFFFF`
- `C_BORDER = #C8D0E0`
- `C_TEXT = #1A1A2E`
- `C_SUBTEXT = #6B7280`
- `C_SAFE = #065F46`
- `C_SAFE_BG = #ECFDF5`
- `C_WARN = #92400E`
- `C_WARN_BG = #FFFBEB`
- `C_DANGER = #991B1B`
- `C_DANGER_BG = #FEF2F2`

Global page values:

- `PAGE_W = A4[0]`
- `MARGIN = 0.75 * inch`

#### `ThickRule`

- Custom ReportLab horizontal rule flowable.

#### `build_styles()`

Returns:

```python
S, usable_width
```

Styles:

- `title`
- `subtitle`
- `section`
- `key`
- `val`
- `learn_key`
- `learn_val`
- `packet_row`

#### `_on_page(canvas, doc)`

Adds:

- Top teal strip.
- Footer:

```text
WaveTrace v1.0 | Network Analysis Report | Page <n> | Generated <timestamp> | github.com/Rishi0cybertech/Pavitra
```

- Bottom divider line.

#### `generate_report(stats: dict, output_file="wavetrace_report.pdf")`

Main PDF flow:

1. Title: `WaveTrace`.
2. Subtitle: `Network Packet Analysis Report`.
3. Capture metadata:
   - captured date
   - `stats["start_time"]`
   - interface
   - tool version
4. `CAPTURE SUMMARY`.
5. `PROTOCOL BREAKDOWN`.
6. `PROTOCOL INTELLIGENCE`.
7. Optional `SUSPICIOUS TRAFFIC DETECTED`.
8. `PACKET CAPTURE LOG`.
9. `WHAT DID WAVETRACE CAPTURE?`.
10. Legal disclaimer.
11. Builds PDF and prints saved path.

Current stats used:

```python
packets    = stats.get("packets", [])
protocols  = stats.get("protocols", {})
suspicious = stats.get("suspicious", [])
enriched   = stats.get("enriched_protocols", {})
total      = max(stats.get("total", 1), 1)
```

Capture summary rows:

- INTERFACE / START TIME
- TOTAL PACKETS / END TIME
- PROTOCOLS SEEN / SUSPICIOUS
- UNIQUE SOURCES / UNIQUE DESTS

Current protocol breakdown logic:

- Uses `stats["enriched_protocols"]`, not a hardcoded `PROTO_RISK` dict.
- Sorts protocols by count descending:

```python
sorted_protos = sorted(enriched.items(), key=lambda x: x[1]["count"], reverse=True)
```

- Severity display colors:

```python
SEVERITY_DISPLAY_COLOR = {
    "CRITICAL": C_DANGER,
    "HIGH":     C_DANGER,
    "MEDIUM":   C_WARN,
    "LOW":      C_SAFE,
}
```

- Breakdown columns:
  - PROTOCOL
  - PACKETS
  - SHARE
  - RISK

Current protocol intelligence detail section:

- Added after protocol breakdown.
- For every sorted protocol:
  - `proto -- protocol_name`
  - WHY SEEN
  - WHO USES IT
  - WHO EXPLOITS IT
  - RISK
  - RED FLAGS TO WATCH
  - REAL WORLD EXAMPLE
- Uses protocol severity color as the detail header background.
- Uses `KeepTogether([dt, Spacer(...)])`.
- Default red flags:

```text
No known red flags on file
```

Suspicious traffic section:

- Only appears if `stats["suspicious"]` has entries.
- Columns:
  - PKT #
  - SOURCE
  - DEST
  - PORT
  - REASON

Packet log section:

- Columns:
  - #
  - TIME
  - PROTOCOL
  - SOURCE
  - DEST
  - LENGTH
  - STATUS
- Status is `SUSPICIOUS` or `NORMAL`.

Educational section concepts:

- DNS TRAFFIC
- TLS TRAFFIC
- TCP TRAFFIC
- PACKET LENGTH
- IP ADDRESS

Recent verified behavior:

- `python3 -m py_compile WaveTrace/core/reporter.py` passed.
- A mock PDF generation using enriched protocol data succeeded at `/tmp/wavetrace_sample.pdf`.

Important current note:

- The hardcoded local `PROTO_RISK` dictionary has been removed.
- Report now depends on `stats["enriched_protocols"]` for protocol risk.

### `WaveTrace/data/protocol_intel.json`

Purpose: local protocol intelligence database used by `WaveTrace/core/analyzer.py`.

Current schema per protocol:

- `protocol_name`
- `why_seen`
- `who_uses`
- `who_exploits`
- `risk`
- `severity`
- `red_flags`
- `real_world_example`

Current protocol entries:

```text
DNS     LOW
TLS     LOW
TCP     LOW
HTTP    MEDIUM
TELNET  CRITICAL
FTP     HIGH
UDP     LOW
ICMP    LOW
NTP     LOW
ARP     MEDIUM
```

Key intelligence notes:

- DNS:
  - Normal name resolution.
  - Abuse: DNS tunneling, spoofing.
  - Red flags: long domains, high query frequency, malicious/DGA domains.
  - Example: DNSMessenger.
- TLS:
  - Encrypted HTTPS foundation.
  - Abuse/risk: old TLS versions, weak ciphers.
  - Example: CVE-2014-3566 POODLE.
- TCP:
  - Reliable transport foundation.
  - Abuse: scans, SYN floods, hijacking.
  - Red flags: many SYNs, RST repeats, half-open connections.
- HTTP:
  - Plain web traffic.
  - Risk: plaintext credentials/tokens/content.
  - Example: Firesheep session hijacking.
- TELNET:
  - Legacy unencrypted remote access.
  - Severity CRITICAL.
  - Example: Mirai botnet.
- FTP:
  - Unencrypted file transfer.
  - Severity HIGH.
  - Example: CVE-2011-2523 vsftpd backdoor.
- UDP:
  - Connectionless speed-priority traffic.
  - Abuse: amplification DDoS.
  - Example: 2018 GitHub memcached amplification DDoS.
- ICMP:
  - Diagnostics: ping/traceroute/errors.
  - Abuse: tunneling/flooding.
  - Example: Loki ICMP tunneling.
- NTP:
  - Time sync.
  - Abuse: amplification DDoS.
  - Example: 2014 NTP amplification attacks.
- ARP:
  - IP-to-MAC mapping on local network.
  - No IP layer, so source/destination may be N/A.
  - Abuse: ARP spoofing/poisoning, MITM.
  - Example: Ettercap/Bettercap style MITM.

### WaveTrace Binary/Generated Assets

```text
WaveTrace/screenshots/report_page1.png                         128798 bytes
WaveTrace/screenshots/report_page2.png                         140614 bytes
WaveTrace/screenshots/terminal_ui_1.png                         76236 bytes
WaveTrace/screenshots/terminal_ui_2.png                        142738 bytes
WaveTrace/reports/wavetrace_report_20260630_112830.pdf           6163 bytes
WaveTrace/reports/wavetrace_report_20260702_122957.pdf           6662 bytes
WaveTrace/reports/wavetrace_report_20260702_124638.pdf          10288 bytes
```

These are not embedded in this Markdown because they are binary/generated artifacts.

## Cross-Project Patterns

Both projects follow the same Pavitra style:

- Beginner-friendly security tooling.
- Terminal-first UX using Rich.
- Local JSON intelligence database.
- PDF reporting using ReportLab.
- Educational explanations inside reports.
- Legal disclaimers emphasizing authorized use only.

Shared design idea:

```text
Raw security tool output -> intelligence enrichment -> human-readable report -> learning layer
```

## Important Data Contracts

### NPATH scan data

Current scanner output:

```python
[
    {
        "ip": "127.0.0.1",
        "hostname": "localhost",
        "state": "up",
        "ports": [
            {
                "port": 631,
                "protocol": "tcp",
                "state": "open",
                "service": "ipp",
                "version": "2.4",
                "intel": {...}
            }
        ]
    }
]
```

### WaveTrace capture stats

Current capture output after `wavetrace.py` enriches it:

```python
{
    "total": 50,
    "protocols": {"DNS": 10, "TCP": 20},
    "src_ips": {"192.168.1.10": 15},
    "dst_ips": {"8.8.8.8": 5},
    "suspicious": [
        {
            "packet": 3,
            "src": "192.168.1.10",
            "dst": "10.0.0.5",
            "port": 23,
            "reason": "Telnet -- Unencrypted"
        }
    ],
    "packets": [
        {
            "num": 1,
            "time": "10:00:00",
            "protocol": "DNS",
            "src": "192.168.1.10",
            "dst": "8.8.8.8",
            "length": "64",
            "suspicious": False
        }
    ],
    "start_time": "YYYY-MM-DD HH:MM:SS",
    "end_time": "YYYY-MM-DD HH:MM:SS",
    "interface": "eth0",
    "enriched_protocols": {
        "DNS": {
            "count": 10,
            "intel": {...}
        }
    },
    "risk_analysis": {
        "score": 90,
        "risk_level": "LOW RISK",
        "grade": "A",
        "summary": "..."
    }
}
```

## Current Known Issues / Cleanup Ideas

- `NPATH/test_report.py` is stale and likely broken because it treats list scan data as a dict.
- `NPATH/README.md` says the port DB has 12 ports, but `port_intel.json` currently has 14.
- `WaveTrace/core/capture.py` type hint says `capture_packets(...) -> list`, but it returns a dict.
- `WaveTrace/core/capture.py` imports `Layout` and `Text` but does not use them.
- `WaveTrace/core/reporter.py` imports `getSampleStyleSheet` and `TA_RIGHT` but does not use them.
- `WaveTrace/core/reporter.py` uses `stats["enriched_protocols"]`; if callers skip enrichment, the protocol breakdown table will be empty even if `stats["protocols"]` exists.
- Both analyzer files load JSON using relative paths like `Path("data/...")`, so running from the wrong working directory can make intelligence loading silently return `{}`.

## Recent Work Remembered

- In `WaveTrace/core/reporter.py`, the hardcoded `PROTO_RISK` dictionary was deleted.
- `PROTOCOL BREAKDOWN` now uses `stats.get("enriched_protocols", {})`.
- A severity color map was added inside `generate_report()`.
- A new `PROTOCOL INTELLIGENCE` section was added after the breakdown.
- The new detail section includes:
  - WHY SEEN
  - WHO USES IT
  - WHO EXPLOITS IT
  - RISK
  - RED FLAGS TO WATCH
  - REAL WORLD EXAMPLE
- Syntax was verified with:

```bash
python3 -m py_compile WaveTrace/core/reporter.py
```

- Mock PDF generation was verified with enriched data and saved to:

```text
/tmp/wavetrace_sample.pdf
```

