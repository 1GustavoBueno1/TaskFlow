from app.config import Config
import pymysql


allowed_columns_user = frozenset(('name', 'gmail', 'password'))
class UserRepository:
    def create_table_users(self):
        with Config.get_connection() as connection:
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
    def find(self, informa):
        with Config.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT id, name, gmail FROM Users WHERE id = %s',
                    (informa, )
                )
                user_id = cursor.fetchone()
                return user_id
    def insert(self, name: str, gmail: str, password: str) -> None:
        try:
            with Config.get_connection() as connection:
                with connection.cursor() as cursor:
                        cursor.execute(
                            'INSERT INTO Users'
                            '(name, gmail, password) VALUES (%s, %s, %s)', 
                            (name, gmail, password)
                        )
                connection.commit()
        except pymysql.err.IntegrityError:
            raise ValueError("Email ja existente")
    def login(self, gmail: str) -> dict:
        with Config.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT id, name, gmail, password FROM Users WHERE gmail = %s',
                    (gmail, )
                )
                user_login = cursor.fetchone()
                return user_login
    def update_user(self, column: str, new_data: str, id: int) -> None:
        if column not in allowed_columns_user:
            raise ValueError(f'Column {column} dont exist!')
        with Config.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f'UPDATE Users SET {column} = %s WHERE id = %s',
                    (new_data, id)
                )
                connection.commit()