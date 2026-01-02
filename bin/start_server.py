#!/usr/bin/env python3
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from server.server_main import load_config
from server.socket_listener import start_listener

if __name__ == "__main__":
    config = load_config()
    start_listener(config["HOST"], int(config["PORT"]))
