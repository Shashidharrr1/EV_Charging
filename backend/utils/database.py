import mysql.connector
from backend.config import Config  # Use absolute import with package name

class Database:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )