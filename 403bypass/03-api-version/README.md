# Lab 03 — API Version Bypass

## Scenario

A REST API has been hardened in its latest version (`v2`).  
The admin configuration endpoint `/api/v2/admin/config` returns 403.  
During a recon phase, you notice the API has version prefixes in its URLs.

## Goal

Retrieve the admin configuration and find the flag.

## Setup

```bash
docker build -t lab03 .
docker run -p 5003:5003 lab03
```

Then open: http://localhost:5003

## Hints (for instructor use)

<details>
<summary>Hint 1</summary>
APIs evolve over time. Security controls are often added in newer versions,  
but older versions may still be accessible and unprotected.
</details>

<details>
<summary>Hint 2</summary>
If `/api/v2/admin/config` is blocked, what about `/api/v1/admin/config`?
</details>

<details>
<summary>Solution</summary>

```
GET /api/v1/admin/config HTTP/1.1
```

The v1 endpoint was never decommissioned and has no access controls.  
This is a real-world pattern: APIs accumulate versions, and old endpoints  
are forgotten rather than removed.
</details>
