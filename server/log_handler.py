from datetime import datetime

def log_event(log_file, ip, sender, recipient, status):
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{time_str}] [{ip}] [{sender}] [{recipient}] [{status}]\n"

    with open(log_file, "a") as f:
        f.write(log_line)
