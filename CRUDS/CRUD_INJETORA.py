from tkinter import messagebox
from CONFIG import get_connection

def ADD_INJETORA(entries, fornecedor_cb, tree_injetoras):
    conn = get_connection()
    cursor = conn.cursor() 
    
    # Obter ID do fornecedor selecionado
    nome_fornecedor = fornecedor_cb.get()
    cursor.execute("SELECT ID_Fornecedor FROM Fornecedor WHERE NM_Fornecedor = %s", (nome_fornecedor,))
    id_fornecedor = cursor.fetchone()
    
    # Inserir nova injetora
    query = """
    INSERT INTO Injetora (marca, modelo, tipo_de_controle, capacidade_de_injecao, 
                         forca_de_fechamento, preco_medio_USD, preco_medio_BRL, 
                         quantidade, observacao, ID_Fornecedor)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        entries["Marca"].get(),
        entries["Modelo"].get(),
        entries["Tipo de Controle"].get(),
        float(entries["Capacidade de Injeção (g)"].get()),
        float(entries["Força de Fechamento (ton)"].get()),
        float(entries["Preço Médio (USD)"].get()),
        float(entries["Preço Médio (BRL)"].get()),
        int(entries["Quantidade"].get()),
        entries["Observações"].get(),
        id_fornecedor
    )
    
    cursor.execute(query, valores)
    conn.commit()
    messagebox.showinfo("Sucesso", "Injetora cadastrada com sucesso!")
    UPD_TABELA_IJETORA(tree_injetoras)
    cursor.close()
    conn.close()

def DEL_INJETORA(injetora_id, tree):
    id_inj = injetora_id.get()
    if not id_inj:
        messagebox.showwarning("Aviso", "Selecione uma injetora para excluir!")
        return
        
    resposta = messagebox.askyesno("Confirmar", "Deseja realmente excluir esta injetora?")
    if resposta:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM Injetora WHERE ID_Injetora = %s", (id_inj,))
        conn.commit()
        
        messagebox.showinfo("Sucesso", "Injetora excluída com sucesso!")
        UPD_TABELA_IJETORA(tree)
        cursor.close()
        conn.close()

def UPD_INJETORA(entries, fornecedor_cb, injetora_id, tree):
    id_inj = injetora_id.get()
    if not id_inj:
        messagebox.showwarning("Aviso", "Selecione uma injetora para atualizar!")
        return
        
    conn = get_connection()
    cursor = conn.cursor()
    
    # Obter ID do fornecedor selecionado
    nome_fornecedor = fornecedor_cb.get()
    cursor.execute("SELECT ID_Fornecedor FROM Fornecedor WHERE NM_Fornecedor = %s", (nome_fornecedor,))
    id_fornecedor = cursor.fetchone()[0]
    
    # Atualizar injetora
    query = """
    UPDATE Injetora SET 
        marca = %s,
        modelo = %s,
        tipo_de_controle = %s,
        capacidade_de_injecao = %s,
        forca_de_fechamento = %s,
        preco_medio_USD = %s,
        preco_medio_BRL = %s,
        quantidade = %s,
        observacao = %s,
        ID_Fornecedor = %s
    WHERE ID_Injetora = %s
    """
    valores = (
        entries["Marca"].get(),
        entries["Modelo"].get(),
        entries["Tipo de Controle"].get(),
        float(entries["Capacidade de Injeção (g)"].get()),
        float(entries["Força de Fechamento (ton)"].get()),
        float(entries["Preço Médio (USD)"].get()),
        float(entries["Preço Médio (BRL)"].get()),
        int(entries["Quantidade"].get()),
        entries["Observações"].get(),
        id_fornecedor,
        id_inj
    )
    
    cursor.execute(query, valores)
    conn.commit()
    messagebox.showinfo("Sucesso", "Injetora atualizada com sucesso!")
    UPD_TABELA_IJETORA(tree)
    cursor.close()
    conn.close()

def UPD_TABELA_IJETORA(tree):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Limpar a treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Buscar injetoras com informações de fornecedores
    query = """
    SELECT i.*, f.NM_Fornecedor 
    FROM Injetora i
    LEFT JOIN Fornecedor f ON i.ID_Fornecedor = f.ID_Fornecedor
    """
    cursor.execute(query)
    injetoras = cursor.fetchall()
    
    # Preencher a treeview
    for inj in injetoras:
        tree.insert("", "end", values=(
            inj["ID_Injetora"],
            inj["marca"],
            inj["modelo"],
            inj["tipo_de_controle"],
            inj["capacidade_de_injecao"],
            inj["forca_de_fechamento"],
            inj["preco_medio_USD"],
            inj["preco_medio_BRL"],
            inj["quantidade"],
            inj["NM_Fornecedor"],
            inj["observacao"]
        ))
        
    cursor.close()
    conn.close()

def UPD_CAMPOS_INJETORA(entries, fornecedor_cb, injetora_id, id_inj, fornecedores):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Buscar dados da injetora
    query = """
    SELECT i.*, f.NM_Fornecedor 
    FROM Injetora i
    LEFT JOIN Fornecedor f ON i.ID_Fornecedor = f.ID_Fornecedor
    WHERE i.ID_Injetora = %s
    """
    cursor.execute(query, (id_inj,))
    inj = cursor.fetchone()
    
    if inj:
        # Preencher os campos
        entries["Marca"].delete(0, "end")
        entries["Marca"].insert(0, inj["marca"])
        
        entries["Modelo"].delete(0, "end")
        entries["Modelo"].insert(0, inj["modelo"])
        
        entries["Tipo de Controle"].delete(0, "end")
        entries["Tipo de Controle"].insert(0, inj["tipo_de_controle"])
        
        entries["Capacidade de Injeção (g)"].delete(0, "end")
        entries["Capacidade de Injeção (g)"].insert(0, str(inj["capacidade_de_injecao"]))
        
        entries["Força de Fechamento (ton)"].delete(0, "end")
        entries["Força de Fechamento (ton)"].insert(0, str(inj["forca_de_fechamento"]))
        
        entries["Preço Médio (USD)"].delete(0, "end")
        entries["Preço Médio (USD)"].insert(0, str(inj["preco_medio_USD"]))
        
        entries["Preço Médio (BRL)"].delete(0, "end")
        entries["Preço Médio (BRL)"].insert(0, str(inj["preco_medio_BRL"]))
        
        entries["Quantidade"].delete(0, "end")
        entries["Quantidade"].insert(0, str(inj["quantidade"]))
        
        entries["Observações"].delete(0, "end")
        entries["Observações"].insert(0, inj["observacao"] if inj["observacao"] else "")
        
        # Configurar o combobox do fornecedor
        fornecedor_cb.set(inj["NM_Fornecedor"])
        
        # Atualizar o ID da injetora
        injetora_id.delete(0, "end")
        injetora_id.insert(0, str(inj["ID_Injetora"]))
        
    cursor.close()
    conn.close()