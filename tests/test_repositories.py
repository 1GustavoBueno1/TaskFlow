"""
Testes dos repositórios (app/models).

Aqui validamos a "allowlist" de colunas em update_user/update_task — a
proteção contra injeção de SQL no NOME da coluna (que não pode ser
parametrizada pelo driver). O ValueError é levantado ANTES de qualquer
acesso ao banco, então estes testes rodam sem conexão com o MySQL.

Os métodos que de fato executam SQL (insert, find, show_tasks, etc.)
exigem um banco real e ficam fora do escopo destes testes unitários —
seriam cobertos por testes de integração com um MySQL de teste.
"""
import pytest

from app.models.task import TaskRepository
from app.models.user import UserRepository


@pytest.mark.parametrize("coluna", [
    "id",
    "admin",
    "senha",
    "name; DROP TABLE Users",
])
def test_update_user_rejeita_coluna_nao_permitida(coluna):
    repo = UserRepository()
    with pytest.raises(ValueError):
        repo.update_user(coluna, "valor", 1)

@pytest.mark.parametrize("coluna", [
    "id",
    "user_id",
    "status; DROP TABLE Tasks",
])
def test_update_task_rejeita_coluna_nao_permitida(coluna):
    repo = TaskRepository()
    with pytest.raises(ValueError):
        repo.update_task(coluna, "valor", 1, 1)
