from app.models.user import UserRepository
from Logs.savelogs import SalvarLog
import bcrypt
import re


_EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@gmail\.com$')


class Autenticacao:
    def __init__(self) -> None:
        self.banco_dados = UserRepository()
        self.logs = SalvarLog()

    def validar_email(self, email: str) -> str | bool:
        if _EMAIL_REGEX.fullmatch(email):
            return email
        return False

    def gerar_hash_senha(self, senha: str) -> str:
        return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode('utf-8')

    def verificar_senha(self, senha: str, usuario_password: str) -> bool:
        if senha is None or usuario_password is None:
            return False
        return bcrypt.checkpw(senha.encode(), usuario_password.encode())

    def cadastrar_usuario(self, nome: str, email: str, senha: str) -> tuple[bool, str]:
        if nome is None or not nome.strip() or email is None or senha is None:
            return False, "Não pode haver campos em branco"
        if len(nome) > 20:
            return False, 'Nome nao pode ser muito longo'
        if len(senha) < 8:
            return False, "Sua senha é muito curta!"
        if not self.validar_email(email):
            return False, "Insira um email válido"
        try:
            senha_hash = self.gerar_hash_senha(senha)
            self.banco_dados.insert(nome, email, senha_hash)
            self.logs.sucesso(f"Cadastro realizado: {email}")
            return True, "Cadastro realizado com sucesso, Efetue login!"
        except ValueError:
            return False, "Email já existente!"

    def login(self, email: str, senha: str) -> tuple[dict | None, str]:
        if not email or not senha:
            return None, "Não pode haver campos em branco!"
        usuario = self.banco_dados.login(email)
        if not usuario:
            return None, "Credenciais inválidas!"
        if self.verificar_senha(senha, usuario['password']):
            self.logs.sucesso(f"Login realizado com sucesso: {email}")
            return usuario, "Login realizado com sucesso"
        self.logs.erro(f"Acesso negado: {email}")
        return None, "Credenciais inválidas!"
    
    def sair(self, senha_user: str, senha_correta: dict):
        if senha_correta is None or senha_user is None:
            return False, 'Não pode haver campos em branco'
        if self.verificar_senha(senha_user, senha_correta['password']):
            return True, 'Logout efetuado com sucesso'
        return False, 'Algo deu errado, tente novamente'
