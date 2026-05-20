from app.models.task import TaskRepository


MAPA_CAMPOS_TAREFA = frozenset(['name', 'description', 'status'])


class Tarefas:
    def __init__(self) -> None:
        self.banco_tarefa = TaskRepository()

    def listar_tarefas(self, id_usuario: int) -> tuple[bool, str | list]:
        tarefas = self.banco_tarefa.show_tasks(id_usuario)
        if tarefas:
            return tarefas
        return False

    def editar_tarefas(self, campo: str, novo_dado: str, id_tarefa: int, id_usuario: int) -> tuple[bool, str]:
        if campo is None or novo_dado is None or id_tarefa is None or id_usuario is None:
            return False, 'Não pode haver campos em branco!'
        if campo not in MAPA_CAMPOS_TAREFA:
            return False, f'Campo {campo} não existe'
        try:
            self.banco_tarefa.update_task(campo, novo_dado, id_usuario, id_tarefa)
            return True, 'Tarefa atualizada com sucesso!'
        except ValueError:
            return False, f'Campo {campo} não existe'

    def deletar_tarefa(self, id_tarefa: int, id_usuario: int) -> tuple[bool, str]:
        if id_tarefa is None or id_usuario is None:
            return False, 'Não pode haver campos em branco!'
        linhas_afetadas = self.banco_tarefa.del_task(id_usuario, id_tarefa)
        if linhas_afetadas >= 1:
            return True, 'Tarefa deletada com sucesso!'
        return False, 'Não foi possível deletar essa tarefa'

    def criar_tarefa(self, nome: str, descricao: str, id_usuario: int) -> tuple[bool, str]:
        if nome is None or id_usuario is None or descricao is None:
            return False, 'Não pode haver campos em branco!'
        self.banco_tarefa.insert_task(nome, descricao, id_usuario)
        return True, 'Tarefa criada com sucesso'
