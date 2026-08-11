<div align="center">

# 🛡️ Pavitra

**A cybersecurity suite that scans, captures, and lets you practice — built to make security learning make sense.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-00C853?style=for-the-badge)](LICENSE)
[![Tools](https://img.shields.io/badge/Tools-3-8E24AA?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Active%20Development-FFD600?style=for-the-badge)]()

</div>

---

## 🎯 The Idea

Professional security tools — NMAP, Wireshark — are powerful and genuinely difficult to learn from. Their output assumes you already know what you're looking at. Pavitra exists to close that gap: scan your network, understand your traffic, and practice real attacks — all explained in plain language, with the mechanism behind every finding, not just the finding itself.

```
Scan it  →  NPath
Understand it  →  WaveTrace
Practice it  →  NETRA
```

Each tool works standalone. Together, they close a loop most security learning never closes: find a vulnerability class in NETRA, then independently confirm the same finding by scanning with NPath or capturing its traffic with WaveTrace.

---

## 🔍 NPath — Network Scan Intelligence

Wraps NMAP and turns raw port-scan output into a professional report — what's open, why it matters, who exploits it, and exactly how to fix it. 19-port intelligence database, real CVE references, risk scoring from A to F, verified multi-host subnet scanning.

```bash
python3 npath.py scan 192.168.1.0/24 --report
```

**[→ Full NPath documentation](NPATH/README.md)**

---

## 🌊 WaveTrace — Network Packet Analyzer

Captures live traffic via TShark and explains what it means, not just what it is. Protocol-level intelligence for DNS, TLS, TCP, HTTP, Telnet, FTP, UDP, ICMP, NTP, and ARP — each with real-world abuse examples and red flags to watch for. Session-level risk scoring on every capture.

```bash
sudo venv/bin/python3 wavetrace.py
```

**[→ Full WaveTrace documentation](WaveTrace/README.md)**

---

## 🎯 NETRA — Virtual Attack Labs

Six isolated, deliberately vulnerable environments for hands-on practice — from OWASP Top 10 web vulnerabilities to a fully original command injection app built from scratch. Every lab runs in its own Docker container, reachable only from `localhost`.

```bash
python3 netra.py
```

**[→ Full NETRA documentation](Netra/README.md)**

---

## 🚀 Getting Started

Each tool has its own virtual environment and dependencies — set up whichever you need:

```bash
git clone https://github.com/Rishi0cybertech/Pavitra.git
cd Pavitra

# NPath
cd NPATH && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# WaveTrace
cd ../WaveTrace && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# NETRA
cd ../Netra && python3 -m venv venv && source venv/bin/activate && pip install flask redis paramiko rich
```

---

## 🧩 How They Connect

A single walkthrough across all three tools:

1. **NETRA** — practice exploiting an exposed FTP server with anonymous login, watch the real attack stream live in the browser
2. **NPath** — scan the same host, watch port 21 get flagged CRITICAL with the exact CVE and remediation steps
3. **WaveTrace** — capture the network traffic during the exploit, see the plaintext FTP credentials pass across the wire in real time

Same vulnerability, three angles: exploit it, detect it, watch it happen on the wire.

---

## 📁 Repository Structure

```
Pavitra/
├── NPATH/       # Network scanner + PDF intelligence reports
├── WaveTrace/   # Live packet capture + protocol intelligence
├── Netra/       # Virtual attack labs, 6 environments
└── README.md    # This file
```

---

## ⚠️ Legal Disclaimer

Every tool in Pavitra is built for authorized use only — your own systems, your own networks, or explicit written permission. NETRA's labs run isolated on `localhost` and are never reachable externally. Unauthorized scanning, capture, or exploitation is illegal under the IT Act 2000 (India) and equivalent legislation elsewhere. These tools teach; they don't grant permission.

---

## 🤝 Contributing

Each sub-project accepts contributions independently — see the individual READMEs for how to add ports, protocols, or labs.

---

<div align="center">

**Built by a student, for students.**

⭐ Star this repo if any part of Pavitra helped you understand something you were stuck on.

</div>
