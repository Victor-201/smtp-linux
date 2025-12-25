import os
from datetime import datetime

def save_mail(mail_root, user, sender, recipient, content):
    user_dir = os.path.join(mail_root, user)
    os.makedirs(user_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(user_dir, f"{timestamp}.eml")

    with open(filepath, "w") as f:
        f.write(f"From: {sender}\n")
        f.write(f"To: {recipient}\n")
        f.write("Content-Type: text/plain\n\n")
        f.write(content)

    return filepath
