import base64

def load_users(path):
    users = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if ":" in line:
                u, p = line.split(":", 1)
                users[u] = p
    return users

def auth_login(conn, users):
    conn.send(b"334 VXNlcm5hbWU6\r\n")
    user_b64 = conn.recv(1024).strip()

    conn.send(b"334 UGFzc3dvcmQ6\r\n")
    pass_b64 = conn.recv(1024).strip()

    try:
        user = base64.b64decode(user_b64).decode()
        password = base64.b64decode(pass_b64).decode()
    except:
        conn.send(b"535 Authentication failed\r\n")
        return False, None

    if user in users and users[user] == password:
        conn.send(b"235 Authentication successful\r\n")
        return True, user
    else:
        conn.send(b"535 Authentication failed\r\n")
        return False, None
