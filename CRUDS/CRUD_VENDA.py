from CONFIG import get_connection
from datetime import datetime
# ======================
# FUNÇÃO: GET_CLIENTES
# ======================
def GET_CLIENTES():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT ID_Cliente, nome FROM Cliente")
        clientes = cursor.fetchall()
        cursor.close()
        conn.close()
        return clientes
    except Exception as e:
        print(f"[ERRO - GET_CLIENTES] {e}")
        return []

# ======================
# FUNÇÃO: GET_INJETORAS
# ======================
def GET_INJETORAS():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Injetora, marca, modelo FROM Injetora")
        injetoras = cursor.fetchall()
        cursor.close()
        conn.close()
        return injetoras
    except Exception as e:
        print(f"[ERRO - GET_INJETORAS] {e}")
        return []


# ======================
# FUNÇÃO: ADD_VENDA
# ======================
def ADD_VENDA(ID_Cliente, ID_Funcionario, data_venda, forma_pagamento, valor_total_BRL, valor_total_USD, observacoes):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Venda (ID_Cliente, ID_Funcionario, data_venda, forma_pagamento, valor_total_BRL, valor_total_USD, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        valores = (ID_Cliente, ID_Funcionario, data_venda, forma_pagamento, valor_total_BRL, valor_total_USD, observacoes)
        cursor.execute(query, valores)
        conn.commit()
        venda_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return venda_id
    except Exception as e:
        print(f"[ERRO - ADD_VENDA] {e}")
        return None

# ======================
# FUNÇÃO: ADD_ITEM_VENDA
# ======================
def ADD_ITEM_VENDA(ID_Venda, ID_Injetora, quantidade, preco_unitario_BRL, preco_unitario_USD):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO ItemVenda (ID_Venda, ID_Injetora, quantidade, preco_unitario_BRL, preco_unitario_USD)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (ID_Venda, ID_Injetora, quantidade, preco_unitario_BRL, preco_unitario_USD)
        cursor.execute(query, valores)

        # Atualiza o estoque da injetora
        cursor.execute(
            "UPDATE Injetora SET quantidade = quantidade - %s WHERE ID_Injetora = %s",
            (quantidade, ID_Injetora)
        )

        # Insere log de saída de estoque
        cursor.execute(
            """
            INSERT INTO LogEstoque (ID_Injetora, tipo_movimento, quantidade, origem, id_origem, ID_Funcionario)
            VALUES (%s, 'saida', %s, 'Venda', %s, %s)
            """,
            (ID_Injetora, quantidade, ID_Venda, 2)  # 2 como exemplo do funcionário responsável
        )

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"[ERRO - ADD_ITEM_VENDA] {e}")
        return False
