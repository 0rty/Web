from flask import Flask, request, render_template_string
from urllib.parse import unquote
import re

app = Flask(__name__)

FLAG = "HackUTT{d0ubl3_enc0d1ng_byp4ss_ftw}"

base_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>{{ title }}</title>
<style>
    body {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: "Courier New", monospace;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        text-align: center;
    }
    h2 { color: #58a6ff; }
    .flag { color: #3fb950; font-size: 1.2em; margin-top: 20px; }
    .blocked { color: #f85149; font-size: 1.2em; }
    p { color: #8b949e; }
</style>
</head>
<body>
<h3>HTTP Headers Learning Lab</h3>
<div>
    {{ content|safe }}
</div>
</body>
</html>
"""

def decode_path(path):
    """Decode once — simulates what a WAF/proxy does before forwarding."""
    return unquote(path)

@app.route("/panel/admin")
def admin_direct():
    # Direct access is blocked
    return render_template_string(base_template,
        title="403 Forbidden",
        content='<h2>403 Forbidden</h2><p class="blocked">Access denied to /panel/admin.</p>'
    ), 403

@app.route("/panel/<path:subpath>")
def panel(subpath):
    # Decode the path a second time (the app decodes again after the "proxy" decoded once)
    decoded = decode_path(subpath)

    if decoded == "admin":
        return render_template_string(base_template,
            title="Admin Panel",
            content=f'<h2>Admin Panel</h2><p>Welcome, admin.</p><p class="flag">Flag: {FLAG}</p>'
        )

    return render_template_string(base_template,
        title="Panel",
        content=f'<h2>Panel</h2><p>Section: {decoded}</p>'
    )

@app.route("/")
def index():
    return render_template_string(base_template,
        title="Double Encoding Lab",
        content="""
        <h2>Double URL Encoding Lab</h2>
        <p>The <code>/panel/admin</code> route is protected.</p>
        <p>Can you find another way to reach it?</p>
        """
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
