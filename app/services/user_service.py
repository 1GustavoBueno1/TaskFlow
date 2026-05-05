from  pymysql.err import IntegrityError
from flask.blueprints import Blueprint

user_bp = Blueprint('user', __name__, url_prefix = 'profile')
class User():
    def view_profile(self) -> tuple[bool, str]:
        if self.user_logged:
            return True, f'ID = {self.user_logged['id']} | Name = {self.user_logged['name']} | Email = {self.user_logged['gmail']}'
        return False, 'Carry out login to check your informations!'
    def edit_profile(self) -> tuple[bool, str]:
        if self.user_logged:
            result = self.ui.edit_profile()
            if result is None:
                return False, 'Invalid option'
            colum, data = result
            if data is None:
                return False, 'Field cannot be empty' 
            if colum == 'password':
                if len(data) < 6:
                    return False, 'Your passsword is too short'
                data = bcrypt.hashpw(data.encode(), bcrypt.gensalt()).decode('utf-8')
            if colum == 'gmail':
                data = self.check_gmail(data)
                if not data:
                    return False, 'The email address you entered is incorrect'
            try:
                self.data_base.update_user(colum, data, self.user_logged['id'])
                self.user_logged[colum] = data
                return True, 'Success when updating the information'
            except ValueError:
                return False, f'Column {colum} dont exist'
            except IntegrityError:
                return False, 'Gmail already exists'
        return False, 'Carry out login for update your informations!'
    def password_hash(self):
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')