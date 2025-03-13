from Config import get_connection

conn = get_connection()
cursor = conn.cursor()
query = """INSERT INTO Produto (tipo, marca, modelo, capacidade_de_injeçao, força_de_fechamento, tipo_de_controle, preço_medio_USD, preço_medio_BRL, fornecedor, observacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
cursor.execute(query, (1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
conn.commit()
cursor.close()
conn.close()