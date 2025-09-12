from tkinter import messagebox
from CONFIG import get_connection

def ADD_INJETORA(entries, fornecedor_cb, tree_injetoras):
    """Adiciona uma nova injetora ao banco de dados e atualiza a tabela de exibição"""
    try:
        # Estabelece conexão com o banco de dados
        conn = get_connection()
        cursor = conn.cursor()
        
        # Obtém o ID do fornecedor selecionado no combobox
        nome_fornecedor = fornecedor_cb.get()
        cursor.execute("SELECT ID_Fornecedor FROM Fornecedor WHERE NM_Fornecedor = %s", (nome_fornecedor,))
        id_fornecedor = cursor.fetchone()
        
        # Verifica se o fornecedor existe
        if id_fornecedor is None:
            messagebox.showerror("Erro", "Fornecedor não encontrado!")
            return
            
        id_fornecedor = id_fornecedor[0]

        # Query SQL para inserir nova injetora
        query = """
        INSERT INTO Injetora (marca, modelo, tipo_de_controle, capacidade_de_injecao, 
                             forca_de_fechamento, preco_medio_BRL, 
                             quantidade, observacao, ID_Fornecedor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Prepara os valores a serem inseridos a partir dos campos de entrada
        valores = (
            entries["Marca"].get(),
            entries["Modelo"].get(),
            entries["Tipo de Controle"].get(),
            int(entries["Capacidade de Injeção (g)"].get()),  # Converte para inteiro
            int(entries["Força de Fechamento (ton)"].get()),  # Converte para inteiro
            float(entries["Preço Médio (BRL)"].get()),       # Converte para float
            int(entries["Quantidade"].get()),                # Converte para inteiro
            entries["Observações"].get(),
            id_fornecedor
        )
        
        # Executa a query e faz commit
        cursor.execute(query, valores)
        conn.commit()
        messagebox.showinfo("Sucesso", "Injetora cadastrada com sucesso!")
        
        # Atualiza a tabela de exibição e limpa os campos
        UPD_TABELA_IJETORA(tree_injetoras)
        LIMPAR_CAMPOS(entries)
        
    except Exception as e:
        # Tratamento de erros genéricos
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
    finally:
        # Fecha conexões se existirem
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()
        
def DEL_INJETORA(injetora_id, tree):
    """Remove uma injetora do banco de dados, incluindo itens de venda associados"""
    id_inj = injetora_id.get()
    
    # Verifica se foi selecionada uma injetora
    if not id_inj:
        messagebox.showwarning("Aviso", "Selecione uma injetora para excluir!")
        return
        
    # Confirmação de exclusão
    resposta = messagebox.askyesno("Confirmar", "Deseja realmente excluir esta injetora? Esta ação também excluirá todos os itens de venda associados.")
    if resposta:
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Primeiro exclui os itens de venda associados (integridade referencial)
            cursor.execute("DELETE FROM ItemVenda WHERE ID_Injetora = %s", (id_inj,))
            
            # Depois exclui a injetora
            cursor.execute("DELETE FROM Injetora WHERE ID_Injetora = %s", (id_inj,))
            
            conn.commit()
            messagebox.showinfo("Sucesso", "Injetora e itens associados excluídos com sucesso!")
            UPD_TABELA_IJETORA(tree)
            
        except Exception as e:
            # Rollback em caso de erro
            if conn:
                conn.rollback()
            messagebox.showerror("Erro", f"Ocorreu um erro ao excluir: {str(e)}")
        finally:
            # Fecha conexões
            if cursor:
                cursor.close()
            if conn:
                conn.close()

def UPD_INJETORA(entries, fornecedor_cb, injetora_id, tree):
    """Atualiza os dados de uma injetora existente"""
    id_inj = injetora_id.get()
    
    # Verifica se foi selecionada uma injetora
    if not id_inj:
        messagebox.showwarning("Aviso", "Selecione uma injetora para atualizar!")
        return
        
    conn = get_connection()
    cursor = conn.cursor()
    
    # Obtém o ID do fornecedor selecionado
    nome_fornecedor = fornecedor_cb.get()
    cursor.execute("SELECT ID_Fornecedor FROM Fornecedor WHERE NM_Fornecedor = %s", (nome_fornecedor,))
    id_fornecedor = cursor.fetchone()[0]
    
    # Query SQL para atualização
    query = """
    UPDATE Injetora SET 
        marca = %s,
        modelo = %s,
        tipo_de_controle = %s,
        capacidade_de_injecao = %s,
        forca_de_fechamento = %s,
        preco_medio_BRL = %s,
        quantidade = %s,
        observacao = %s,
        ID_Fornecedor = %s
    WHERE ID_Injetora = %s
    """
    # Valores para atualização
    valores = (
        entries["Marca"].get(),
        entries["Modelo"].get(),
        entries["Tipo de Controle"].get(),
        int(entries["Capacidade de Injeção (g)"].get()),
        int(entries["Força de Fechamento (ton)"].get()),
        float(entries["Preço Médio (BRL)"].get()),
        int(entries["Quantidade"].get()),
        entries["Observações"].get(),
        id_fornecedor,
        id_inj
    )
    
    # Executa a atualização
    cursor.execute(query, valores)
    conn.commit()
    messagebox.showinfo("Sucesso", "Injetora atualizada com sucesso!")
    
    # Atualiza a tabela e limpa os campos
    UPD_TABELA_IJETORA(tree)
    LIMPAR_CAMPOS(entries)
    cursor.close()
    conn.close()

def UPD_TABELA_IJETORA(tree):
    """Atualiza a tabela de exibição com todas as injetoras cadastradas"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Limpa todos os itens atuais da treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Query para buscar injetoras com informações de fornecedores (LEFT JOIN)
    query = """
    SELECT i.*, f.NM_Fornecedor 
    FROM Injetora i
    LEFT JOIN Fornecedor f ON i.ID_Fornecedor = f.ID_Fornecedor
    """
    cursor.execute(query)
    injetoras = cursor.fetchall()
    
    # Preenche a treeview com os dados atualizados
    for inj in injetoras:
        tree.insert("", "end", values=(
            inj["ID_Injetora"],
            inj["marca"],
            inj["modelo"],
            inj["tipo_de_controle"],
            inj["capacidade_de_injecao"],
            inj["forca_de_fechamento"],
            inj["preco_medio_BRL"],
            inj["quantidade"],
            inj["NM_Fornecedor"],
            inj["observacao"]
        ))
        
    cursor.close()
    conn.close()

