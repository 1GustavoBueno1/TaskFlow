import bcrypt
import re

_EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@gmail\.com$')
class auth():
    def check_gmail(self, gmail) -> bool | str:
        if _EMAIL_REGEX.fullmatch(gmail):
            return gmail
        return False
    # def password_hash(self):
    #     password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
    # def check_password():
    #     bcrypt.checkpw(.encode(), user['password'].encode())
    def register_user(self) -> tuple[bool, str]:
            name, gmail, password = self.ui.new_user()
            if not name:
                return False, "The name field cannot be empty"
            if len(password) < 6:
                return False, 'Your password is too short!'
            # try:
            #     if self.check_gmail(gmail):
            #         password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
            #         self.data_base.insert(name, gmail, password_hash)
            #         self.logs.success(f"Register completed: {gmail}")
            #         return True, 'User registration successfull'
            #     return False, 'The email address you entered is incorrect'
            #     return False, 'Gmail already exists'
    def login(self) -> tuple[bool, str]:
        gmail, password = self.ui.login()
        user = self.data_base.login(gmail)
        if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
            self.user_logged = user
            self.logs.success(f"Success to login: {gmail}")
            return True, 'Success to carry out login'
        self.logs.error(f"Access deined: {gmail}")
        return False, 'Error to carry out login, check your credentials and try again!\n'