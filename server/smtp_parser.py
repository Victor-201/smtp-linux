import datetime
from .log_handler import log_event
from .auth_handler import authenticate
from .mail_handler import save_mail

STATE_INIT = 0
STATE_AUTH_USER = 1
STATE_AUTH_PASS = 2
STATE_MAIL = 3
STATE_RCPT = 4
STATE_DATA = 5

def handle_client(client_socket, addr):
    ip = addr[0]
    log_event(ip, message="Connection established")
    
    client_socket.send(b"220 localhost.localdomain SMTP GrokSMTP\r\n")
    
    state = STATE_INIT
    authenticated = False
    authenticated_user = ""
    mail_from = ""
    rcpt_to = []
    data_buffer = []
    
    try:
        while True:
            line = client_socket.recv(1024).decode("utf-8").strip()
            if not line:
                break
            
            log_event(ip, mail_from, ",".join(rcpt_to), "OK" if authenticated else "NONE", f"RECV: {line}")
            
            if state == STATE_DATA:
                if line == ".":
                    # Kết thúc DATA
                    full_data = "\r\n".join(data_buffer) + "\r\n"
                    for recipient in rcpt_to:
                        local_part = recipient.split("@")[0]
                        save_mail(local_part, mail_from, full_data)
                    client_socket.send(b"250 OK\r\n")
                    log_event(ip, mail_from, ",".join(rcpt_to), authenticated_user, "Mail saved")
                    state = STATE_MAIL
                    mail_from = ""
                    rcpt_to = []
                    data_buffer = []
                else:
                    data_buffer.append(line)
                continue
            
            command = line.split(" ", 1)[0].upper()
            
            if command == "HELO":
                client_socket.send(b"250 OK\r\n")
                
            elif command == "AUTH" and line.upper().startswith("AUTH LOGIN"):
                client_socket.send(b"334 VXNlcm5hbWU6\r\n")  # "Username:"
                state = STATE_AUTH_USER
                
            elif state == STATE_AUTH_USER:
                username_b64 = line
                client_socket.send(b"334 UGFzc3dvcmQ6\r\n")  # "Password:"
                state = STATE_AUTH_PASS
                temp_user_b64 = username_b64
                
            elif state == STATE_AUTH_PASS:
                success, username = authenticate(temp_user_b64, line)
                if success:
                    client_socket.send(b"235 Authentication successful\r\n")
                    authenticated = True
                    authenticated_user = username
                    log_event(ip, auth_status=username)
                else:
                    client_socket.send(b"535 Authentication failed\r\n")
                    log_event(ip, auth_status="FAILED")
                state = STATE_INIT
                
            elif command == "MAIL" and line.upper().startswith("MAIL FROM:"):
                if not authenticated:
                    client_socket.send(b"503 Authentication required\r\n")
                    continue
                mail_from = line[10:].strip("<>")
                client_socket.send(b"250 OK\r\n")
                state = STATE_MAIL
                
            elif command == "RCPT" and line.upper().startswith("RCPT TO:"):
                if not mail_from:
                    client_socket.send(b"503 Bad sequence\r\n")
                    continue
                recipient = line[8:].strip("<>")
                rcpt_to.append(recipient)
                client_socket.send(b"250 OK\r\n")
                
            elif command == "DATA":
                if not mail_from or not rcpt_to:
                    client_socket.send(b"503 Bad sequence\r\n")
                    continue
                client_socket.send(b"354 Start mail input; end with <CRLF>.<CRLF>\r\n")
                state = STATE_DATA
                data_buffer = []
                
            elif command == "QUIT":
                client_socket.send(b"221 Bye\r\n")
                log_event(ip, message="Connection closed")
                break
                
            else:
                client_socket.send(b"500 Command not recognized\r\n")
                
    except Exception as e:
        log_event(ip, message=f"Error: {str(e)}")
    finally:
        client_socket.close()