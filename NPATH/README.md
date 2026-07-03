<div align="center">

# 🛡️ NPath — Network Scan Report Generator

**Stop staring at raw NMAP output. Start understanding it.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Tool](https://img.shields.io/badge/Tool-Network%20Scanner-red?style=for-the-badge&logo=linux)](https://github.com/Rishi0cybertech/Pavitra)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()
[![CLI](https://img.shields.io/badge/CLI-Working-success?style=for-the-badge&logo=gnubash)]()
[![Ports](https://img.shields.io/badge/Port%20Intel-18%20Ports-blue?style=for-the-badge)]()

> *"NMAP tells you what ports are open. NPath tells you what that actually means."*

</div>

---

## 📸 Screenshots

### Terminal UI — Real-time Scan Output
![NPath Terminal UI](screenshots/terminal_ui.png)

### PDF Report — Page 1
![NPath PDF Report Page 1](screenshots/report_page1.png)

### PDF Report — Page 2
![NPath PDF Report Page 2](screenshots/report_page2.png)

---

## 🤔 The Problem NPath Solves

When you run NMAP for the first time, you see something like this:

```
PORT     STATE SERVICE VERSION
631/tcp  open  ipp     CUPS 2.4
5432/tcp open  postgresql  9.6.0
```

**Three questions immediately hit you:**
- What is port 631? Should I be scared?
- Who can exploit PostgreSQL on port 5432?
- What do I actually do about this?

NMAP gives you data. **NPath gives you answers.**

---

## ✨ What NPath Does

NPath builds an intelligence layer on top of NMAP, automatically converting raw scan output into a **clean, professional PDF report** that explains every open port in plain English — what it is, why it is dangerous, who exploits it, and exactly how to fix it.

```
You run one command
        ↓
NPath scans the target using NMAP internally
        ↓
Every open port is matched against the intelligence database
        ↓
Risk score calculated automatically
        ↓
A timestamped PDF report is generated with full explanation
        ↓
You actually understand your network
```

---

## 📄 Real Scan Example

Here is what NPath found on `localhost (127.0.0.1)`:

| Port | Service | Severity | Finding |
|------|---------|----------|---------|
| 631/tcp | IPP — Internet Printing Protocol (CUPS 2.4) | 🟢 LOW | Printer sharing service running in background |
| 5432/tcp | PostgreSQL Database | 🔴 CRITICAL | Database server exposed — shut down immediately |

> ✅ After running NPath, PostgreSQL was identified and disabled — open ports reduced from 2 to 1.

---

## 🧠 What The PDF Report Contains

Every generated PDF includes:

### 1. Scan Summary Header
- Target IP and Hostname
- Host State (up/down)
- Total open ports found
- Count of CRITICAL / HIGH / MEDIUM / LOW issues

### 2. Risk Score & Grade
- Overall risk score out of 100
- Grade: A / B / C / D / F
- Risk level: LOW RISK → SEVERE RISK
- Ports sorted by severity — most critical first

### 3. Per-Port Intelligence Section

| Field | What It Tells You |
|-------|------------------|
| **What Is This Port?** | Service name and why it runs |
| **Who Uses It?** | Legitimate users of this port |
| **Who Can Exploit It?** | Attack vectors and threat actors |
| **What Is The Risk?** | Exact impact if compromised |
| **How To Fix It?** | Step-by-step remediation actions |
| **Real World CVE** | Actual vulnerability reference |
| **Version Detected** | Exact software version found |

### 4. Learning Section — How NPath Scanned This Target

| Concept | Explanation |
|---------|------------|
| Command Used | `nmap -sV --open <target>` |
| `-sV` flag | Detects service version behind each port |
| `--open` flag | Shows only open ports, ignores filtered/closed |
| TCP Handshake | SYN → SYN-ACK → ACK explained |
| Port States | Open vs Closed vs Filtered |
| 127.0.0.1 | Loopback address — scanning yourself safely |

---

## 🚀 Installation

### Requirements
- Python 3.10+
- NMAP installed on system
- Linux recommended (Kali, Debian, Ubuntu)

### Step 1 — Clone the repository
```bash
git clone https://github.com/Rishi0cybertech/Pavitra.git
cd Pavitra/NPATH
```

### Step 2 — Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Install NMAP
```bash
sudo apt install nmap        # Debian / Ubuntu / Kali
```

---

## ⚡ Usage

NPath has a fully working CLI. Two ways to run it:

---

### 🖥️ Method 1 — CLI (Recommended)

```bash
# Activate virtual environment first
source venv/bin/activate

# Scan target — terminal output only
python3 npath.py scan 127.0.0.1

# Scan target — generate PDF report
python3 npath.py scan 127.0.0.1 --report

# Scan any IP on your network
python3 npath.py scan 192.168.1.1 --report

# Short flag for report
python3 npath.py scan 192.168.1.1 -r

# Help menu
python3 npath.py --help
```

---

### 📄 Method 2 — Direct Script

```bash
source venv/bin/activate
python3 test_report.py
```

---

### 🖥️ Terminal Output

```
╭──────────────────────────────────────╮
│  NPath Scanner v1.0                  │
│  Target : 127.0.0.1                  │
│  Mode   : Service Detection          │
╰──────────────────────────────────────╯

⠋ Scanning target...
✔ Scan complete!

Host    : 127.0.0.1 (localhost)
State   : up

  PORT 631/tcp  [LOW]  ipp  2.4

[✓] Report saved: npath_report_20260630_090000.pdf
```

---

## 📁 Project Structure

```
NPATH/
├── core/
│   ├── scanner.py        # NMAP wrapper + real-time terminal UI
│   ├── reporter.py       # Professional PDF generator
│   └── analyzer.py       # Risk scoring + port prioritization engine
├── data/
│   └── port_intel.json   # Port knowledge database (18 ports with CVEs)
├── screenshots/
│   ├── terminal_ui.png   # Terminal scan UI preview
│   ├── report_page1.png  # PDF report page 1 preview
│   └── report_page2.png  # PDF report page 2 preview
├── npath.py              # ✅ Working CLI entry point
├── test_report.py        # Direct scan + PDF script
├── requirements.txt      # Python dependencies
└── README.md
```

---

## 🗄️ Port Intelligence Database

NPath maintains a `port_intel.json` database — the brain of the tool.

Current coverage — **18 ports with real CVE references:**

| Port | Service | Severity |
|------|---------|----------|
| 21 | FTP — File Transfer Protocol | 🔴 CRITICAL |
| 22 | SSH — Secure Shell | 🟠 HIGH |
| 23 | Telnet — Unencrypted Remote Access | 🔴 CRITICAL |
| 25 | SMTP — Simple Mail Transfer Protocol | 🟠 HIGH |
| 53 | DNS — Domain Name System | 🟠 HIGH |
| 80 | HTTP — Hypertext Transfer Protocol | 🟡 MEDIUM |
| 110 | POP3 — Post Office Protocol v3 | 🟠 HIGH |
| 139 | NetBIOS — Network Basic Input Output System | 🟡 MEDIUM |
| 143 | IMAP — Internet Message Access Protocol | 🟠 HIGH |
| 443 | HTTPS — HTTP over TLS | 🟢 LOW |
| 445 | SMB — Server Message Block | 🔴 CRITICAL |
| 631 | IPP — Internet Printing Protocol (CUPS) | 🟢 LOW |
| 3306 | MySQL — Database Server | 🔴 CRITICAL |
| 3389 | RDP — Remote Desktop Protocol | 🔴 CRITICAL |
| 5432 | PostgreSQL — Database Server | 🔴 CRITICAL |
| 5900 | VNC — Virtual Network Computing | 🔴 CRITICAL |
| 8080 | HTTP Alternate — Development/Proxy Server | 🟡 MEDIUM |
| 8443 | HTTPS Alternate — Secure Admin Interface | 🟡 MEDIUM |

> Database actively expanding — contributions welcome.

### Database Schema
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

---

## 📦 Dependencies

```
python-nmap     — NMAP Python interface
reportlab       — Professional PDF generation
rich            — Beautiful terminal output
typer           — CLI interface
```

---

## ✅ Completed So Far

- [x] Core scanner with NMAP wrapper
- [x] Professional PDF report generation
- [x] Severity color coding (CRITICAL / HIGH / MEDIUM / LOW)
- [x] Real-time terminal UI with rich
- [x] Port intelligence database with real CVEs
- [x] Learning section in PDF — teaches NMAP concepts
- [x] Unique timestamped PDF per scan
- [x] Working CLI — `python3 npath.py scan <target> --report`
- [x] Port intel database expanded to 18 ports
- [x] Company-grade professional PDF layout
- [x] Risk scoring engine — grade A to F
- [x] Port prioritization — critical ports first

---

## 🗺️ Roadmap — What's Coming Next

- [X] Subnet scanning — `python3 npath.py scan 192.168.1.0/24 --report`
- [ ] OS detection section in report
- [ ] HTML report export option
- [ ] Auto-update CVE database from NVD API
- [ ] Integration with WaveTrace — cross-reference open ports with live traffic
- [ ] DRISHTI AI integration — Hindi + English explanations

---

## ⚠️ Legal Disclaimer

NPath is built strictly for:
- Educational purposes
- Scanning your own machines and networks
- Authorized penetration testing only

**Never scan networks or systems without explicit written permission.**
Unauthorized scanning is illegal under IT Act 2000 (India) and similar laws globally.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

If you find a port that should be in the database — submit it with:
- Port number
- Service name
- Real CVE reference
- Fix steps

---

<div align="center">

**Part of the Pavitra Security Suite.**
**Built by a student, for students.**

⭐ Star this repo if NPath helped you understand your network better.

</div>
