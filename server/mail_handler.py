import os, datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def save_mail(recipient, from_addr, content):
    box = os.path.join(BASE_DIR, "data", "mailbox", recipient)
    os.makedirs(box, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(box, f"{ts}.eml")
    with open(path, "w") as f:
        f.write(f"From: {from_addr}\n")
        f.write(f"To: {recipient}\n")
        f.write(f"Date: {datetime.datetime.now()}\n\n")
        f.write(content)
    return path
