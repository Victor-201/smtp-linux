import socket, threading
from server.smtp_parser import SMTPParser
from server.log_handler import log_event

def handle_client(conn, addr):
    ip = addr[0]
    log_event(ip=ip, message="CONNECT")
    parser = SMTPParser(ip)
    conn.sendall(b"220 localhost SMTP Ready\r\n")
    buffer = ""
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            buffer += data.decode(errors="ignore")
            while "\r\n" in buffer:
                line, buffer = buffer.split("\r\n", 1)
                resp = parser.process_command(line)
                if resp:
                    conn.sendall((resp + "\r\n").encode())
                    if resp.startswith("221"):
                        return
    finally:
        conn.close()
        log_event(ip=ip, message="DISCONNECT")

def start_listener(host, port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    print(f"[*] SMTP Server listening on {host}:{port}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
