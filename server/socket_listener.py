import socket
import sys

def start_listener(port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", port))
        server.listen(5)

        print("=" * 60)
        print("[SMTP SERVER] Server started")
        print(f"[SMTP SERVER] Listening on port {port}")
        print("=" * 60)

        return server
    except Exception as e:
        print("[ERROR] Cannot start server:", e)
        sys.exit(1)
