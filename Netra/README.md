<div align="center">

# 🎯 NETRA — Virtual Attack Labs

**Practice real exploits. Isolated environments. Zero risk to real systems.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Isolated-2496ED?style=for-the-badge&logo=docker&logoColor=white)]()
[![Labs](https://img.shields.io/badge/Labs-6-D946EF?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Active-00E676?style=for-the-badge)]()

*Part of the Pavitra Security Suite*

</div>

---

## 🤔 What Is NETRA?

NETRA is a set of isolated, deliberately vulnerable environments for hands-on cybersecurity practice. Every lab runs in its own Docker container — fully cut off from your host machine and from every other lab — so mistakes cost nothing and experimentation is safe.

This isn't a slide deck about vulnerabilities. You perform the actual attack, see the actual result, and understand why the misconfiguration matters — the same way you'd encounter it on a real network.

---

## 🧪 The Labs

<table>
<tr><th>#</th><th>Lab</th><th>Category</th><th>Access</th><th>Origin</th></tr>
<tr><td>1</td><td><b>Juice Shop</b></td><td>OWASP Top 10 — modern web app vulns</td><td><code>:3000</code></td><td>Industry-standard image</td></tr>
<tr><td>2</td><td><b>DVWA</b></td><td>Classic SQLi / XSS / Command Injection</td><td><code>:8081</code></td><td>Industry-standard image</td></tr>
<tr><td>3</td><td><b>Anonymous FTP</b></td><td>Unauthenticated file access</td><td><code>:5001</code></td><td>Custom-built NETRA GUI</td></tr>
<tr><td>4</td><td><b>Open Redis</b></td><td>Unauthenticated database access</td><td><code>:5002</code></td><td>Custom-built NETRA GUI</td></tr>
<tr><td>5</td><td><b>SSH Brute Force</b></td><td>Weak credential exploitation</td><td><code>:5003</code></td><td>Custom-built, live SSE streaming</td></tr>
<tr><td>6</td><td><b>Command Injection</b></td><td>Unsanitized shell input (CWE-78)</td><td><code>:5004</code></td><td>Fully original vulnerable app</td></tr>
</table>

**Honest attribution:** Labs 1–2 run proven, industry-standard vulnerable images used across the security training world — nothing about the vulnerabilities themselves was built here. Labs 3–6 have interfaces and/or logic built specifically for NETRA, since services like raw FTP, Redis, and SSH don't ship with a browser GUI at all. Lab 6 is the only fully original vulnerable *application* — written from scratch as a deliberately unsafe "network diagnostic tool."

---

## ⚡ Quick Start

```bash
git clone https://github.com/Rishi0cybertech/Pavitra.git
cd Pavitra/Netra

python3 -m venv venv
source venv/bin/activate
pip install flask redis paramiko rich

# Start every lab's container
docker run -d --name netra-web    -p 3000:3000 bkimminich/juice-shop
docker run -d --name netra-sqli   -p 8081:80   vulnerables/web-dvwa
docker run -d --name netra-ftp    -p 2121:21   fauria/vsftpd
docker run -d --name netra-nosql  -p 6379:6379 redis:latest
docker run -d --name netra-ssh    -p 2222:22   rastasheep/ubuntu-sshd

# Launch the CLI dashboard
python3 netra.py
```

The launcher shows every lab, its category, difficulty, and opens the right one in your browser — no memorizing ports.

---

## 🖥️ Custom Labs — Live, Streaming Output

Labs 3–6 don't just click a button and wait. They stream real command output to the browser in real time via **Server-Sent Events (SSE)** — you watch the exploit happen line by line, like a live terminal, not a static result dump.

```bash
# Each runs as its own server — separate terminals
python3 ftp_lab.py     # :5001
python3 redis_lab.py   # :5002
python3 ssh_lab.py     # :5003
python3 cmdinj_lab.py  # :5004
```

---

## 📁 Structure

```
Netra/
├── netra.py          # CLI dashboard — lists and launches every lab
├── ftp_lab.py         # Anonymous FTP exploit, live streamed
├── redis_lab.py        # Unauthenticated Redis exploit, live streamed
├── ssh_lab.py          # SSH weak-credential brute force, live streamed
├── cmdinj_lab.py       # Original command injection app, live streamed
├── venv/
└── README.md
```

---

## ⚠️ Legal & Safety

Every service in every lab is bound to `localhost` only — none are reachable from any external network. Built strictly for personal, authorized, educational practice. The command injection lab in particular is deliberately unsafe code; never deploy it, or any lab here, on a network beyond your own machine.

---

## 🤝 Part of Pavitra

NETRA connects directly to the rest of the suite — a vulnerability practiced here can be independently confirmed by **NPath** (port scanning) and **WaveTrace** (live traffic capture), closing the loop between manual exploitation, automated detection, and network observation.

</div>
