import sqlite3
import secrets
import threading
import time
import urllib.parse

from flask import (
    Flask, render_template, request, redirect,
    url_for, make_response, session, g, abort
)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# ── Config ─────────────────────────────────────────────────────────────
BOT_USER    = 'chef'
BOT_TOKEN   = secrets.token_hex(32)   # token secret inconnu du joueur
FLAG        = 'HackUTT{M4g1Cal_c00Ki3_57eaLing}'
DB_PATH     = '/tmp/patisserie.db'

# ── DB ─────────────────────────────────────────────────────────────────
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db:
        db.close()

def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS orders (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            item     TEXT,
            qty      INTEGER
        );
        CREATE TABLE IF NOT EXISTS recipes (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            origin  TEXT NOT NULL,
            details TEXT NOT NULL
        );
        DELETE FROM recipes;
        INSERT INTO recipes (name, origin, details) VALUES
            ('Croissant',        'France',   'Feuilletage beurre, 27 couches, cuisson 18 min a 190C.'),
            ('Pain au chocolat', 'France',   'Pate feuilletee, deux barres de chocolat noir 70%.'),
            ('Eclair au cafe',   'France',   'Pate a choux, creme patissiere au cafe, glacage fondant.'),
            ('Mille-feuille',    'France',   'Trois couches de feuilletage, creme diplomate vanille.'),
            ('Tarte Tatin',      'France',   'Pommes caramelisees, pate brisee renversee.'),
            ('Macaron',          'France',   'Coques amande meringuees, ganache au choix.'),
            ('Kouign-amann',     'Bretagne', 'Pate levee feuilletee au sucre caramelise sale.'),
            ('Financier',        'France',   'Beurre noisette, poudre amande, blanc oeuf monte.'),
            ('Paris-Brest',      'France',   'Couronne de choux, creme pralinee, amandes effilees.'),
            ('Saint-Honore',     'France',   'Base feuilletee, choux caramelises, creme Chiboust.');
    """)
    db.commit()
    db.close()

# ── BOT ────────────────────────────────────────────────────────────────
def visit_as_admin(url):
    """
    Le bot visite /bot-auth/<token>.
    Le serveur pose lui-même session + secret_recipe via Set-Cookie,
    puis redirige le bot vers l'URL cible. Aucune injection Selenium.
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.binary_location = '/usr/bin/chromium'

    driver = webdriver.Chrome(options=options)
    try:
        auth_url = f'http://localhost:5002/bot-auth/{BOT_TOKEN}'

        # Étape 1 : récupérer les cookies (200 OK, pas de redirect)
        driver.get(auth_url)
        time.sleep(1)

        # Étape 2 : visiter l'URL du joueur avec les cookies actifs
        driver.get(url)
        time.sleep(7)

    except Exception as e:
        print(f'[BOT ERROR] {e}')
    finally:
        driver.quit()

# ── Routes ─────────────────────────────────────────────────────────────

@app.route('/bot-auth/<token>')
def bot_auth(token):
    """
    Pose session + cookies sur une réponse 200 sans redirect.
    Selenium stocke les cookies, puis navigue séparément vers l'URL cible.
    Évite le problème </script> dans le JS redirect.
    """
    if token != BOT_TOKEN:
        abort(403)

    # Identifie le bot en tant que "chef"
    session['username'] = BOT_USER

    resp = make_response('<html><body>ok</body></html>')
    resp.set_cookie('order_id',      secrets.token_hex(8),
                    httponly=False, samesite='Lax')
    
    # C'est ce cookie que le joueur doit voler avec le Cookie Sandwich !
    resp.set_cookie('secret_recipe', FLAG,
                    httponly=True,  samesite='Lax')
    return resp


@app.route('/')
@app.route('/dashboard')
def dashboard():
    order_id = request.cookies.get('order_id', '')
    
    # Si le cookie order_id n'existe pas encore (premier visiteur), on le crée
    if not order_id:
        order_id = secrets.token_hex(8)
        
    username = session.get('username', 'Visiteur')
    note     = request.args.get('note', '')
    
    resp = make_response(render_template('dashboard.html',
                           order_id=order_id, username=username, note=note))
                           
    # On s'assure de l'envoyer au client pour initialiser la mécanique
    resp.set_cookie('order_id', order_id, httponly=False, samesite='Lax')
    return resp


@app.route('/order', methods=['POST'])
def order():
    item     = request.form.get('item', '')
    qty      = request.form.get('qty', 1)
    username = session.get('username', 'Visiteur')
    
    db = get_db()
    db.execute("INSERT INTO orders (username, item, qty) VALUES (?, ?, ?)",
               (username, item, qty))
    db.commit()
    
    order_id = request.cookies.get('order_id', secrets.token_hex(8))
    
    resp = make_response(render_template('dashboard.html',
                           order_id=order_id,
                           username=username, note='',
                           order_confirmed=item, order_qty=qty))
    resp.set_cookie('order_id', order_id, httponly=False, samesite='Lax')
    return resp


@app.route('/recipes')
def recipes():
    db     = get_db()
    search = request.args.get('q', '')
    rows, error =[], None
    if search:
        try:
            # Spoiler: il y a aussi une petite injection SQL ici sur 'search' !
            rows = db.execute(
                f"SELECT id, name, origin, details FROM recipes "
                f"WHERE name LIKE '%{search}%'"
            ).fetchall()
        except Exception as e:
            error = str(e)
    else:
        rows = db.execute(
            "SELECT id, name, origin, details FROM recipes"
        ).fetchall()
    return render_template('recipes.html', rows=rows, search=search, error=error)


@app.route('/signal', methods=['GET', 'POST'])
def signal():
    sent = False
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if url:
            threading.Thread(target=visit_as_admin, args=(url,), daemon=True).start()
        sent = True
    return render_template('signal.html', sent=sent)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002, debug=False)
