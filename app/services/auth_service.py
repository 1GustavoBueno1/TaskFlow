from app.models.user import UserRepository
from Logs.savelogs import SaveLog
import bcrypt
import re

_EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@gmail\.com$')
class Auth:
    def __init__(self):
        self.data_base = UserRepository()
        self.logs = SaveLog()
    def check_gmail(self, gmail) -> bool | str:
        if _EMAIL_REGEX.fullmatch(gmail):
            return gmail
        return False
    def password_hash(self, password):
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
        return password_hash

    def check_password(self, password):
        bcrypt.checkpw(password.encode(), user['password'].encode())
    def register_user(self, name, email, password) -> tuple[bool, str]:
            if not name:
                return False, "The name field cannot be empty"
            if len(password) < 6:
                return False, "Your password is too short!"
            if not self.check_gmail(email):
                return False, 'Insira um email valido'
            try:
                password_hash = self.password_hash(password)
                self.data_base.insert(name, email, password_hash)
                self.logs.success(f"Register completed: {email}")
                return True, 'User registration successfull'
            except ValueError:
                return False, "Email ja existente!"
    def login(self) -> tuple[bool, str]:
        gmail, password = self.ui.login()
        user = self.data_base.login(gmail)
        if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
            self.user_logged = user
            self.logs.success(f"Success to login: {gmail}")
            return True, 'Success to carry out login'
        self.logs.error(f"Access deined: {gmail}")
        return False, 'Error to carry out login, check your credentials and try again!\n'