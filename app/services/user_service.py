from flask.blueprints import Blueprint
from app.models.user import UserRepository
from app.services.auth_service import Auth
import pymysql
allowed_columns_user = frozenset(('name', 'gmail', 'password'))
user_bp = Blueprint('user', __name__, url_prefix = 'profile')
class User():
    def __init__(self):
        self.user_db = UserRepository()
        self.autenticacao = Auth()
    def edit_profile(self, column, dado, user_id) -> tuple[bool, str]:
        if column not in allowed_columns_user:
            return False, 'Coluna nao existente'
        if dado is None or column is None:
            return False, 'Nao pode haver campos vazios'
        if column == 'password':
            if len(dado) < 6:
                return False, 'Your passsword is too short'
            novo_dado = self.autenticacao.password_hash(dado)
            try:
                self.user_db.update_user(column, novo_dado, user_id)
                return True, 'Dado alterado com sucesso!'
            except ValueError:
                return False, 'Ocorreu um erro ao alterar suas informações!'
        if column == 'gmail':
            novo_dado = self.autenticacao.check_gmail(dado)
            if not novo_dado:
                return False, 'The email address you entered is incorrect'
            try:
                self.user_db.update_user(column, novo_dado, user_id)
                return True, 'Dado alterado com sucesso!'
            except ValueError:
                return False, f'Column {column} dont exist'
            except pymysql.err.IntegrityError:
                return False, 'Gmail already exists'
        if column == 'name':
            self.user_db.update_user(column, dado, user_id)
            return True, 'Dado alterado com sucesso!'