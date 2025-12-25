def send_mail(s, sender, recipient, content):
    s.send(f"MAIL FROM:<{sender}>\r\n".encode())
    print(s.recv(1024).decode(), end="")

    s.send(f"RCPT TO:<{recipient}>\r\n".encode())
    print(s.recv(1024).decode(), end="")

    s.send(b"DATA\r\n")
    print(s.recv(1024).decode(), end="")

    s.send(content.encode() + b"\r\n.\r\n")
    print(s.recv(1024).decode(), end="")
