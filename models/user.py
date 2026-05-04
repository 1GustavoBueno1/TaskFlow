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
allowed_columns_user = frozenset(('name', 'gmail', 'password'))
class UserRepository:
    def create_table_users(self):
        with get_connection() as connection:
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
        with get_connection() as connection:
            with connection.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO Users '
                        '(name, gmail, password) VALUES (%s, %s, %s)', 
                        (name, gmail, password)
                    )
            connection.commit()
    def login(self, gmail: str) -> bool:
        with get_connection() as connection:
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
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f'UPDATE Users SET {column} = %s WHERE id = %s',
                    (new_data, id)
                )
                connection.commit()