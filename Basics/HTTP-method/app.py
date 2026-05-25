from flask import Flask, request, render_template_string, redirect, url_for, session, abort

app = Flask(__name__)
app.secret_key = "supersecretkey123!"

FLAG = "HackUTT{Y0u_CoNjug47e_V3ry_W3LL}"

COUNT = 0

USED_METHODS = set()

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

<h3>HTTP Methods Learning Lab</h3>
<div>
    {{ content|safe  }}
</div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    if COUNT != 7:
        content = f"""
        <h2>Welcome to HackUTT</h2>
        <p>Try different methods on the endpoint /method to get the flag</p>
        <p>Method used {COUNT}/7</p>
        """
    else: 
        content = f"""
        <h2>Well done !</h2>
        <p>Know you can get the flag</p>
        <p>{FLAG}</p>
        <p>Note that there exist more methods like TRACE or CONNECT</p>
        """
    return render_template_string(base_template, title="index", content=content), 200

@app.route("/method", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"])
def method():
    global COUNT
    current_method = request.method
    content = f"""
    <h2>You used the {current_method} method</h2>
    <p>You are on the right way</p>
    """
    if current_method not in USED_METHODS:
        USED_METHODS.add(current_method)
        COUNT += 1
    return render_template_string(base_template, title="method", content=content), 200


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5003)
