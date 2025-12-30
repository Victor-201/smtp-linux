import socket

def connect_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    banner = s.recv(1024).decode("utf-8")
    print(banner.strip())
    return s