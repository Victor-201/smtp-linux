import os
import datetime

MAILBOX_DIR = "../data/mailbox"

def save_mail(recipient, sender, data_content):
    user_dir = os.path.join(MAILBOX_DIR, recipient)
    os.makedirs(user_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.eml"
    filepath = os.path.join(user_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"From: {sender}\n")
        f.write(f"To: {recipient}\n")
        f.write(f"Date: {datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S')}\n")
        f.write(data_content)
    
    return filepath