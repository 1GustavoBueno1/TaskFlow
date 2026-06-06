"""
Testes da camada de autenticação (app/services/auth_service.py).

O repositório (banco de dados) e os logs são substituídos por mocks, de
modo que estes testes NÃO precisam de uma conexão com o MySQL. O bcrypt
roda de verdade, validando o hashing e a verificação de senha.
"""
from unittest.mock import MagicMock

import pytest

from app.services.auth_service import Autenticacao


@pytest.fixture
def auth():
    """Autenticacao com repositório e logs mockados (não toca no banco)."""
    servico = Autenticacao()
    servico.banco_dados = MagicMock()
    servico.logs = MagicMock()
    return servico


# --- validar_email ---------------------------------------------------------

@pytest.mark.parametrize("email", [
    "gustavo@gmail.com",
    "gustavo.silva@gmail.com",
    "gustavo_123@gmail.com",
    "g+spam@gmail.com",
])
def test_validar_email_aceita_gmail_valido(auth, email):
    assert auth.validar_email(email) == email


@pytest.mark.parametrize("email", [
    "gustavo@yahoo.com",
    "gustavo@hotmail.com",
    "gustavo@gmail.com.br",
    "sem-arroba.com",
    "@gmail.com",
    "gustavo @gmail.com",
    "",
])
def test_validar_email_rejeita_invalidos(auth, email):
    assert auth.validar_email(email) is False


# --- hashing / verificação de senha ----------------------------------------

def test_gerar_hash_nao_retorna_senha_em_texto_puro(auth):
    senha = "minhasenha123"
    hash_gerado = auth.gerar_hash_senha(senha)
    assert hash_gerado != senha
    assert isinstance(hash_gerado, str)


def test_verificar_senha_correta(auth):
    senha = "minhasenha123"
    hash_gerado = auth.gerar_hash_senha(senha)
    assert auth.verificar_senha(senha, hash_gerado) is True


def test_verificar_senha_incorreta(auth):
    hash_gerado = auth.gerar_hash_senha("senha-correta")
    assert auth.verificar_senha("senha-errada", hash_gerado) is False


def test_verificar_senha_com_none_retorna_false(auth):
    assert auth.verificar_senha(None, "qualquer") is False
    assert auth.verificar_senha("qualquer", None) is False


# --- cadastrar_usuario ------------------------------------------------------

def test_cadastrar_usuario_sucesso(auth):
    ok, msg = auth.cadastrar_usuario("Gustavo", "gustavo@gmail.com", "senhaforte123")

    assert ok is True
    assert "sucesso" in msg.lower()
    auth.banco_dados.insert.assert_called_once()
    auth.logs.sucesso.assert_called_once()
    # a senha gravada deve ser o hash, nunca o texto puro
    nome, email, senha_gravada = auth.banco_dados.insert.call_args.args
    assert nome == "Gustavo"
    assert email == "gustavo@gmail.com"
    assert senha_gravada != "senhaforte123"


@pytest.mark.parametrize("nome,email,senha", [
    (None, "gustavo@gmail.com", "senhaforte123"),
    ("   ", "gustavo@gmail.com", "senhaforte123"),
    ("Gustavo", None, "senhaforte123"),
    ("Gustavo", "gustavo@gmail.com", None),
])
def test_cadastrar_usuario_campos_em_branco(auth, nome, email, senha):
    ok, msg = auth.cadastrar_usuario(nome, email, senha)

    assert ok is False
    assert msg == "Não pode haver campos em branco"
    auth.banco_dados.insert.assert_not_called()


def test_cadastrar_usuario_nome_muito_longo(auth):
    ok, msg = auth.cadastrar_usuario("G" * 21, "gustavo@gmail.com", "senhaforte123")
    assert ok is False
    assert msg == "Nome nao pode ser muito longo"


def test_cadastrar_usuario_senha_curta(auth):
    ok, msg = auth.cadastrar_usuario("Gustavo", "gustavo@gmail.com", "1234567")
    assert ok is False
    assert msg == "Sua senha é muito curta!"


def test_cadastrar_usuario_email_invalido(auth):
    ok, msg = auth.cadastrar_usuario("Gustavo", "gustavo@yahoo.com", "senhaforte123")
    assert ok is False
    assert msg == "Insira um email válido"


def test_cadastrar_usuario_email_duplicado(auth):
    # o repositório levanta ValueError quando o e-mail já existe
    auth.banco_dados.insert.side_effect = ValueError("Email já existente")
    ok, msg = auth.cadastrar_usuario("Gustavo", "gustavo@gmail.com", "senhaforte123")
    assert ok is False
    assert msg == "Email já existente!"


# --- login ------------------------------------------------------------------

def test_login_campos_em_branco(auth):
    usuario, msg = auth.login("", "")
    assert usuario is None
    assert msg == "Não pode haver campos em branco!"


def test_login_usuario_inexistente(auth):
    auth.banco_dados.login.return_value = None
    usuario, msg = auth.login("naoexiste@gmail.com", "senha123")
    assert usuario is None
    assert msg == "Credenciais inválidas!"


def test_login_sucesso(auth):
    senha = "senhaforte123"
    registro = {
        "id": 1,
        "name": "Gustavo",
        "gmail": "gustavo@gmail.com",
        "password": auth.gerar_hash_senha(senha),
    }
    auth.banco_dados.login.return_value = registro

    usuario, msg = auth.login("gustavo@gmail.com", senha)

    assert usuario == registro
    assert msg == "Login realizado com sucesso"
    auth.logs.sucesso.assert_called_once()


def test_login_senha_incorreta(auth):
    registro = {
        "id": 1,
        "name": "Gustavo",
        "gmail": "gustavo@gmail.com",
        "password": auth.gerar_hash_senha("senha-correta"),
    }
    auth.banco_dados.login.return_value = registro

    usuario, msg = auth.login("gustavo@gmail.com", "senha-errada")

    assert usuario is None
    assert msg == "Credenciais inválidas!"
    auth.logs.erro.assert_called_once()


# --- sair (confirmação de senha no logout) ----------------------------------

def test_sair_campos_em_branco(auth):
    ok, msg = auth.sair(None, {"password": "hash"})
    assert ok is False
    assert msg == "Não pode haver campos em branco"


def test_sair_senha_correta(auth):
    senha = "senhaforte123"
    usuario = {"password": auth.gerar_hash_senha(senha)}
    ok, msg = auth.sair(senha, usuario)
    assert ok is True
    assert msg == "Logout efetuado com sucesso"


def test_sair_senha_incorreta(auth):
    usuario = {"password": auth.gerar_hash_senha("senha-correta")}
    ok, msg = auth.sair("senha-errada", usuario)
    assert ok is False
    assert msg == "Algo deu errado, tente novamente"
