from tkinter import messagebox
from CONFIG import get_connection

def ADD_VENDA(entries, cliente_cb, produto_cb_venda, tree_vendas, funcionario_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Obter o ID do funcionário (tratando se for Entry widget)
        if hasattr(funcionario_id, 'get'):
            funcionario_id = funcionario_id.get()
        if not funcionario_id:
            messagebox.showwarning("Aviso", "Funcionário não identificado!")
            return
        try:
            funcionario_id = int(funcionario_id)
        except ValueError:
            messagebox.showwarning("Aviso", "ID do funcionário inválido!")
            return

        # Obter ID do cliente
        nome_cliente = cliente_cb.get()
        cursor.execute("SELECT ID_Cliente FROM Cliente WHERE nome = %s", (nome_cliente,))
        id_cliente = cursor.fetchone()
        if not id_cliente:
            messagebox.showwarning("Aviso", "Cliente não encontrado!")
            return

        # Obter ID do produto
        nome_produto = produto_cb_venda.get()
        cursor.execute("SELECT ID_Injetora FROM Injetora WHERE modelo = %s", (nome_produto,))
        id_produto = cursor.fetchone()
        if not id_produto:
            messagebox.showwarning("Aviso", "Produto não encontrado!")
            return

        # Inserir nova venda
        query = """
        INSERT INTO Venda (data_venda, valor_total_BRL, valor_total_USD, 
                        status_aprovacao, ID_Cliente, ID_Funcionario, observacoes, forma_pagamento)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            entries["Data Venda"].get(),
            float(entries["Preço Unitário (BRL)"].get()),
            float(entries["Preço Unitário (USA)"].get()),
            entries["Status Aprovação"].get(),
            id_cliente[0],
            funcionario_id,
            entries["Observações"].get(),
            entries["Forma Pagamento"].get()
        )

        cursor.execute(query, valores)
        id_venda = cursor.lastrowid

        # Inserir item da venda
        query_item = """
        INSERT INTO ItemVenda (ID_Venda, ID_Injetora, quantidade, 
                            preco_unitario_BRL, preco_unitario_USD)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores_item = (
            id_venda,
            id_produto[0],
            int(entries["Quantidade"].get()),
            float(entries["Preço Unitário (BRL)"].get()),
            float(entries["Preço Unitário (USA)"].get())
        )

        cursor.execute(query_item, valores_item)
        conn.commit()

        messagebox.showinfo("Sucesso", "Venda cadastrada com sucesso!")
        UPD_TABELA_VENDAS(tree_vendas)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao cadastrar a venda:\n{str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def DEL_VENDA(venda_id, tree):
    id_venda = venda_id.get()
    if not id_venda:
        messagebox.showwarning("Aviso", "Selecione uma venda para excluir!")
        return

    resposta = messagebox.askyesno("Confirmar", "Deseja realmente excluir esta venda?")
    if resposta:
        conn = get_connection()
        cursor = conn.cursor()

        # Primeiro excluir os itens da venda
        cursor.execute("DELETE FROM ItemVenda WHERE ID_Venda = %s", (id_venda,))
        # Depois excluir a venda
        cursor.execute("DELETE FROM Venda WHERE ID_Venda = %s", (id_venda,))
        conn.commit()

        messagebox.showinfo("Sucesso", "Venda excluída com sucesso!")
        UPD_TABELA_VENDAS(tree)
        cursor.close()
        conn.close()

def UPD_VENDA(entries, cliente_cb, venda_id, tree, funcionario_id):
    try:
        id_venda = venda_id.get()
        if not id_venda:
            messagebox.showwarning("Aviso", "Selecione uma venda para atualizar!")
            return

        if hasattr(funcionario_id, 'get'):
            funcionario_id = funcionario_id.get()
        if not funcionario_id:
            messagebox.showwarning("Aviso", "Funcionário não identificado!")
            return
        try:
            funcionario_id = int(funcionario_id)
        except ValueError:
            messagebox.showwarning("Aviso", "ID do funcionário inválido!")
            return

        conn = get_connection()
        cursor = conn.cursor()

        # Obter ID do cliente
        nome_cliente = cliente_cb.get()
        cursor.execute("SELECT ID_Cliente FROM Cliente WHERE nome = %s", (nome_cliente,))
        resultado_cliente = cursor.fetchone()
        if not resultado_cliente:
            messagebox.showwarning("Aviso", "Cliente não encontrado!")
            return
        id_cliente = resultado_cliente[0]

        # Obter ID do produto
        nome_produto = entries["Produto"].get()
        cursor.execute("SELECT ID_Injetora FROM Injetora WHERE modelo = %s", (nome_produto,))
        resultado_produto = cursor.fetchone()
        if not resultado_produto:
            messagebox.showwarning("Aviso", "Produto não encontrado!")
            return
        id_produto = resultado_produto[0]

        # Limpar resultados pendentes do SELECT de funcionário, caso necessário
        cursor.execute("SELECT nome FROM Funcionario WHERE ID_Funcionario = %s", (funcionario_id,))
        _ = cursor.fetchone()

        # Atualizar tabela Venda
        query = """
        UPDATE Venda SET 
            data_venda = %s,
            valor_total_BRL = %s,
            valor_total_USD = %s,
            status_aprovacao = %s,
            ID_Cliente = %s,
            observacoes = %s,
            forma_pagamento = %s
        WHERE ID_Venda = %s
        """
        valores = (
            entries["Data Venda"].get(),
            float(entries["Preço Unitário (BRL)"].get()),
            float(entries["Preço Unitário (USA)"].get()),
            entries["Status Aprovação"].get(),
            id_cliente,
            entries["Observações"].get(),
            entries["Forma Pagamento"].get(),
            id_venda
        )
        cursor.execute(query, valores)

        # Atualizar tabela ItemVenda
        query_item = """
        UPDATE ItemVenda SET 
            ID_Injetora = %s,
            quantidade = %s,
            preco_unitario_BRL = %s,
            preco_unitario_USD = %s
        WHERE ID_Venda = %s
        """
        valores_item = (
            id_produto,
            int(entries["Quantidade"].get()),
            float(entries["Preço Unitário (BRL)"].get()),
            float(entries["Preço Unitário (USA)"].get()),
            id_venda
        )
        cursor.execute(query_item, valores_item)

        conn.commit()
        messagebox.showinfo("Sucesso", "Venda atualizada com sucesso!")
        UPD_TABELA_VENDAS(tree)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao atualizar a venda:\n{str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def UPD_TABELA_VENDAS(tree):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Limpar a treeview
    for item in tree.get_children():
        tree.delete(item)

    # Buscar vendas com informações completas
    query = """
    SELECT v.ID_Venda, c.nome AS cliente, i.modelo AS produto, 
        iv.quantidade, iv.preco_unitario_BRL, iv.preco_unitario_USD,
        v.data_venda, v.status_aprovacao, f.nome AS cadastrante, 
        v.observacoes, v.forma_pagamento
    FROM Venda v
    JOIN Cliente c ON v.ID_Cliente = c.ID_Cliente
    JOIN ItemVenda iv ON v.ID_Venda = iv.ID_Venda
    JOIN Injetora i ON iv.ID_Injetora = i.ID_Injetora
    JOIN Funcionario f ON v.ID_Funcionario = f.ID_Funcionario
    ORDER BY v.data_venda DESC
    """
    cursor.execute(query)
    vendas = cursor.fetchall()

    # Preencher a treeview
    for venda in vendas:
        tree.insert("", "end", values=(
            venda["ID_Venda"],
            venda["cliente"],
            venda["produto"],
            venda["quantidade"],
            venda["preco_unitario_BRL"],
            venda["preco_unitario_USD"],
            venda["data_venda"],
            venda["status_aprovacao"],
            venda["cadastrante"],
            venda["observacoes"]
        ))

    cursor.close()
    conn.close()

def UPD_CAMPOS_VENDA(entries, cliente_cb, venda_id, id_venda):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Buscar dados completos da venda
    query = """
    SELECT v.*, c.nome AS cliente, i.modelo AS produto, 
           iv.quantidade, iv.preco_unitario_BRL, iv.preco_unitario_USD,
           f.nome AS cadastrante
    FROM Venda v
    JOIN Cliente c ON v.ID_Cliente = c.ID_Cliente
    JOIN ItemVenda iv ON v.ID_Venda = iv.ID_Venda
    JOIN Injetora i ON iv.ID_Injetora = i.ID_Injetora
    JOIN Funcionario f ON v.ID_Funcionario = f.ID_Funcionario
    WHERE v.ID_Venda = %s
    """
    cursor.execute(query, (id_venda,))
    venda = cursor.fetchone()

    if venda:
        # Preencher os campos
        entries["Data Venda"].delete(0, "end")
        entries["Data Venda"].insert(0, venda["data_venda"])

        entries["Forma Pagamento"].delete(0, "end")
        entries["Forma Pagamento"].insert(0, str(venda["forma_pagamento"]))

        entries["Preço Unitário (BRL)"].delete(0, "end")
        entries["Preço Unitário (BRL)"].insert(0, str(venda["preco_unitario_BRL"]))

        entries["Preço Unitário (USA)"].delete(0, "end")
        entries["Preço Unitário (USA)"].insert(0, str(venda["preco_unitario_USD"]))

        entries["Quantidade"].delete(0, "end")
        entries["Quantidade"].insert(0, str(venda["quantidade"]))

        entries["Status Aprovação"].delete(0, "end")
        entries["Status Aprovação"].insert(0, venda["status_aprovacao"])

        entries["Cadastrante"].delete(0, "end")
        entries["Cadastrante"].insert(0, venda["cadastrante"])

        entries["Observações"].delete(0, "end")
        entries["Observações"].insert(0, venda["observacoes"])

        # Configurar os comboboxes
        cliente_cb.set(venda["cliente"])
        entries["Produto"].delete(0, "end")
        entries["Produto"].insert(0, venda["produto"])

        # Atualizar o ID da venda
        venda_id.delete(0, "end")
        venda_id.insert(0, str(venda["ID_Venda"]))

    cursor.close()
    conn.close()