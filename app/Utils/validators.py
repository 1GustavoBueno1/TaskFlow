import bcrypt
import re


_EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@gmail\.com$')
class Validators():
    def validate_gmail(self, gmail) -> bool | str:
        if _EMAIL_REGEX.fullmatch(gmail):
            return gmail
        return False
    def validate_password():
        bcrypt.checkpw(password.encode(), user['password'].encode())
    def validate_name():
        ...