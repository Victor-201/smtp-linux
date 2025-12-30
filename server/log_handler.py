import datetime
import os

LOG_FILE = "../logs/smtp_server.log"

def log_event(ip, from_addr="", to_addr="", auth_status="", message=""):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        log_line = f"[{timestamp}] [IP:{ip}] [FROM:{from_addr}] [TO:{to_addr}] [AUTH:{auth_status}] {message}\n"
        f.write(log_line)