from flask import Flask, request, render_template_string, redirect, url_for, session, abort

app = Flask(__name__)
app.secret_key = "supersecretkey123!"
FLAG = "HackUTT{Y0u_h4dL3_HearD3R5_N0W}"

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
    input {
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
        border: 1px solid #30363d;
        background-color: #161b22;
        color: #c9d1d9;
    }
    button {
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        background-color: #238636;
        color: white;
        cursor: pointer;
        margin-top: 10px;
    }
</style>
</head>
<body>

<h3>HTTP Headers Learning Lab</h3>
<div>
    {{ content|safe  }}
</div>
</body>
</html>
"""


@app.route("/")
def index():
    content = """
    <h2>Welcome to HackUTT</h2>
    <p>You'll find the flag at the /flag endpoint</p>
    """
    return render_template_string(base_template, title="Welcome", content=content), 200


@app.route("/flag")
def flag():
    if request.headers.get('User-Agent') != "Gustave":
        content = """
        <h2>Wrong User-Agent !</h2>
        <p>You should be Gustave</p>
        """
        return render_template_string(base_template, title="Gustave", content=content), 403
    if request.headers.get('Accept-Datetime') != "Mon, 6 Jul 1987 20:00:00 GMT":
        content = """
        <h2>Wrong Date !</h2>
        <p>You should be there on Monday, 6 July 1987 at 20:00:00 GMT</p>
        """
        return render_template_string(base_template, title="Date", content=content), 403
    if request.headers.get('X-Forwarded-For') != "67.67.67.67":
        content = """
        <h2>Wrong IP</h2>
        <p>You told me that your IP was 67.67.67.67</p>
        """
        return render_template_string(base_template, title="IP", content=content), 403
    content = f"""
    <h2>Welcome Gustave</h2>
    <p>You proved your identity, you can get the flag.</p>
    <p>{FLAG}</p>
    """
    return render_template_string(base_template, title="FLAG", content=content), 200



if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5002)
