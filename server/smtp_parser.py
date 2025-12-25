from server.auth_handler import auth_login
from server.mail_handler import save_mail
from server.log_handler import log_event

def handle_client(conn, addr, config, users):
    conn.send(b"220 Simple SMTP Server Ready\r\n")

    authenticated = False
    current_user = None
    sender = ""
    recipient = ""
    data_lines = []

    while True:
        data = conn.recv(1024)
        if not data:
            break

        cmd = data.decode().strip()

        if cmd.startswith("HELO"):
            conn.send(b"250 OK\r\n")

        elif cmd == "AUTH LOGIN":
            authenticated, current_user = auth_login(conn, users)

        elif cmd.startswith("MAIL FROM"):
            sender = cmd.split(":", 1)[1].strip("<>")
            conn.send(b"250 OK\r\n")

        elif cmd.startswith("RCPT TO"):
            recipient = cmd.split(":", 1)[1].strip("<>")
            conn.send(b"250 OK\r\n")

        elif cmd == "DATA":
            conn.send(b"354 End data with <CR><LF>.<CR><LF>\r\n")
            data_lines.clear()

            while True:
                line = conn.recv(1024).decode()
                if line.strip() == ".":
                    break
                data_lines.append(line)

            if authenticated:
                save_mail(
                    config["MAIL_ROOT"],
                    current_user,
                    sender,
                    recipient,
                    "".join(data_lines)
                )
                log_event(
                    config["LOG_FILE"],
                    addr[0],
                    sender,
                    recipient,
                    "AUTH_OK"
                )
                conn.send(b"250 Message accepted\r\n")
            else:
                conn.send(b"535 Authentication required\r\n")

        elif cmd == "QUIT":
            conn.send(b"221 Bye\r\n")
            break

        else:
            conn.send(b"500 Command not recognized\r\n")

    conn.close()
