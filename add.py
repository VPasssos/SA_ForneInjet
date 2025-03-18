from Config import get_connection

conn = get_connection()
cursor = conn.cursor()
query = """
INSERT INTO Funcionario (nome_funcionario, cargo, telefone, email, data_admissao, situacao, permissao, usuario, senha) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
cursor.execute(query, (1, 1, 1, 1, 1, 1, "nom", 1, 1))
conn.commit()
cursor.close()
conn.close()