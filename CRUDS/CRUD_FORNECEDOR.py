from tkinter import messagebox
from CONFIG import get_connection

def ADD_FORNECEDOR(entries, tree_fornecedor, funcionario_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Validação de campos obrigatórios
        required_fields = ["Nome", "CNPJ"]
        for field in required_fields:
            if not entries[field].get().strip():
                messagebox.showerror("Erro", f"O campo {field} é obrigatório!")
                return
        
        # Inserir novo fornecedor
        query = """
        INSERT INTO Fornecedor (NM_Fornecedor, CNPJ, telefone, email, website, cadastrado_por)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (
            entries["Nome"].get(),
            entries["CNPJ"].get(),
            entries["Telefone"].get(),
            entries["E-mail"].get(),
            entries["Website"].get(),
            funcionario_id
        )
        
        cursor.execute(query, valores)
        id_fornecedor = cursor.lastrowid
        
        # Inserir endereço do fornecedor (se pelo menos um campo de endereço foi preenchido)
        if any(entries[field].get().strip() for field in ["Rua", "Número", "Bairro", "Cidade", "Estado", "CEP"]):
            query_end = """
            INSERT INTO EnderecoFornecedor (ID_Fornecedor, rua, numero, bairro, cidade, estado, cep)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores_end = (
                id_fornecedor,
                entries["Rua"].get(),
                entries["Número"].get(),
                entries["Bairro"].get(),
                entries["Cidade"].get(),
                entries["Estado"].get(),
                entries["CEP"].get()
            )
            cursor.execute(query_end, valores_end)
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso!")
        UPD_TABELA_FORNECEDOR(tree_fornecedor)
        LIMPAR_CAMPOS(entries)
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao cadastrar fornecedor: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def DEL_FORNECEDOR(fornecedor_id, tree):
    id_for = fornecedor_id.get()
    if not id_for:
        messagebox.showwarning("Aviso", "Selecione um fornecedor para excluir!")
        return
        
    resposta = messagebox.askyesno("Confirmar", "Deseja realmente excluir este fornecedor? Esta ação também excluirá todos os dados associados (endereço, injetoras, etc.)")
    if not resposta:
        return
    
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar se existem injetoras associadas
        cursor.execute("SELECT COUNT(*) FROM Injetora WHERE ID_Fornecedor = %s", (id_for,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Erro", "Este fornecedor possui injetoras associadas e não pode ser excluído!")
            return
        
        # Excluir em transação segura
        cursor.execute("DELETE FROM EnderecoFornecedor WHERE ID_Fornecedor = %s", (id_for,))
        cursor.execute("DELETE FROM Fornecedor WHERE ID_Fornecedor = %s", (id_for,))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Fornecedor excluído com sucesso!")
        UPD_TABELA_FORNECEDOR(tree)
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao excluir fornecedor: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def UPD_FORNECEDOR(entries, fornecedor_id, tree, funcionario_id):
    id_for = fornecedor_id.get()
    if not id_for:
        messagebox.showwarning("Aviso", "Selecione um fornecedor para atualizar!")
        return
        
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Validação de campos obrigatórios
        required_fields = ["Nome", "CNPJ"]
        for field in required_fields:
            if not entries[field].get().strip():
                messagebox.showerror("Erro", f"O campo {field} é obrigatório!")
                return
        
        # Atualizar fornecedor
        query = """
        UPDATE Fornecedor SET 
            NM_Fornecedor = %s,
            CNPJ = %s,
            telefone = %s,
            email = %s,
            website = %s,
            cadastrado_por = %s
        WHERE ID_Fornecedor = %s
        """
        valores = (
            entries["Nome"].get(),
            entries["CNPJ"].get(),
            entries["Telefone"].get(),
            entries["E-mail"].get(),
            entries["Website"].get(),
            funcionario_id,
            id_for
        )
        cursor.execute(query, valores)
        
        # Verificar se endereço existe
        cursor.execute("SELECT COUNT(*) FROM EnderecoFornecedor WHERE ID_Fornecedor = %s", (id_for,))
        endereco_existe = cursor.fetchone()[0] > 0
        
        # Dados do endereço
        endereco_data = (
            entries["Rua"].get(),
            entries["Número"].get(),
            entries["Bairro"].get(),
            entries["Cidade"].get(),
            entries["Estado"].get(),
            entries["CEP"].get(),
            id_for
        )
        
        if endereco_existe:
            # Atualizar endereço existente
            query_end = """
            UPDATE EnderecoFornecedor SET 
                rua = %s,
                numero = %s,
                bairro = %s,
                cidade = %s,
                estado = %s,
                cep = %s
            WHERE ID_Fornecedor = %s
            """
        else:
            # Inserir novo endereço
            query_end = """
            INSERT INTO EnderecoFornecedor 
                (rua, numero, bairro, cidade, estado, cep, ID_Fornecedor)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        
        cursor.execute(query_end, endereco_data)
        conn.commit()
        
        messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
        UPD_TABELA_FORNECEDOR(tree)
        LIMPAR_CAMPOS(entries)
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao atualizar fornecedor: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def UPD_TABELA_FORNECEDOR(tree):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Limpar a treeview
        tree.delete(*tree.get_children())
        
        # Buscar fornecedores com informações de endereço
        query = """
        SELECT f.*, 
               CONCAT(e.rua, ', ', e.numero, ', ', e.bairro, ', ', e.cidade, ', ', e.estado) as endereco
        FROM Fornecedor f
        LEFT JOIN EnderecoFornecedor e ON f.ID_Fornecedor = e.ID_Fornecedor
        ORDER BY f.NM_Fornecedor
        """
        cursor.execute(query)
        
        # Preencher a treeview
        for forn in cursor.fetchall():
            tree.insert("", "end", values=(
                forn["ID_Fornecedor"],
                forn["NM_Fornecedor"],
                forn["CNPJ"],
                forn["telefone"] or "",
                forn["email"] or "",
                forn["website"] or "",
                forn["endereco"] or "Endereço não cadastrado"
            ))
            
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar fornecedores: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def UPD_CAMPOS_FORNECEDOR(entries, fornecedor_id, id_for):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Buscar dados do fornecedor
        query = """
        SELECT f.*, e.* 
        FROM Fornecedor f
        LEFT JOIN EnderecoFornecedor e ON f.ID_Fornecedor = e.ID_Fornecedor
        WHERE f.ID_Fornecedor = %s
        """
        cursor.execute(query, (id_for,))
        forn = cursor.fetchone()
        
        if forn:
            # Limpar e preencher campos
            for field, db_field in [
                ("Nome", "NM_Fornecedor"),
                ("CNPJ", "CNPJ"),
                ("Telefone", "telefone"),
                ("E-mail", "email"),
                ("Website", "website"),
                ("Rua", "rua"),
                ("Número", "numero"),
                ("Bairro", "bairro"),
                ("Cidade", "cidade"),
                ("Estado", "estado"),
                ("CEP", "cep")
            ]:
                entries[field].delete(0, "end")
                entries[field].insert(0, forn.get(db_field, ""))
            
            # Atualizar o ID do fornecedor
            fornecedor_id.delete(0, "end")
            fornecedor_id.insert(0, str(forn["ID_Fornecedor"]))
            
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar dados do fornecedor: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def GET_FORNECEDOR():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Fornecedor, NM_Fornecedor FROM Fornecedor ORDER BY NM_Fornecedor")
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao obter lista de fornecedores: {str(e)}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def LIMPAR_CAMPOS(entries):
    for entry in entries.values():
        entry.delete(0, "end")