# 403 Bypass Labs — HackUTT

A collection of 5 independent hands-on labs covering common HTTP 403 bypass techniques.  
Each lab runs in Docker and exposes a Flask application (with nginx for lab 05).

## Labs

| # | Technique | Port | Stack |
|---|---|---|---|
| 01 | Path Double URL Encoding | 5001 | Flask |
| 02 | Path Normalization | 5002 | Flask |
| 03 | API Version Bypass | 5003 | Flask |
| 04 | Range Header Content Leak | 5004 | Flask |
| 05 | HTTP Request Smuggling (CL.TE) | 5005 | nginx + gunicorn + Flask |

## Quick start

Each lab is independent. Navigate into a folder and run:

```bash
# Labs 01–04 (Flask only)
docker build -t labXX .
docker run -p 50XX:5000 labXX

# Lab 05 (nginx + gunicorn)
docker-compose up --build
```

## Prerequisites

- Docker
- Burp Suite (Community or Pro)
- Basic HTTP knowledge

## Flag format

```
HackUTT{...}
```
