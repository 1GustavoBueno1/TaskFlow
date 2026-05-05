from app.config import Config
from flask import current_app
import pymysql


allowed_columns_user = frozenset(('name', 'gmail', 'password'))
class UserRepository:
    def __init__(self):
        self.connection_db = pymysql.connect(
            host=current_app.config['DB_HOST'],
            password=current_app.config['DB_PASSWORD'],
            name=current_app.config['DB_NAME'],
            user=current_app.config['DB_USER'],
            port=current_app.config['DB_PORT']
        )
    def create_table_users(self):
        with self.connection_db.get_connection() as connection:
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
    def insert(self, name: str, gmail: str, password: str) -> None:
        with self.connection_db.get_connection() as connection:
            with connection.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO Users '
                        '(name, gmail, password) VALUES (%s, %s, %s)', 
                        (name, gmail, password)
                    )
            connection.commit()
    def login(self, gmail: str) -> bool:
        with self.connection_db.get_connection() as connection:
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
        with self.connection_db.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f'UPDATE Users SET {column} = %s WHERE id = %s',
                    (new_data, id)
                )
                connection.commit()