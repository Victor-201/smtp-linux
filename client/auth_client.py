import base64

def enc(s):
    return s.strip().encode("utf-8", errors="ignore")

def auth_login(sock, username, password):
    sock.sendall(b"AUTH LOGIN\r\n")
    resp = sock.recv(1024).decode().strip()
    print(resp)
    if not resp.startswith("334"):
        return False, None
    sock.sendall(base64.b64encode(enc(username)) + b"\r\n")
    resp = sock.recv(1024).decode().strip()
    print(resp)
    if not resp.startswith("334"):
        return False, None
    sock.sendall(base64.b64encode(enc(password)) + b"\r\n")
    resp = sock.recv(1024).decode().strip()
    print(resp)
    if resp.startswith("235"):
        try:
            start = resp.find("<")
            end = resp.find(">")
            email = resp[start+1:end] if start != -1 and end != -1 else None
        except:
            email = None
        return True, email
    return False, None
