import mysql.connector

from Config import get_connection
def create_user(nome_funcionario,telefone,email,cargo,departamento,data_addmissao,situacao,permicao):
    conn = get_connection()
    cursor = conn.cursor()
    query = "insert funcionario(nome_funcionario,telefone,email,cargo,departamento,data_addmissao,situacao,permicao)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query,(nome_funcionario,telefone,email,cargo,departamento,data_addmissao,situacao,permicao))
    conn.commit()
    cursor.close()
    conn.close()

def read_users():  
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM funcionario"
    cursor.execute(query)
    result= cursor.fetchall()
    cursor.close()
    conn.close()
    return result 

def update_user(idfuncionario,nome_funcionario,telefone,email,cargo,departamento,data_addmissao,situacao,permicao):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE funcionario SET nome_funcionario=%s,telefone=%s,email=%s,cargo=%s,departamento=%s,data_admissao=%s,situacao=%s,permicao=%s WHERE idfuncionario= %s"
    cursor.execute(query,(nome_funcionario,telefone,email,cargo,departamento,data_addmissao,situacao,permicao,idfuncionario))
    conn.commit()
    cursor.close()
    conn.close()

    
def delete_user(idfuncionario,nome_funcionario,telefone,email,cargo,departamento,data_addmissao,situacao,permicao):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM funcionario WHERE idfuncionario = %s"
    cursor.execute(query,(idfuncionario))
    conn.commit()
    cursor.close()
    conn.close()
    
class Database:
    def __init__(self):
        # Conecta ao banco de dados MySQL com as credenciais fornecidas
        self.conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "ForneInjet_SA"
        )
        self.cursor = self.conn.cursor() # Cria um cursor para executar comandos SQL
        # Tabela "funcionario" se ela naõ existir
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS funcionario(
                            idfuncionario INT AUTO_INCREMENT PRIMARY KEY,
                            nome_funcionario TEXT(255),
                            email TEXT(255),
                            telefone TEXT(255),
                            cargo TEXT(255),
                            departamento TEXT(255),
                            data_admissao TEXT(255),
                            situacao TEXT(255),
                            permicao TEXT(255)
                            );''')
                           
        self.conn.commit() # Confirma criação da tabela


        print("conectado ao banco de Dados")
    # Metodo chamado quando a instancia da classe é destruida
    def __del__(self):
        self.conn.close() # Fecha a conexao com o banco