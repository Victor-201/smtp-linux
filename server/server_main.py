import os
from server.socket_listener import start_listener

def load_config():
    cfg = {"HOST": "0.0.0.0", "PORT": 2525}
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "server.conf")
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    cfg[k] = v
    return cfg

if __name__ == "__main__":
    cfg = load_config()
    start_listener(cfg["HOST"], int(cfg["PORT"]))
