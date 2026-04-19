import pymysql
connection = pymysql.connect(
    host = 'localhost',
    user = 'Gustavo',
    password = 'ferreira3010@',
    database = 'Base_para_dados',
    port = 3307,
    charset = 'utf8mb4'
)
class UserRepository:
    def create_table_users(self):
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE 'Users' ")
            if not cursor.fetchall():
                cursor.execute(
                    'CREATE TABLE IF NOT EXISTS Users('
                    'id INT NOT NULL AUTO_INCREMENT, '
                    'name VARCHAR(50) NOT NULL, '
                    'gmail VARCHAR(100) NOT NULL, '
                    'password VARCHAR(255) NOT NULL, '
                    'PRIMARY KEY (id), ' 
                    'UNIQUE KEY (gmail)'
                    ')'
                )
                connection.commit()
    def create_table_tasks(self):
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE 'Tasks' ")
            if not cursor.fetchall():
                cursor.execute(
                    'CREATE TABLE IF NOT EXISTS Tasks('
                    'id INT NOT NULL AUTO_INCREMENT,' \
                    'name VARCHAR(150) NOT NULL, ' \
                    'description VARCHAR(150),' \
                    'status VARCHAR(50) DEFAULT "Pendente", ' \
                    'user_id INT NOT NULL, ' \
                    'PRIMARY KEY (id), ' \
                    'CONSTRAINT fk_user_id FOREIGN KEY (user_id) ' \
                    'REFERENCES Users(id) ' \
                    'ON DELETE CASCADE ON UPDATE CASCADE)'
                )
            connection.commit()
    def insert_task(self, name: str, description: str, user_id : int) -> None:
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO Tasks (name, description, user_id) '
                'VALUES (%s, %s, %s)',
                (name, description, user_id)
            )
            connection.commit()
    def show_tasks(self, id: int) -> tuple[str] | bool:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT id, name, description, status FROM Tasks WHERE user_id = %s',
                (id)
            )
            tasks = cursor.fetchall()
            if tasks:
                return tasks
            return False
    def insert(self, name: str, gmail: str, password: str) -> None:
        try:
            with connection:
                with connection.cursor() as cursor:
                        cursor.execute(
                            'INSERT INTO Users '
                            '(name, gmail, password) VALUES (%s, %s, %s)', # %s faz com que o sql não interprete as variaveis como comandos 
                            (name, gmail, password)
                        )
                connection.commit()
        except pymysql.err.IntegrityError:
            raise ValueError('Email already exists')
    def login(self, gmail: str) -> bool:
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT id, name, gmail, password FROM Users WHERE gmail = %s',
                (gmail)
            )
            user_login = cursor.fetchone()
            return user_login
    def update_user(self, column: str, new_data: str, id: int) -> None:
        with connection.cursor() as cursor:
            cursor.execute(
                f'UPDATE Users SET {column} = %s WHERE id = %s',
                (new_data, id)
            )
            connection.commit()
    def update_task(self, column: str, new_data: str, user_id: int, task_id: int) -> None:
        with connection.cursor() as cursor:
            cursor.execute(
                f'UPDATE Tasks SET {column} = %s WHERE id = %s and user_id = %s',
                (new_data, task_id, user_id)
            )
            connection.commit()