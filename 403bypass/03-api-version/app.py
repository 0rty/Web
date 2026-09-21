from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

FLAG = "HackUTT{0ld_4p1_v3rs10n_n3v3r_d13s}"

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
    pre {
        background: #161b22;
        padding: 15px;
        border-radius: 8px;
        text-align: left;
        color: #3fb950;
        max-width: 600px;
        word-break: break-all;
    }
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

# v2 — current, hardened API
@app.route("/api/v2/users")
def api_v2_users():
    return render_template_string(base_template,
        title="API v2 - Users",
        content='<h2>API v2 — /users</h2><p>Returns public user list. Admin endpoints have been removed in v2.</p>'
    )

@app.route("/api/v2/admin/config")
def api_v2_admin():
    return render_template_string(base_template,
        title="403 Forbidden",
        content='<h2>403 Forbidden</h2><p class="blocked">Admin endpoints are disabled in API v2.</p>'
    ), 403

# v1 — legacy, forgotten, not hardened
@app.route("/api/v1/admin/config")
def api_v1_admin():
    return render_template_string(base_template,
        title="API v1 - Admin Config",
        content=f"""
        <h2>API v1 — Admin Config</h2>
        <p>Legacy endpoint. Access controls not enforced in v1.</p>
        <pre>{{
  "debug": true,
  "db_host": "internal-db.local",
  "secret_key": "sup3r_s3cr3t",
  "flag": "{FLAG}"
}}</pre>
        """
    )

@app.route("/api/v1/users")
def api_v1_users():
    return render_template_string(base_template,
        title="API v1 - Users",
        content='<h2>API v1 — /users</h2><p>Legacy user endpoint.</p>'
    )

@app.route("/")
def index():
    return render_template_string(base_template,
        title="API Version Lab",
        content="""
        <h2>API Version Lab</h2>
        <p>The application exposes a REST API.</p>
        <p>The current version is <code>v2</code>.</p>
        <p>The admin config endpoint at <code>/api/v2/admin/config</code> is blocked.</p>
        <p>Can you retrieve the admin configuration anyway?</p>
        """
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=False)
