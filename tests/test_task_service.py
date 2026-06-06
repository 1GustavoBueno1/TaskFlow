"""
Testes da camada de tarefas (app/services/task_service.py).

O repositório de tarefas e a autenticação são mockados, então não há
acesso ao MySQL nem hashing real de senha.
"""
from unittest.mock import MagicMock

import pytest

from app.services.task_service import Tarefas


@pytest.fixture
def tarefas():
    servico = Tarefas()
    servico.banco_tarefa = MagicMock()
    servico.auth = MagicMock()
    return servico


# --- listar_tarefas --------------------------------------------------------

def test_listar_tarefas_sem_id(tarefas):
    assert tarefas.listar_tarefas(None) == (False, 'Efetue login novamete para prosseguir')


def test_listar_tarefas_com_resultados(tarefas):
    lista = [{"id": 1, "name": "Estudar", "description": "pytest", "status": "pendente"}]
    tarefas.banco_tarefa.show_tasks.return_value = lista
    assert tarefas.listar_tarefas(1) == lista


def test_listar_tarefas_sem_resultados(tarefas):
    tarefas.banco_tarefa.show_tasks.return_value = False
    assert tarefas.listar_tarefas(1) is False


# --- editar_tarefas --------------------------------------------------------

@pytest.mark.parametrize("campo,novo_dado,id_tarefa,id_usuario", [
    (None, "x", 1, 1),
    ("name", None, 1, 1),
    ("name", "x", None, 1),
    ("name", "x", 1, None),
])
def test_editar_tarefa_campos_em_branco(tarefas, campo, novo_dado, id_tarefa, id_usuario):
    ok, msg = tarefas.editar_tarefas(campo, novo_dado, id_tarefa, id_usuario)
    assert ok is False
    assert msg == 'Não pode haver campos em branco!'


def test_editar_tarefa_campo_invalido(tarefas):
    ok, msg = tarefas.editar_tarefas("coluna_inexistente", "x", 1, 1)
    assert ok is False
    assert msg == 'Campo coluna_inexistente não existe'
    tarefas.banco_tarefa.update_task.assert_not_called()


def test_editar_tarefa_status_invalido(tarefas):
    ok, msg = tarefas.editar_tarefas("status", "em_andamento", 1, 1)
    assert ok is False
    assert msg == 'em_andamento não e uma das opções'
    tarefas.banco_tarefa.update_task.assert_not_called()


@pytest.mark.parametrize("status", ["pendente", "concluida"])
def test_editar_tarefa_status_valido(tarefas, status):
    ok, msg = tarefas.editar_tarefas("status", status, 5, 7)
    assert ok is True
    assert msg == 'Tarefa atualizada com sucesso!'
    # o service repassa (campo, novo_dado, id_usuario, id_tarefa) ao repositório
    tarefas.banco_tarefa.update_task.assert_called_once_with("status", status, 7, 5)


def test_editar_tarefa_nome_sucesso(tarefas):
    ok, msg = tarefas.editar_tarefas("name", "Novo nome", 10, 20)
    assert ok is True
    assert msg == 'Tarefa atualizada com sucesso!'
    tarefas.banco_tarefa.update_task.assert_called_once_with("name", "Novo nome", 20, 10)


def test_editar_tarefa_repositorio_levanta_valueerror(tarefas):
    tarefas.banco_tarefa.update_task.side_effect = ValueError
    ok, msg = tarefas.editar_tarefas("name", "x", 1, 1)
    assert ok is False
    assert msg == 'Campo name não existe'


# --- deletar_tarefa --------------------------------------------------------

def test_deletar_tarefa_id_em_branco(tarefas):
    ok, msg = tarefas.deletar_tarefa(None, 1, {"password": "hash"}, "senha")
    assert ok is False
    assert msg == 'Não pode haver campos em branco!'


def test_deletar_tarefa_usuario_ou_senha_none(tarefas):
    ok, msg = tarefas.deletar_tarefa(1, 1, None, "senha")
    assert ok is False
    assert msg == 'Não pode haver campos em branco!'


def test_deletar_tarefa_senha_incorreta(tarefas):
    tarefas.auth.verificar_senha.return_value = False
    ok, msg = tarefas.deletar_tarefa(1, 1, {"password": "hash"}, "senha-errada")
    assert ok is False
    assert msg == 'Senha incorreta'
    tarefas.banco_tarefa.del_task.assert_not_called()


def test_deletar_tarefa_sucesso(tarefas):
    tarefas.auth.verificar_senha.return_value = True
    tarefas.banco_tarefa.del_task.return_value = 1
    ok, msg = tarefas.deletar_tarefa(3, 7, {"password": "hash"}, "senha-correta")
    assert ok is True
    assert msg == 'Tarefa deletada com sucesso!'
    # del_task recebe (id_usuario, id_tarefa)
    tarefas.banco_tarefa.del_task.assert_called_once_with(7, 3)


def test_deletar_tarefa_nenhuma_linha_afetada(tarefas):
    tarefas.auth.verificar_senha.return_value = True
    tarefas.banco_tarefa.del_task.return_value = 0
    ok, msg = tarefas.deletar_tarefa(3, 7, {"password": "hash"}, "senha-correta")
    assert ok is False
    assert msg == 'Não foi possível deletar essa tarefa'


# --- criar_tarefa ----------------------------------------------------------

@pytest.mark.parametrize("nome,descricao,id_usuario", [
    (None, "desc", 1),
    ("nome", None, 1),
    ("nome", "desc", None),
])
def test_criar_tarefa_campos_em_branco(tarefas, nome, descricao, id_usuario):
    ok, msg = tarefas.criar_tarefa(nome, descricao, id_usuario)
    assert ok is False
    assert msg == 'Não pode haver campos em branco!'
    tarefas.banco_tarefa.insert_task.assert_not_called()


def test_criar_tarefa_sucesso(tarefas):
    ok, msg = tarefas.criar_tarefa("Estudar", "pytest", 42)
    assert ok is True
    assert msg == 'Tarefa criada com sucesso'
    tarefas.banco_tarefa.insert_task.assert_called_once_with("Estudar", "pytest", 42)
