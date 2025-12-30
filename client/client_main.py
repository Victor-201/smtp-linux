import configparser
from .socket_client import connect_server
from .auth_client import auth_login
from .mail_sender import send_mail

def main():
    config = configparser.ConfigParser()
    config.read("../config/server.conf")
    host = config["server"]["host"]
    port = int(config["server"]["port"])
    
    sock = connect_server(host, port)
    
    sock.send(b"HELO client.local\r\n")
    print(sock.recv(1024).decode("utf-8").strip())
    
    username = input("Username: ")
    password = input("Password: ")
    
    if not auth_login(sock, username, password):
        print("Đăng nhập thất bại!")
        sock.send(b"QUIT\r\n")
        sock.close()
        return
    
    mail_from = input("From: ")
    rcpt_input = input("To (cách nhau bởi dấu phẩy): ")
    rcpt_to = [r.strip() for r in rcpt_input.split(",")]
    subject = input("Subject: ")
    print("Body (kết thúc bằng dòng chỉ chứa dấu chấm '.'): ")
    body_lines = []
    while True:
        line = input()
        if line == ".":
            break
        body_lines.append(line)
    body = "\n".join(body_lines)
    
    send_mail(sock, mail_from, rcpt_to, subject, body)
    
    sock.send(b"QUIT\r\n")
    print(sock.recv(1024).decode("utf-8").strip())
    sock.close()

if __name__ == "__main__":
    main()