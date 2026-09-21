# Lab 01 - Path Double URL Encoding

## Scenario

A web application exposes an admin panel at `/panel/admin`.  
The route is directly blocked and returns **403 Forbidden**.

## Goal

Reach the admin panel and retrieve the flag.

## Setup

```bash
docker build -t lab01 .
docker run -p 5001:5001 lab01
```

Then open: http://localhost:5001

## Hints (for instructor use)

<details>
<summary>Hint 1</summary>
URL encoding transforms a character into its `%XX` hex form.  
What happens if you encode the `%` sign itself?
</details>

<details>
<summary>Hint 2</summary>
The letter `a` encodes to `%61`.  
Double-encoding means encoding the `%` again: `%` → `%25`, so `a` becomes `%2561`.  
Apply this to every character in `admin`.
</details>

<details>
<summary>Solution</summary>

```
GET /panel/%2561%2564%256d%2569%256e HTTP/1.1
```

The proxy/WAF decodes once → sees `%61%64%6d%69%6e` (not `admin`) → allows it.  
The Flask app decodes again → gets `admin` → grants access.
</details>
