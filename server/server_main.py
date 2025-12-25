from server.socket_listener import start_listener
from server.smtp_parser import handle_client
from server.auth_handler import load_users

def load_config():
    config = {}
    with open("config/server.conf") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                config[k] = v
    config["SMTP_PORT"] = int(config["SMTP_PORT"])
    return config

def run():
    config = load_config()
    users = load_users("config/users.txt")
    server = start_listener(config["SMTP_PORT"])

    while True:
        conn, addr = server.accept()
        handle_client(conn, addr, config, users)
