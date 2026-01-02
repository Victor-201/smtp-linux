def enc(s):
    return s.strip().encode("utf-8", errors="ignore")

def send_mail(sock, from_addr, to_addr, subject, body):
    sock.sendall(b"MAIL FROM:<" + enc(from_addr) + b">\r\n")
    print(sock.recv(1024).decode().strip())
    sock.sendall(b"RCPT TO:<" + enc(to_addr) + b">\r\n")
    print(sock.recv(1024).decode().strip())
    sock.sendall(b"DATA\r\n")
    print(sock.recv(1024).decode().strip())
    sock.sendall(b"Subject: " + enc(subject) + b"\r\n\r\n")
    for line in body.split("\n"):
        sock.sendall(enc(line) + b"\r\n")
    sock.sendall(b".\r\n")
    print(sock.recv(1024).decode().strip())
