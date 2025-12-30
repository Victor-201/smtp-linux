from .socket_listener import start_listener
from .smtp_parser import handle_client
import configparser
import os

def main():
    config = configparser.ConfigParser()
    config.read("../config/server.conf")
    
    host = config["server"]["host"]
    port = int(config["server"]["port"])
    
    os.makedirs("../data/mailbox", exist_ok=True)
    os.makedirs("../logs", exist_ok=True)
    
    start_listener(host, port, handle_client)

if __name__ == "__main__":
    main()