def UPD_CAMPOS_INJETORA(entries, fornecedor_cb, injetora_id, id_inj, fornecedores):
    """Preenche os campos do formulário com os dados de uma injetora selecionada"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Busca os dados da injetora selecionada
    query = """
    SELECT i.*, f.NM_Fornecedor 
    FROM Injetora i
    LEFT JOIN Fornecedor f ON i.ID_Fornecedor = f.ID_Fornecedor
    WHERE i.ID_Injetora = %s
    """
    cursor.execute(query, (id_inj,))
    inj = cursor.fetchone()
    
    if inj:
        # Preenche cada campo do formulário com os dados da injetora
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
        
        entries["Preço Médio (BRL)"].delete(0, "end")
        entries["Preço Médio (BRL)"].insert(0, str(inj["preco_medio_BRL"]))
        
        entries["Quantidade"].delete(0, "end")
        entries["Quantidade"].insert(0, str(inj["quantidade"]))
        
        entries["Observações"].delete(0, "end")
        entries["Observações"].insert(0, inj["observacao"] if inj["observacao"] else "")
        
        # Configura o combobox do fornecedor com o valor correto
        fornecedor_cb.set(inj["NM_Fornecedor"])
        
        # Atualiza o campo do ID da injetora
        injetora_id.delete(0, "end")
        injetora_id.insert(0, str(inj["ID_Injetora"]))
        
    cursor.close()
    conn.close()

def GET_INJETORA():
    """Obtém lista de todas as injetoras (ID e modelo) ordenadas por modelo"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT ID_Injetora, modelo FROM injetora ORDER BY modelo")
    clientes = cursor.fetchall()
    
    conn.close()
    return clientes

def LIMPAR_CAMPOS(entries):
    """Limpa todos os campos do formulário"""
    for entry in entries.values():
        entry.delete(0, "end")