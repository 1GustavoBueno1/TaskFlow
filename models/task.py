import pymysql
import os
from dotenv import load_dotenv
from pymysql.cursors import DictCursor
load_dotenv()
def get_connection():
    connection = pymysql.connect(
        host = os.getenv('DB_HOST', 'localhost'),
        user = os.getenv('DB_USER', ''),
        password = os.getenv('DB_PASSWORD', ''),
        database = os.getenv('DB_NAME', ''),
        port = int(os.getenv('DB_PORT', '3307')),
        charset = 'utf8mb4',
        cursorclass = DictCursor)
    return connection
allowed_columns_task = frozenset(('name', 'description', 'status'))
class TaskRepository():
    def create_table_tasks(self):
            with get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SHOW TABLES LIKE 'Tasks' ")
                    if not cursor.fetchall():
                        cursor.execute(
                            'CREATE TABLE IF NOT EXISTS Tasks('
                            'id INT NOT NULL AUTO_INCREMENT,' \
                            'name VARCHAR(150) NOT NULL, ' \
                            'description VARCHAR(150),' \
                            'status VARCHAR(50) DEFAULT "Outstanding", ' \
                            'user_id INT NOT NULL, ' \
                            'PRIMARY KEY (id), ' \
                            'CONSTRAINT fk_user_id FOREIGN KEY (user_id) ' \
                            'REFERENCES Users(id) ' \
                            'ON DELETE CASCADE ON UPDATE CASCADE)'
                        )
                        connection.commit()
    def insert_task(self, name: str, description: str, user_id : int) -> None:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO Tasks (name, description, user_id) '
                    'VALUES (%s, %s, %s)',
                    (name, description, user_id)
                )
                connection.commit()
    def show_tasks(self, id: int) -> tuple[str] | bool:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT id, name, description, status FROM Tasks WHERE user_id = %s',
                    (id, )
                )
                tasks = cursor.fetchall()
                if tasks:
                    return tasks
                return False
    def update_task(self, column: str, new_data: str, user_id: int, task_id: int) -> None:

        if column not in allowed_columns_task:
            raise ValueError(f'Column {column} dont exist')
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f'UPDATE Tasks SET {column} = %s WHERE id = %s and user_id = %s',
                    (new_data, task_id, user_id)
                )
                connection.commit()
    def del_task(self, user_id: int, task_id: int) -> int:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f'DELETE FROM Tasks WHERE user_id = %s AND id = %s',
                    (user_id, task_id)
                )
                connection.commit()
                return cursor.rowcount > 0