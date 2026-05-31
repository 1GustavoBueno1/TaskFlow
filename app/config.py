import pymysql
import os
from dotenv import load_dotenv
from pymysql.cursors import DictCursor
load_dotenv()
class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')
    if SECRET_KEY is None:
        raise RuntimeError('Secret key nãoo foi definida')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', '')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', '')
    DB_PORT = int(os.getenv('DB_PORT') or '3306')
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    @staticmethod
    def get_connection():
        connection = pymysql.connect(
            host = os.getenv('DB_HOST', 'localhost'),
            user = os.getenv('DB_USER', ''),
            password = os.getenv('DB_PASSWORD', ''),
            database = os.getenv('DB_NAME', ''),
            port = int(os.getenv('DB_PORT') or '3306'),
            charset = 'utf8mb4',
            cursorclass = DictCursor)
        return connection