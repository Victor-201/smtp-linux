import socket, sys

def connect(host="127.0.0.1", port=2525):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((host, port))
    except Exception:
        print("[!] Cannot connect to SMTP server")
        sys.exit(1)
    banner = s.recv(1024).decode().strip()
    print(banner)
    return s
