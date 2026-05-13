from flask import session
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

    def check_password(self, password, user_password):
        if bcrypt.checkpw(password.encode(), user_password['password'].encode()):
            return True
        return False
        
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
    def login(self, email, password) -> tuple[bool, str]:
        if not email or not password:
            return None, "Nao pode haver campos em branco!"
        user = self.data_base.login(email)
        if not user:
            return None, "Credenciais invalidas!"
        if self.check_password(password, user):
            self.logs.success(f"Success to login: {email}")
            return user, 'Success to carry out login'
        self.logs.error(f"Access deined: {email}")
        return None, 'Credenciais invalidas!\n'