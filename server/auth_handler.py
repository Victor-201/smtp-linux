import base64
import os

USERS_FILE = "../config/users.txt"

def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and ":" in line:
                    username, password = line.split(":", 1)
                    users[username] = password
    return users

USERS = load_users()

def authenticate(username_b64, password_b64):
    try:
        username = base64.b64decode(username_b64).decode("utf-8").strip()
        password = base64.b64decode(password_b64).decode("utf-8").strip()
        if username in USERS and USERS[username] == password:
            return True, username
        else:
            return False, ""
    except:
        return False, ""