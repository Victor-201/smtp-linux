from client.socket_client import connect
from client.auth_client import auth_login
from client.mail_sender import send_mail

def main():
    sock = connect()
    sock.sendall(b"HELO client\r\n")
    print(sock.recv(1024).decode().strip())
    username = input("Username or Email: ")
    password = input("Password: ")
    ok, email = auth_login(sock, username, password)
    if not ok:
        sock.sendall(b"QUIT\r\n")
        sock.close()
        return
    from_addr = email if email else username
    if email:
        print(f"From: {email}")
    to_addr = input("To: ")
    subject = input("Subject: ")
    print("Body (end with '.'): ")
    lines = []
    while True:
        l = input()
        if l == ".":
            break
        lines.append(l)
    send_mail(sock, from_addr, to_addr, subject, "\n".join(lines))
    sock.sendall(b"QUIT\r\n")
    print(sock.recv(1024).decode().strip())
    sock.close()

if __name__ == "__main__":
    main()