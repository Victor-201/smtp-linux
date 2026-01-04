from server.auth_handler import authenticate
from server.mail_handler import save_mail
from server.log_handler import log_event

STATE_INIT = 0
STATE_AUTH_USER = 1
STATE_AUTH_PASS = 2
STATE_MAIL = 3
STATE_RCPT = 4
STATE_DATA = 5

class SMTPParser:
    def __init__(self, ip):
        self.ip = ip
        self.reset()

    def reset(self):
        self.state = STATE_INIT
        self.authenticated = False
        self.user = None
        self.from_addr = ""
        self.to_addrs = []
        self.data = []
        self.user_b64 = ""

    def process_command(self, line):
        line = line.rstrip("\r\n")
        if not line:
            return None
        cmd = line.split(" ", 1)[0].upper()

        if cmd == "HELO":
            return "250 OK"

        if cmd == "AUTH" and line.upper() == "AUTH LOGIN":
            self.state = STATE_AUTH_USER
            return "334 VXNlcm5hbWU6"

        if self.state == STATE_AUTH_USER:
            self.user_b64 = line
            self.state = STATE_AUTH_PASS
            return "334 UGFzc3dvcmQ6"

        if self.state == STATE_AUTH_PASS:
            ok, user = authenticate(self.user_b64, line)
            if ok:
                self.user = user
                self.from_addr = user["email"]
                self.authenticated = True
                self.state = STATE_MAIL
                log_event(ip=self.ip, auth_status="LOGIN", message=f"{user['username']} <{user['email']}>")
                return ("235 Authentication successful\r\n"f"From: {user['email']}\r\n")
            log_event(ip=self.ip, auth_status="FAILED")
            self.reset()
            return "535 Authentication failed"

        if cmd == "MAIL":
            if not self.authenticated:
                return "530 Authentication required"
            self.state = STATE_RCPT
            return "250 OK"

        if cmd == "RCPT" and self.state == STATE_RCPT:
            rcpt = line.split(":", 1)[1].strip().strip("<>")
            self.to_addrs.append(rcpt)
            return "250 OK"

        if cmd == "DATA" and self.state == STATE_RCPT:
            self.data = []
            log_event(ip=self.ip, from_addr=self.from_addr, to_addr=",".join(self.to_addrs), auth_status="SENDING")
            self.state = STATE_DATA
            return "354 End data with <CRLF>.<CRLF>"

        if self.state == STATE_DATA:
            if line == ".":
                content = "\n".join(self.data)
                for r in self.to_addrs:
                    save_mail(r, self.from_addr, content)
                    log_event(ip=self.ip, from_addr=self.from_addr, to_addr=r, auth_status="DELIVERED")
                self.reset()
                return "250 OK"
            self.data.append(line)
            return None

        if cmd == "QUIT":
            if self.user:
                log_event(ip=self.ip, auth_status="LOGOUT", message=self.user["username"])
            return "221 Bye"

        return "500 Command not recognized"
