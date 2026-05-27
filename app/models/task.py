from app.config import Config


COLUNAS_PERMITIDAS_TAREFA = frozenset(('name', 'description', 'status'))


class TaskRepository:
    def create_table_tasks(self) -> None:
        with Config.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SHOW TABLES LIKE 'Tasks' ")
                if not cursor.fetchall():
                    cursor.execute(
                        'CREATE TABLE IF NOT EXISTS Tasks('
                        'id INT NOT NULL AUTO_INCREMENT,'
                        'name VARCHAR(150) NOT NULL, '
                        'description VARCHAR(150),'
                        'status VARCHAR(50) DEFAULT "pendente", '
                        'user_id INT NOT NULL, '
                        'PRIMARY KEY (id), '
                        'CONSTRAINT fk_user_id FOREIGN KEY (user_id) '
                        'REFERENCES Users(id) '
                        'ON DELETE CASCADE ON UPDATE CASCADE)'
                    )
                    connection.commit()

    def insert_task(self, nome: str, descricao: str, id_usuario: int) -> None:
        with Config.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO Tasks (name, description, user_id) VALUES (%s, %s, %s)',
                    (nome, descricao, id_usuario)
                )
                connection.commit()

    def show_tasks(self, id_usuario: int) -> list | bool:
        with Config.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT id, name, description, status FROM Tasks WHERE user_id = %s',
                    (id_usuario,)
                )
                tarefas = cursor.fetchall()
                if tarefas:
                    return tarefas
                return False

    def update_task(self, coluna: str, novo_dado: str, id_usuario: int, id_tarefa: int) -> None:
        if coluna not in COLUNAS_PERMITIDAS_TAREFA:
            raise ValueError(f'Coluna {coluna} não existe')
        with Config.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f'UPDATE Tasks SET {coluna} = %s WHERE id = %s and user_id = %s',
                    (novo_dado, id_tarefa, id_usuario)
                )
                connection.commit()

    def del_task(self, id_usuario: int, id_tarefa: int) -> int:
        with Config.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'DELETE FROM Tasks WHERE user_id = %s AND id = %s',
                    (id_usuario, id_tarefa)
                )
                connection.commit()
                return cursor.rowcount
