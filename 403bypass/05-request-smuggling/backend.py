"""
Vulnerable HTTP/1.1 backend — intentionally mimics a server that:
  - Accepts both Content-Length and Transfer-Encoding headers
  - Prioritizes Transfer-Encoding: chunked (RFC-compliant)
  - Keeps connections alive (persistent connections)

The CL.TE smuggling works because:
  - nginx (front-end) reads Content-Length → determines body boundary
  - This backend reads Transfer-Encoding: chunked → different boundary
  - The "leftover" bytes become a new request processed internally
"""
import socket, threading, re

FLAG = "HackUTT{CL_TE_smuggl1ng_fr0nt_b4ck_diss0nanc3}"

def html_page(title, content):
    return f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><title>{title}</title>
<style>
body {{background-color:#0d1117;color:#c9d1d9;font-family:"Courier New",monospace;
      display:flex;flex-direction:column;align-items:center;justify-content:center;
      height:100vh;text-align:center;}}
h2 {{color:#58a6ff;}} .flag {{color:#3fb950;font-size:1.2em;margin-top:20px;}}
.blocked {{color:#f85149;font-size:1.2em;}} p {{color:#8b949e;}}
code {{background:#161b22;padding:2px 6px;border-radius:4px;}}
</style></head>
<body><h3>HTTP Headers Learning Lab</h3><div>{content}</div></body></html>"""

def make_response(status, body_str):
    body = body_str.encode()
    header = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"\r\n"
    ).encode()
    return header + body

def try_parse(buf):
    """
    Try to parse one complete HTTP request from buf.
    Returns (method, path, body_end_pos) or None if incomplete.
    """
    header_end = buf.find(b"\r\n\r\n")
    if header_end == -1:
        return None

    header_section = buf[:header_end].decode(errors="replace")
    lines = header_section.split("\r\n")
    parts = lines[0].split(" ")
    if len(parts) < 2:
        return None
    method, path = parts[0], parts[1]

    headers = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    body_start = header_end + 4
    te = headers.get("transfer-encoding", "")
    cl_str = headers.get("content-length", "0")

    # Prioritize Transfer-Encoding: chunked (the vulnerable behavior)
    if "chunked" in te:
        pos = body_start
        while pos < len(buf):
            end = buf.find(b"\r\n", pos)
            if end == -1:
                return None  # incomplete chunk
            try:
                size = int(buf[pos:end].split(b";")[0].strip(), 16)
            except ValueError:
                return None
            pos = end + 2
            if size == 0:
                pos += 2  # consume trailing \r\n after last chunk
                return method, path, pos
            pos += size + 2
        return None  # incomplete
    else:
        try:
            length = int(cl_str)
        except ValueError:
            length = 0
        body_end = body_start + length
        if len(buf) < body_end:
            return None  # incomplete
        return method, path, body_end

def route(method, path):
    if path == "/":
        body = html_page("Request Smuggling Lab",
            "<h2>Request Smuggling Lab (CL.TE)</h2>"
            "<p>This application sits behind an nginx reverse proxy.</p>"
            "<p>The <code>/admin</code> route is blocked by nginx.</p>"
            "<p>Can you reach it from outside?</p>")
        return make_response("200 OK", body)

    if path == "/post" and method == "POST":
        body = html_page("POST endpoint", "<h2>POST /post</h2><p>Request received.</p>")
        return make_response("200 OK", body)

    if path == "/admin":
        body = html_page("Admin Panel",
            f"<h2>Admin Panel</h2><p>Internal access granted.</p>"
            f'<p class="flag">Flag: {FLAG}</p>')
        return make_response("200 OK", body)

    body = html_page("404", '<h2>404</h2><p class="blocked">Not found.</p>')
    return make_response("404 Not Found", body)

def handle_client(conn, addr):
    conn.settimeout(5)
    buf = b""
    try:
        while True:
            # Try to process any complete request already in buffer
            result = try_parse(buf)
            if result is not None:
                method, path, end = result
                resp = route(method, path)
                conn.sendall(resp)
                buf = buf[end:]
                continue  # try to parse next request immediately

            # Buffer has no complete request — read more data
            try:
                data = conn.recv(4096)
                if not data:
                    break
                buf += data
            except socket.timeout:
                break
    except Exception:
        pass
    finally:
        conn.close()

def run(host="0.0.0.0", port=8000):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen(50)
    print(f"Vulnerable backend listening on {host}:{port}")
    while True:
        conn, addr = srv.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    run()
