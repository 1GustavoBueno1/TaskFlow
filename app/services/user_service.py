from app.models.user import UserRepository
from app.services.auth_service import Autenticacao
import pymysql


MAPA_CAMPOS_USUARIO = frozenset({'name', 'gmail', 'password'})


class Usuario:
    def __init__(self) -> None:
        self.banco_usuario = UserRepository()
        self.autenticacao = Autenticacao()

    def editar_perfil(self, campo: str, dado: str, user_senha:str ,id_usuario: int, usuario) -> tuple[bool, str]:
        if dado is None or campo is None:
            return False, 'Não pode haver campos vazios'
        if not self.autenticacao.verificar_senha(user_senha, usuario['password']):
            return False, 'senha incorreta, para alterar informações, digite sua senha corretamente'
        if campo is None:
            return False, f'Campo {campo} não existe'
        if campo == 'password':
            if len(dado) < 6:
                return False, 'Sua senha é muito curta'
            novo_dado = self.autenticacao.gerar_hash_senha(dado)
            try:
                self.banco_usuario.update_user(campo, novo_dado, id_usuario)
                return True, 'Dado alterado com sucesso!'
            except ValueError:
                return False, 'Ocorreu um erro ao alterar suas informações!'
        if campo == 'gmail':
            novo_dado = self.autenticacao.validar_email(dado)
            if not novo_dado:
                return False, 'O email informado é inválido'
            try:
                self.banco_usuario.update_user(campo, novo_dado, id_usuario)
                return True, 'Dado alterado com sucesso!'
            except ValueError:
                return False, f'Campo {campo} não existe'
            except pymysql.err.IntegrityError:
                return False, 'Email já cadastrado'
        if campo == 'name':
            self.banco_usuario.update_user(campo, dado, id_usuario)
            return True, 'Dado alterado com sucesso!'
        return False, 'Não foi possível atualizar o perfil'
