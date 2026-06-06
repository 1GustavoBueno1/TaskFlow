"""
Testes da camada de perfil de usuário (app/services/user_service.py).

O repositório de usuários e a autenticação são mockados. Por padrão a
fixture deixa a verificação de senha retornando True; os testes que
precisam do caminho de "senha incorreta" sobrescrevem esse valor.
"""
from unittest.mock import MagicMock

import pytest

from app.services.user_service import Usuario


USUARIO = {"id": 1, "name": "Gustavo", "gmail": "gustavo@gmail.com", "password": "hash"}


@pytest.fixture
def usuario_service():
    servico = Usuario()
    servico.banco_usuario = MagicMock()
    servico.autenticacao = MagicMock()
    servico.autenticacao.verificar_senha.return_value = True  # senha confere por padrão
    return servico


# --- validações iniciais ---------------------------------------------------

@pytest.mark.parametrize("campo,dado,senha", [
    (None, "x", "senha"),
    ("name", None, "senha"),
    ("name", "x", None),
])
def test_editar_perfil_campos_vazios(usuario_service, campo, dado, senha):
    ok, msg = usuario_service.editar_perfil(campo, dado, senha, 1, USUARIO)
    assert ok is False
    assert msg == 'Não pode haver campos vazios'


@pytest.mark.parametrize("id_usuario,usuario", [
    (None, USUARIO),
    (1, None),
])
def test_editar_perfil_sem_login(usuario_service, id_usuario, usuario):
    ok, msg = usuario_service.editar_perfil("name", "Novo", "senha", id_usuario, usuario)
    assert ok is False
    assert msg == 'Efetue login novamente para prosseguir'


def test_editar_perfil_senha_incorreta(usuario_service):
    usuario_service.autenticacao.verificar_senha.return_value = False
    ok, msg = usuario_service.editar_perfil("name", "Novo", "senha-errada", 1, USUARIO)
    assert ok is False
    assert 'senha incorreta' in msg
    usuario_service.banco_usuario.update_user.assert_not_called()


# --- alterar nome ----------------------------------------------------------

def test_editar_perfil_nome_sucesso(usuario_service):
    ok, msg = usuario_service.editar_perfil("name", "Novo Nome", "senha", 1, USUARIO)
    assert ok is True
    assert msg == 'Dado alterado com sucesso!'
    usuario_service.banco_usuario.update_user.assert_called_once_with("name", "Novo Nome", 1)


# --- alterar senha ---------------------------------------------------------

def test_editar_perfil_senha_nova_muito_curta(usuario_service):
    ok, msg = usuario_service.editar_perfil("password", "1234567", "senha", 1, USUARIO)
    assert ok is False
    assert msg == 'Sua senha é muito curta'
    usuario_service.banco_usuario.update_user.assert_not_called()


def test_editar_perfil_senha_nova_sucesso(usuario_service):
    usuario_service.autenticacao.gerar_hash_senha.return_value = "novo-hash"
    ok, msg = usuario_service.editar_perfil("password", "senhanova123", "senha", 1, USUARIO)
    assert ok is True
    assert msg == 'Dado alterado com sucesso!'
    usuario_service.autenticacao.gerar_hash_senha.assert_called_once_with("senhanova123")
    # grava o hash, nunca a senha em texto puro
    usuario_service.banco_usuario.update_user.assert_called_once_with("password", "novo-hash", 1)


# --- alterar gmail ---------------------------------------------------------

def test_editar_perfil_email_invalido(usuario_service):
    usuario_service.autenticacao.validar_email.return_value = False
    ok, msg = usuario_service.editar_perfil("gmail", "invalido", "senha", 1, USUARIO)
    assert ok is False
    assert msg == 'O email informado é inválido'
    usuario_service.banco_usuario.update_user.assert_not_called()


def test_editar_perfil_email_sucesso(usuario_service):
    usuario_service.autenticacao.validar_email.return_value = "novo@gmail.com"
    ok, msg = usuario_service.editar_perfil("gmail", "novo@gmail.com", "senha", 1, USUARIO)
    assert ok is True
    assert msg == 'Dado alterado com sucesso!'
    usuario_service.banco_usuario.update_user.assert_called_once_with("gmail", "novo@gmail.com", 1)


# --- campo não reconhecido -------------------------------------------------

def test_editar_perfil_campo_desconhecido(usuario_service):
    ok, msg = usuario_service.editar_perfil("admin", "true", "senha", 1, USUARIO)
    assert ok is False
    assert msg == 'Não foi possível atualizar o perfil'
    usuario_service.banco_usuario.update_user.assert_not_called()
