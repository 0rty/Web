from flask import Flask, request, render_template_string
from posixpath import normpath

app = Flask(__name__)

FLAG = "HackUTT{p4th_tr4v3rs4l_n0rm4l1z4t10n}"

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
    code { background: #161b22; padding: 2px 6px; border-radius: 4px; }
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

def render_403():
    return render_template_string(base_template,
        title="403 Forbidden",
        content='<h2>403 Forbidden</h2><p class="blocked">This path is blocked by security policy.</p>'
    ), 403

def render_admin():
    return render_template_string(base_template,
        title="Admin Dashboard",
        content=f'<h2>Admin Dashboard</h2><p>Restricted area — internal use only.</p><p class="flag">Flag: {FLAG}</p>'
    )

@app.route("/")
def index():
    return render_template_string(base_template,
        title="Path Normalization Lab",
        content="""
        <h2>Path Normalization Lab</h2>
        <p>The route <code>/dashboard/admin</code> is protected.</p>
        <p>Can you reach it anyway?</p>
        """
    )

@app.route("/dashboard")
@app.route("/dashboard/")
def dashboard():
    return render_template_string(base_template,
        title="Dashboard",
        content='<h2>Dashboard</h2><p>Welcome. The admin section is restricted.</p>'
    )

@app.route("/dashboard/<path:subpath>")
def dashboard_catch(subpath):
    raw_path = "/dashboard/" + subpath  # path as received by the server

    # --- WAF simulation ---
    # The WAF checks the raw path with a simple string match.
    # It blocks /dashboard/admin exactly — but does NOT normalize first.
    if raw_path == "/dashboard/admin":
        return render_403()

    # --- Backend normalization ---
    # The backend normalizes the path using POSIX rules (same as the OS / HTTP spec).
    # /dashboard/./admin  → /dashboard/admin
    # /dashboard/x/../admin → /dashboard/admin
    normalized = normpath(raw_path)

    if normalized == "/dashboard/admin":
        return render_admin()

    return render_template_string(base_template,
        title="Not Found",
        content=f'<h2>404</h2><p>Path not found: <code>{raw_path}</code></p>'
    ), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
