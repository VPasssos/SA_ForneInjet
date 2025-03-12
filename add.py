from Config import get_connection

conn = get_connection()
cursor = conn.cursor()
query = """INSERT INTO funcionario (nome_funcionario, telefone, email, cargo, data_admissao, situacao, permissao, usuario, senha)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
cursor.execute(query, (1, 1, 1, 1, 1, 1, 1, 1, 1))
conn.commit()
cursor.close()
conn.close()