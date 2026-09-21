from flask import Flask, request, render_template_string, Response

app = Flask(__name__)

FLAG = "HackUTT{r4ng3_h34d3r_byt3_by_byt3_3xf1l}"

ADMIN_CONTENT = f"""ACCESS GRANTED — INTERNAL ADMIN PANEL
======================================
Server: prod-01.internal
DB host: 10.0.0.42
Secret key: s3cr3t_k3y_d0_n0t_sh4r3

Flag: {FLAG}
"""

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

@app.route("/")
def index():
    return render_template_string(base_template,
        title="Range Header Lab",
        content="""
        <h2>Range Header Lab</h2>
        <p>Welcome to the internal portal.</p>
        <p>The admin panel is available at <code>/admin</code>.</p>
        <p>Access is restricted to authorized users only.</p>
        """
    )

@app.route("/admin")
def admin():
    range_header = request.headers.get("Range")

    # No Range header → standard auth check → denied
    if not range_header:
        return render_template_string(base_template,
            title="403 Forbidden",
            content='<h2>403 Forbidden</h2><p class="blocked">Access to the admin panel requires authentication.</p>'
        ), 403

    # Range header present → auth check skipped (the bug!)
    content_bytes = ADMIN_CONTENT.encode("utf-8")
    total = len(content_bytes)

    try:
        range_val = range_header.replace("bytes=", "")
        parts = range_val.split("-")
        start = int(parts[0]) if parts[0] else 0
        end = int(parts[1]) if parts[1] else total - 1
        end = min(end, total - 1)
    except Exception:
        return Response("Invalid Range header", status=416)

    chunk = content_bytes[start:end + 1]
    resp = Response(chunk, status=206, mimetype="text/plain")
    resp.headers["Content-Range"] = f"bytes {start}-{end}/{total}"
    resp.headers["Content-Length"] = str(len(chunk))
    resp.headers["Accept-Ranges"] = "bytes"
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=False)
