from client.socket_client import connect
from client.auth_client import auth
from client.mail_sender import send_mail

def run():
    s = connect("127.0.0.1", 2525)

    s.send(b"HELO localhost\r\n")
    print(s.recv(1024).decode(), end="")

    user = input("Username: ")
    password = input("Password: ")
    auth(s, user, password)

    sender = input("From: ")
    recipient = input("To: ")

    print("Enter mail content (Ctrl+D to finish):")
    content = ""
    try:
        while True:
            content += input() + "\n"
    except EOFError:
        pass

    send_mail(s, sender, recipient, content)

    s.send(b"QUIT\r\n")
    print(s.recv(1024).decode(), end="")
