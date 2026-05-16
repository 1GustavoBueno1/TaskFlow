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

    def verificar_senha(self, senha: str, usuario: dict) -> bool:
        return bcrypt.checkpw(senha.encode(), usuario['password'].encode())

    def cadastrar_usuario(self, nome: str, email: str, senha: str) -> tuple[bool, str]:
        if not nome:
            return False, "O campo nome não pode estar vazio"
        if len(senha) < 6:
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
        if self.verificar_senha(senha, usuario):
            self.logs.sucesso(f"Login realizado com sucesso: {email}")
            return usuario, "Login realizado com sucesso"
        self.logs.erro(f"Acesso negado: {email}")
        return None, "Credenciais inválidas!"
