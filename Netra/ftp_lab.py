#!/usr/bin/env python3
import time
from flask import Flask, Response, render_template_string, request
import ftplib

app = Flask(__name__)

# --- HTML / Frontend Template (NETRA Dark Navy/Purple Theme) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NETRA - FTP Vulnerability Lab</title>
    <style>
        body {
            background-color: #0b0f19;
            color: #e2e8f0;
            font-family: 'Courier New', Courier, monospace;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        h1 {
            color: #a78bfa;
            text-shadow: 0 0 10px rgba(167, 139, 250, 0.3);
        }
        .card {
            background-color: #1e1b4b;
            border: 1px solid #312e81;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #c084fc;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            background-color: #0f172a;
            border: 1px solid #4338ca;
            color: #f8fafc;
            border-radius: 4px;
            margin-bottom: 15px;
            box-sizing: border-box;
        }
        button {
            background-color: #7c3aed;
            color: white;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        button:hover {
            background-color: #6d28d9;
        }
        button:disabled {
            background-color: #4b5563;
            cursor: not-allowed;
        }
        pre {
            background-color: #030712;
            border: 1px solid #374151;
            border-radius: 4px;
            padding: 15px;
            height: 350px;
            overflow-y: auto;
            color: #34d399;
            font-size: 14px;
            line-height: 1.4;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>NETRA // FTP Exploit Lab</h1>
        <div class="card">
            <label for="target">Target Host / IP:</label>
            <input type="text" id="target" value="127.0.0.1" placeholder="127.0.0.1">
            <button id="exploitBtn" onclick="startExploit()">Execute Exploit Stream</button>
            
            <pre id="terminal">System ready. Click 'Execute Exploit Stream' to begin...</pre>
        </div>
    </div>

    <script>
        let eventSource = null;

        function startExploit() {
            const target = document.getElementById('target').value.trim();
            const terminal = document.getElementById('terminal');
            const btn = document.getElementById('exploitBtn');

            if (!target) {
                alert('Please specify a target host.');
                return;
            }

            // Reset and prep UI
            terminal.textContent = '';
            btn.disabled = true;
            btn.textContent = 'Executing Attack...';

            if (eventSource) {
                eventSource.close();
            }

            // Open SSE connection with target parameter
            eventSource = new EventSource(`/ftp/stream?target=${encodeURIComponent(target)}`);

            eventSource.onmessage = function(event) {
                // Append each line live as it streams in
                terminal.textContent += event.data + '\\n';
                terminal.scrollTop = terminal.scrollHeight; // Auto scroll down
            };

            eventSource.onerror = function(err) {
                terminal.textContent += '\\n[!] Connection closed or stream terminated.\\n';
                cleanup();
            };
        }

        function cleanup() {
            if (eventSource) {
                eventSource.close();
                eventSource = null;
            }
            const btn = document.getElementById('exploitBtn');
            btn.disabled = false;
            btn.textContent = 'Execute Exploit Stream';
        }
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/ftp/stream")
def ftp_stream():
    target = request.args.get("target", "127.0.0.1")

    def generate():
        def send_line(text):
            return f"data: {text}\n\n"

        yield send_line(f"[*] Initializing NETRA FTP module...")
        yield send_line(f"[*] Target specified: {target}")
        time.sleep(0.3)

        try:
            yield send_line(f"[+] Connecting to {target}:21...")
            # Real ftplib connection
            ftp = ftplib.FTP()
            ftp.connect(target, 21, timeout=5)
            
            banner = ftp.getwelcome()
            yield send_line(f"[+] Server Banner received:")
            for line in banner.splitlines():
                yield send_line(f"    > {line}")

            yield send_line(f"[*] Attempting anonymous authentication...")
            login_response = ftp.login('anonymous', 'netra@lab.local')
            yield send_line(f"[+] Login successful: {login_response}")

            yield send_line(f"[*] Querying current working directory...")
            pwd = ftp.pwd()
            yield send_line(f"[+] Current directory: {pwd}")

            yield send_line(f"[*] Fetching directory listing (LIST)...")
            files = []
            ftp.dir(files.append)
            
            yield send_line(f"[+] Directory contents retrieved successfully ({len(files)} items):")
            for f_item in files:
                yield send_line(f"    {f_item}")
                time.sleep(0.05) # Aesthetic pacing for live terminal feel

            yield send_line(f"[*] Closing active FTP session.")
            ftp.quit()
            yield send_line(f"[+] Exploit workflow completed successfully.")

        except Exception as e:
            yield send_line(f"[!] Error during FTP execution: {str(e)}")

        yield send_line("[DONE]")

    return Response(generate(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
