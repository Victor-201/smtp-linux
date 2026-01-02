import base64, os, hashlib, hmac

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
USER_FILE = os.path.join(BASE_DIR, "config", "users.txt")

def sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()

def authenticate(user_b64, pass_b64):
    try:
        login = base64.b64decode(user_b64).decode().strip()
        password = base64.b64decode(pass_b64).decode().strip()
        pwd_hash = sha256(password)
        with open(USER_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if ":" not in line or line.startswith("#"):
                    continue
                username, stored, email = line.strip().split(":", 2)
                if login == username or login == email:
                    if hmac.compare_digest(pwd_hash, stored):
                        return True, {"username": username, "email": email}
                    return False, None
        return False, None
    except Exception:
        return False, None
