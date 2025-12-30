import socket
import threading

def start_listener(host, port, handler_callback):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[+] SMTP Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[+] Connection from {addr}")
        client_thread = threading.Thread(target=handler_callback, args=(client_socket, addr))
        client_thread.start()