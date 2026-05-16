from app.models.user import UserRepository
from app.services.auth_service import Autenticacao
import pymysql


MAPA_CAMPOS_USUARIO = {'nome': 'name', 'email': 'gmail', 'senha': 'password'}


class Usuario:
    def __init__(self) -> None:
        self.banco_usuario = UserRepository()
        self.autenticacao = Autenticacao()

    def editar_perfil(self, campo: str, dado: str, id_usuario: int) -> tuple[bool, str]:
        if dado is None or campo is None:
            return False, 'Não pode haver campos vazios'
        coluna = MAPA_CAMPOS_USUARIO.get(campo)
        if coluna is None:
            return False, f'Campo {campo} não existe'
        if coluna == 'password':
            if len(dado) < 6:
                return False, 'Sua senha é muito curta'
            novo_dado = self.autenticacao.gerar_hash_senha(dado)
            try:
                self.banco_usuario.update_user(coluna, novo_dado, id_usuario)
                return True, 'Dado alterado com sucesso!'
            except ValueError:
                return False, 'Ocorreu um erro ao alterar suas informações!'
        if coluna == 'gmail':
            novo_dado = self.autenticacao.validar_email(dado)
            if not novo_dado:
                return False, 'O email informado é inválido'
            try:
                self.banco_usuario.update_user(coluna, novo_dado, id_usuario)
                return True, 'Dado alterado com sucesso!'
            except ValueError:
                return False, f'Campo {campo} não existe'
            except pymysql.err.IntegrityError:
                return False, 'Email já cadastrado'
        if coluna == 'name':
            self.banco_usuario.update_user(coluna, dado, id_usuario)
            return True, 'Dado alterado com sucesso!'
        return False, 'Não foi possível atualizar o perfil'
