import mysql.connector
from mysql.connector import Error

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DATABASE = "ForneInjet"

def get_connection():
    """Estabelece conexão com o banco de dados"""
    try:
        connection = mysql.connector.connect(
            host= MYSQL_HOST,
            database= MYSQL_DATABASE,
            user= MYSQL_USER,
            password= MYSQL_PASSWORD
        )
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# Codigo para executar o projeto:
# pip install mysql-connector-python    