import os, datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_FILE = os.path.join(BASE_DIR, "logs", "smtp_server.log")

def log_event(ip="", from_addr="", to_addr="", auth_status="", message=""):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{ip}] [{from_addr}] [{to_addr}] [{auth_status}] {message}\n"
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line)
