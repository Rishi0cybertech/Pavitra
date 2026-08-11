from flask import Flask, render_template_string, Response, request
import subprocess
import json
import shlex

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>NETRA — Command Injection Lab</title>
    <style>
        body { background: #0A0E1A; color: #E0E0E0; font-family: 'Courier New', monospace; padding: 40px; }
        h1 { color: #D946EF; }
        .card { background: #1A1040; border: 1px solid #2D1B69; border-radius: 8px; padding: 24px; margin-top: 20px; }
        input[type=text] { background: #0A0E1A; color: #4ADE80; border: 1px solid #2D1B69; padding: 10px; width: 400px; font-family: inherit; border-radius: 4px; }
        button { background: #D946EF; color: #0A0E1A; border: none; padding: 12px 24px; font-weight: bold; cursor: pointer; border-radius: 4px; font-family: inherit; margin-left: 8px; }
        button:hover { background: #E879F9; }
        #terminal { background: #000; color: #4ADE80; padding: 16px; border-radius: 4px; min-height: 150px; font-size: 14px; white-space: pre-wrap; border: 1px solid #2D1B69; margin-top: 16px; }
        .hint { color: #FBBF24; font-size: 13px; margin-top: 10px; }
        code { background: #0A0E1A; padding: 2px 6px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>🎯 NETRA — OS Command Injection Lab</h1>
    <div class="card">
        <p><strong>This is a custom-built vulnerable app</strong> — a "Network Diagnostic Tool" that lets a
        user ping a host. Behind the scenes, the input is concatenated directly into a shell command with
        no sanitization — a real, common vulnerability class (CWE-78).</p>

        <form onsubmit="runPing(event)">
            <input type="text" id="hostInput" placeholder="e.g. 127.0.0.1" value="127.0.0.1">
            <button type="submit">Ping Host</button>
        </form>

        <p class="hint">💡 Try normal input first: <code>127.0.0.1</code><br>
        Then try injection: <code>127.0.0.1; whoami</code> or <code>127.0.0.1 && id</code></p>

        <div id="terminal">Output will stream here...\n</div>
    </div>

<script>
function runPing(e) {
    e.preventDefault();
    const host = document.getElementById('hostInput').value;
    const term = document.getElementById('terminal');
    term.textContent = '';

    const source = new EventSource('/ping/stream?host=' + encodeURIComponent(host));
    source.onmessage = function(event) {
        const data = JSON.parse(event.data);
        term.textContent += data.text + '\\n';
        term.scrollTop = term.scrollHeight;
        if (data.done) source.close();
    };
    source.onerror = function() { source.close(); };
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(PAGE)

def sse_event(text, done=False):
    return f"data: {json.dumps({'text': text, 'done': done})}\n\n"

@app.route("/ping/stream")
def ping_stream():
    host_input = request.args.get("host", "127.0.0.1")

    def generate():
        yield sse_event(f"$ ping -c 3 {host_input}")

        # VULNERABLE BY DESIGN: raw string concatenation into shell=True.
        # This is the exact anti-pattern that causes real CWE-78 command
        # injection vulnerabilities — user input reaches the shell unsanitized.
        command = f"ping -c 3 {host_input}"

        try:
            result = subprocess.run(
                command, shell=True, capture_output=True,
                text=True, timeout=10
            )
            output = result.stdout + result.stderr
            for line in output.splitlines():
                yield sse_event(line)
        except subprocess.TimeoutExpired:
            yield sse_event("[!] Command timed out")
        except Exception as e:
            yield sse_event(f"[!] Error: {e}")

        yield sse_event("", done=True)

    return Response(generate(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=False, threaded=True)
