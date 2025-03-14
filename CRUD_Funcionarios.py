import mysql.connector
from Config import get_connection

def create_funcionario(nome_funcionario, telefone, email, cargo, data_admissao, situacao, permissao, usuario, senha):
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO funcionario (nome_funcionario, telefone, email, cargo, data_admissao, situacao, permissao, usuario, senha)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (nome_funcionario, telefone, email, cargo, data_admissao, situacao, permissao, usuario, senha))
    conn.commit()
    cursor.close()
    conn.close()

def read_funcionario():  
    #conn = get_connection()
    #cursor = conn.cursor()
    #query = "SELECT * FROM funcionario"
    #cursor.execute(query)
    #result = cursor.fetchall()
    #cursor.close()
    #conn.close()
    #return result

    # Obtém a conexão com o banco de dados
    conn = get_connection()
    
    try:
        # Cria um cursor para executar comandos SQL
        cursor = conn.cursor()
        
        # Define a consulta SQL para selecionar todos os registros da tabela 'funcionario'
        query = "SELECT * FROM funcionario"
        
        # Executa a consulta SQL
        cursor.execute(query)
        
        # Obtém todos os resultados da consulta
        result = cursor.fetchall()
        
        return result  # Retorna os resultados da consulta
    
    except Exception as e:
        # Em caso de erro, pode-se logar ou mostrar a exceção
        print(f"Erro ao executar a consulta: {e}")
        return None
    
    finally:
        # Garante que o cursor e a conexão sejam fechados, mesmo em caso de erro
        cursor.close()
        conn.close() 

def update_funcionario(idfuncionario, nome_funcionario, telefone, email, cargo, data_admissao, situacao, permissao, usuario, senha):
    conn = get_connection()
    cursor = conn.cursor()
    query = """UPDATE funcionario
               SET nome_funcionario=%s, telefone=%s, email=%s, cargo=%s, data_admissao=%s, situacao=%s, permissao=%s,usuario=%s,senha=%s
               WHERE idfuncionario=%s"""
    cursor.execute(query, (nome_funcionario, telefone, email, cargo, data_admissao, situacao, permissao, usuario, senha, idfuncionario))
    conn.commit()
    cursor.close()
    conn.close()

def delete_funcionario(idfuncionario):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM funcionario WHERE idfuncionario = %s"
    cursor.execute(query, (idfuncionario,))
    conn.commit()
    cursor.close()
    conn.close()

class Database:
    def __init__(self):
        # Conecta ao banco de dados MySQL com as credenciais fornecidas
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ForneInjet_SA"
        )
        self.cursor = self.conn.cursor()  # Cria um cursor para executar comandos SQL
        
        # Criação da tabela "funcionario", se ela não existir
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS funcionario (
                                idFuncionario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                nome_funcionario TEXT,
                                email TEXT,
                                telefone TEXT,
                                cargo TEXT,
                                data_admissao DATE,  # Ou altere para DATE, se necessário
                                situacao TEXT,
                                permissao TEXT,
                                usuario TEXT,
                                senha TEXT
                            );''')
        self.conn.commit()  # Confirma criação da tabela
        print("Conectado ao banco de dados")

    # Método chamado quando a instância da classe é destruída
    def close_connection(self):
        self.conn.close()  # Fecha a conexão com o banco de dados
