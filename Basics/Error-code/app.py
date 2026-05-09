from flask import Flask, request, render_template_string, redirect, url_for, session, abort

app = Flask(__name__)
app.secret_key = "supersecretkey123!"
FLAG = "HackUTT{L3arn_erR0r_Cod3_4_7he_WIN!!!}"
PASS_PARTS = {
        "200": "@l1ce",
        "302": "b0b",
        "403": "cHR15",
        "500": "D4v3"}


# 🎨 Template unique
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

<h3>HTTP Learning Lab</h3>
<p>2xx = Success | 3xx = Redirection | 4xx = Client Error | 5xx = Server Error</p>
<hr>

<div>
    {{ content|safe }}
</div>

</body>
</html>
"""

@app.route("/")
def index():
        content = f"""
        <h2>Welcome to HAckUTT</h2>
        <p>Status: 200 OK</p>
        <p>{PASS_PARTS["200"]}</p>

        <a href="/login> Aller au login</a>
        """
        return render_template_string(base_template, title="200 OK", content=content), 200



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form.get("username", "guest")
        return redirect(url_for("index"))  # 302 standard Flask

    content = f"""
    <h2>Login</h2>
    <p>Status: 302 Redirect</p>
    <p>{PASS_PARTS['302']}</p>

    <form method="post">
        <input name="username" placeholder="username">
        <input name="password" type="password" placeholder="password">
        <button type="submit">Login</button>
    </form>
    """
    return render_template_string(base_template, title="Login", content=content), 200



@app.route("/admin")
def admin():
    if session.get("username") != "admin":
        content = f"""
        <h2>Access refused !</h2>
        <p>Status 403 Forbidden</p>
        <p>{PASS_PARTS["403"]}</p>
        """
        return render_template_string(base_template, title="403 Forbidden", content=content), 403
    return "<h2>Welcome admin</h2>"



@app.route("/crash")
def crash():
    # erreur volontaire pour déclencher un 500
    return 1 / 0


@app.route("/flag", methods=["GET", "POST"])
def flag():
    if request.method == "POST":
        password = request.form.get("password", "")

        if password == PASS_PARTS["200"] + PASS_PARTS["302"] + PASS_PARTS["403"] + PASS_PARTS["500"]:
            content = f"""
            <h2>Well done !</h2>
            <p>You get the flag</p>
            <p>{FLAG}</p>
            """
            return render_template_string(base_template, title="FLAG", content=content), 200

        # mauvais mot de passe
        content = """
        <h2>Wrong password</h2>
        <p>Access refused</p>
        """
        return render_template_string(base_template, title="403", content=content), 403

    # GET → formulaire
    content = """
    <h2>Accès au flag</h2>
    <form method="post">
        <input name="password" type="password" placeholder="Mot de passe">
        <button type="submit">Accéder</button>
    </form>
    """
    return render_template_string(base_template, title="Flag login", content=content), 200



@app.errorhandler(500)
def error500(e):
    content = f"""
    <h2>Server Error</h2>
    <p>Status: 500 Internal Server Error</p>
    <p>{PASS_PARTS['500']}</p>
    """
    return render_template_string(base_template, title="500 Error", content=content), 500


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5001)
