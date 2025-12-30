import base64

def auth_login(sock, username, password):
    sock.send(b"AUTH LOGIN\r\n")
    resp = sock.recv(1024).decode("utf-8")
    print(resp.strip())
    
    user_b64 = base64.b64encode(username.encode("utf-8")).decode("utf-8")
    sock.send(f"{user_b64}\r\n".encode())
    resp = sock.recv(1024).decode("utf-8")
    print(resp.strip())
    
    pass_b64 = base64.b64encode(password.encode("utf-8")).decode("utf-8")
    sock.send(f"{pass_b64}\r\n".encode())
    resp = sock.recv(1024).decode("utf-8")
    print(resp.strip())
    
    return "235" in resp