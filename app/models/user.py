from app.config import Config
import pymysql


COLUNAS_PERMITIDAS_USUARIO = frozenset(('name', 'gmail', 'password'))


class UserRepository:
    def create_table_users(self) -> None:
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

    def find(self, id_usuario: int) -> dict | None:
        with Config.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT id, name, gmail, password FROM Users WHERE id = %s',
                    (id_usuario,)
                )
                return cursor.fetchone()

    def insert(self, nome: str, email: str, senha: str) -> None:
        try:
            with Config.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO Users (name, gmail, password) VALUES (%s, %s, %s)',
                        (nome, email, senha)
                    )
                connection.commit()
        except pymysql.err.IntegrityError:
            raise ValueError("Email já existente")

    def login(self, email: str) -> dict | None:
        with Config.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT id, name, gmail, password FROM Users WHERE gmail = %s',
                    (email,)
                )
                return cursor.fetchone()

    def update_user(self, coluna: str, novo_dado: str, id_usuario: int) -> None:
        if coluna not in COLUNAS_PERMITIDAS_USUARIO:
            raise ValueError(f'Coluna {coluna} não existe!')
        with Config.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f'UPDATE Users SET {coluna} = %s WHERE id = %s',
                    (novo_dado, id_usuario)
                )
                connection.commit()
