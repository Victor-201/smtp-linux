import base64

def auth(s, user, password):
    s.send(b"AUTH LOGIN\r\n")
    print(s.recv(1024).decode(), end="")

    s.send(base64.b64encode(user.encode()) + b"\r\n")
    print(s.recv(1024).decode(), end="")

    s.send(base64.b64encode(password.encode()) + b"\r\n")
    print(s.recv(1024).decode(), end="")
