import sqlite3
from datetime import datetime

def ADD_VENDA(id_cliente, id_funcionario, data_venda, forma_pagamento, total_brl, total_usd, observacoes):
    # Conecta ao banco de dados
    conn = sqlite3.connect('sua_base_de_dados.db')
    cursor = conn.cursor()

    # Insere uma nova venda
    query = """
        INSERT INTO vendas (id_cliente, id_funcionario, data_venda, forma_pagamento, total_brl, total_usd, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (id_cliente, id_funcionario, data_venda, forma_pagamento, total_brl, total_usd, observacoes))

    # Confirma a transação
    conn.commit()

    # Fecha a conexão
    conn.close()
def ADD_ITEM_VENDA(id_venda, id_injetora, quantidade, preco_brl, preco_usd):
    # Conecta ao banco de dados
    conn = sqlite3.connect('sua_base_de_dados.db')
    cursor = conn.cursor()

    # Insere um item na venda
    query = """
        INSERT INTO itens_venda (id_venda, id_injetora, quantidade, preco_brl, preco_usd)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(query, (id_venda, id_injetora, quantidade, preco_brl, preco_usd))

    # Confirma a transação
    conn.commit()

    # Fecha a conexão
    conn.close()
def GET_CLIENTES():
    # Conecta ao banco de dados
    conn = sqlite3.connect('sua_base_de_dados.db')
    cursor = conn.cursor()

    # Busca todos os clientes
    query = "SELECT * FROM clientes"
    cursor.execute(query)

    # Obtém todos os resultados
    clientes = cursor.fetchall()

    # Fecha a conexão
    conn.close()

    return clientes
def GET_INJETORAS():
    # Conecta ao banco de dados
    conn = sqlite3.connect('sua_base_de_dados.db')
    cursor = conn.cursor()

    # Busca todas as injetoras
    query = "SELECT * FROM injetoras"
    cursor.execute(query)

    # Obtém todos os resultados
    injetoras = cursor.fetchall()

    # Fecha a conexão
    conn.close()

    return injetoras
