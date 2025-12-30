def send_mail(sock, mail_from, rcpt_to, subject, body):
    sock.send(f"MAIL FROM:<{mail_from}>\r\n".encode())
    print(sock.recv(1024).decode("utf-8").strip())
    
    for recipient in rcpt_to:
        sock.send(f"RCPT TO:<{recipient}>\r\n".encode())
        print(sock.recv(1024).decode("utf-8").strip())
    
    sock.send(b"DATA\r\n")
    print(sock.recv(1024).decode("utf-8").strip())
    
    message = f"Subject: {subject}\r\n\r\n{body}\r\n.\r\n"
    sock.send(message.encode())
    print(sock.recv(1024).decode("utf-8").strip())