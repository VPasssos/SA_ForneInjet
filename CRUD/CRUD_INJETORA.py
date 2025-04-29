from Config import get_connection
import tkinter.messagebox as messagebox

def criar_injetora(marca, modelo, tipo_controle, capacidade, forca_fechamento,
                  preco_usd, preco_brl, quantidade, observacoes, id_fornecedor):
    """Cadastra uma nova injetora no sistema"""
    conn = None
    cursor = None
    try:
        # Validações básicas
        if not all([marca, modelo, tipo_controle, capacidade, forca_fechamento]):
            raise ValueError("Preencha todos os campos obrigatórios!")
        
        # Converter valores numéricos
        try:
            capacidade = float(capacidade)
            forca_fechamento = float(forca_fechamento)
            preco_usd = float(preco_usd) if preco_usd else None
            preco_brl = float(preco_brl) if preco_brl else None
            quantidade = int(quantidade) if quantidade else 0
        except ValueError:
            raise ValueError("Valores numéricos inválidos!")
        
        conn = get_connection()
        if not conn:
            raise Exception("Não foi possível conectar ao banco de dados")
        
        cursor = conn.cursor()
        
        query = """
        INSERT INTO Injetora 
            (marca, modelo, tipo_de_controle, capacidade_de_injecao, forca_de_fechamento,
             preco_medio_USD, preco_medio_BRL, quantidade, observacao, ID_Fornecedor) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            marca, modelo, tipo_controle, capacidade, forca_fechamento,
            preco_usd, preco_brl, quantidade, observacoes, id_fornecedor
        ))
        
        conn.commit()
        return cursor.lastrowid
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao cadastrar: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def listar_injetoras():
    """Retorna todas as injetoras com informações do fornecedor"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            raise Exception("Não foi possível conectar ao banco de dados")
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            i.ID_Injetora, i.marca, i.modelo, i.tipo_de_controle, 
            i.capacidade_de_injecao, i.forca_de_fechamento,
            i.preco_medio_USD, i.preco_medio_BRL, i.quantidade, i.observacao,
            f.ID_Fornecedor, f.NM_Fornecedor
        FROM Injetora i
        LEFT JOIN Fornecedor f ON i.ID_Fornecedor = f.ID_Fornecedor
        ORDER BY i.marca, i.modelo
        """
        cursor.execute(query)
        return cursor.fetchall()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao listar injetoras: {str(e)}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def atualizar_injetora(id_injetora, marca, modelo, tipo_controle, capacidade, 
                      forca_fechamento, preco_usd, preco_brl, quantidade, 
                      observacoes, id_fornecedor):
    """Atualiza os dados de uma injetora"""
    conn = None
    cursor = None
    try:
        # Validações básicas
        if not all([marca, modelo, tipo_controle, capacidade, forca_fechamento]):
            raise ValueError("Preencha todos os campos obrigatórios!")
        
        # Converter valores numéricos
        try:
            capacidade = float(capacidade)
            forca_fechamento = float(forca_fechamento)
            preco_usd = float(preco_usd) if preco_usd else None
            preco_brl = float(preco_brl) if preco_brl else None
            quantidade = int(quantidade) if quantidade else 0
        except ValueError:
            raise ValueError("Valores numéricos inválidos!")
        
        conn = get_connection()
        if not conn:
            raise Exception("Não foi possível conectar ao banco de dados")
        
        cursor = conn.cursor()
        
        query = """
        UPDATE Injetora 
        SET 
            marca = %s, modelo = %s, tipo_de_controle = %s, 
            capacidade_de_injecao = %s, forca_de_fechamento = %s,
            preco_medio_USD = %s, preco_medio_BRL = %s, 
            quantidade = %s, observacao = %s, ID_Fornecedor = %s
        WHERE ID_Injetora = %s
        """
        cursor.execute(query, (
            marca, modelo, tipo_controle, capacidade, forca_fechamento,
            preco_usd, preco_brl, quantidade, observacoes, id_fornecedor,
            id_injetora
        ))
        
        conn.commit()
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao atualizar: {str(e)}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def deletar_injetora(id_injetora):
    """Remove uma injetora do sistema"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            raise Exception("Não foi possível conectar ao banco de dados")
        
        cursor = conn.cursor()
        
        # Verificar se há compras associadas
        cursor.execute("SELECT COUNT(*) FROM Compra WHERE ID_Injetora = %s", (id_injetora,))
        if cursor.fetchone()[0] > 0:
            raise Exception("Não é possível excluir injetora com compras associadas!")
        
        cursor.execute("DELETE FROM Injetora WHERE ID_Injetora = %s", (id_injetora,))
        conn.commit()
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", f"Falha ao excluir: {str(e)}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def buscar_injetora_por_id(id_injetora):
    """Retorna uma injetora específica com informações do fornecedor"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        if not conn:
            raise Exception("Não foi possível conectar ao banco de dados")
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            i.ID_Injetora, i.marca, i.modelo, i.tipo_de_controle, 
            i.capacidade_de_injecao, i.forca_de_fechamento,
            i.preco_medio_USD, i.preco_medio_BRL, i.quantidade, i.observacao,
            f.ID_Fornecedor, f.NM_Fornecedor
        FROM Injetora i
        LEFT JOIN Fornecedor f ON i.ID_Fornecedor = f.ID_Fornecedor
        WHERE i.ID_Injetora = %s
        """
        cursor.execute(query, (id_injetora,))
        return cursor.fetchone()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao buscar injetora: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Funções para integração com a interface gráfica
def carregar_injetoras_na_tabela(tabela):
    """Carrega todas as injetoras em uma tabela tkinter"""
    for row in tabela.get_children():
        tabela.delete(row)
    
    injetoras = listar_injetoras()
    for inj in injetoras:
        # Formatar preços
        preco_usd = f"${inj['preco_medio_USD']:,.2f}" if inj['preco_medio_USD'] else ""
        preco_brl = f"R${inj['preco_medio_BRL']:,.2f}" if inj['preco_medio_BRL'] else ""
        
        tabela.insert("", "end", values=(
            inj['ID_Injetora'],
            inj['marca'],
            inj['modelo'],
            inj['tipo_de_controle'],
            f"{inj['capacidade_de_injecao']}g",
            f"{inj['forca_de_fechamento']} ton",
            preco_usd,
            preco_brl,
            inj['quantidade'],
            inj['NM_Fornecedor'] or "",
            inj['ID_Fornecedor']  # Oculto
        ))

def salvar_injetora_gui(entries, fornecedor_cb, id_entry=None, tabela=None):
    """Salva/atualiza uma injetora a partir dos dados da interface"""
    # Extrair ID do fornecedor do combobox
    fornecedor_texto = fornecedor_cb.get()
    if not fornecedor_texto:
        messagebox.showerror("Erro", "Selecione um fornecedor!")
        return False
    
    # Extrair ID do texto no formato "Nome (ID: 123)"
    try:
        id_fornecedor = int(fornecedor_texto.split("(ID: ")[1].replace(")", ""))
    except:
        messagebox.showerror("Erro", "Formato de fornecedor inválido!")
        return False
    
    # Dados da injetora
    dados = {
        'marca': entries['Marca'].get(),
        'modelo': entries['Modelo'].get(),
        'tipo_controle': entries['Tipo de Controle'].get(),
        'capacidade': entries['Capacidade de Injeção (g)'].get(),
        'forca_fechamento': entries['Força de Fechamento (ton)'].get(),
        'preco_usd': entries['Preço Médio (USD)'].get(),
        'preco_brl': entries['Preço Médio (BRL)'].get(),
        'quantidade': entries['Quantidade'].get(),
        'observacoes': entries['Observações'].get()
    }
    
    # Validação obrigatória
    campos_obrigatorios = ['marca', 'modelo', 'tipo_controle', 'capacidade', 'forca_fechamento']
    for campo in campos_obrigatorios:
        if not dados[campo]:
            messagebox.showerror("Erro", f"O campo {campo.replace('_', ' ').capitalize()} é obrigatório!")
            return False
    
    if id_entry and id_entry.get():  # Atualização
        id_inj = int(id_entry.get())
        sucesso = atualizar_injetora(
            id_inj,
            dados['marca'],
            dados['modelo'],
            dados['tipo_controle'],
            dados['capacidade'],
            dados['forca_fechamento'],
            dados['preco_usd'],
            dados['preco_brl'],
            dados['quantidade'],
            dados['observacoes'],
            id_fornecedor
        )
        if sucesso:
            messagebox.showinfo("Sucesso", "Injetora atualizada com sucesso!")
            if tabela:
                carregar_injetoras_na_tabela(tabela)
            return True
    else:  # Cadastro novo
        id_inj = criar_injetora(
            dados['marca'],
            dados['modelo'],
            dados['tipo_controle'],
            dados['capacidade'],
            dados['forca_fechamento'],
            dados['preco_usd'],
            dados['preco_brl'],
            dados['quantidade'],
            dados['observacoes'],
            id_fornecedor
        )
        if id_inj:
            messagebox.showinfo("Sucesso", "Injetora cadastrada com sucesso!")
            if tabela:
                carregar_injetoras_na_tabela(tabela)
            return True
    
    return False

def preencher_campos_injetora(entries, fornecedor_cb, id_entry, id_injetora, fornecedores_disponiveis):
    """Preenche os campos da interface com os dados de uma injetora"""
    inj = buscar_injetora_por_id(id_injetora)
    if not inj:
        messagebox.showerror("Erro", "Injetora não encontrada!")
        return
    
    # Dados básicos
    id_entry.delete(0, 'end')
    id_entry.insert(0, str(inj['ID_Injetora']))
    
    entries['Marca'].delete(0, 'end')
    entries['Marca'].insert(0, inj['marca'])
    
    entries['Modelo'].delete(0, 'end')
    entries['Modelo'].insert(0, inj['modelo'])
    
    entries['Tipo de Controle'].delete(0, 'end')
    entries['Tipo de Controle'].insert(0, inj['tipo_de_controle'])
    
    entries['Capacidade de Injeção (g)'].delete(0, 'end')
    entries['Capacidade de Injeção (g)'].insert(0, str(inj['capacidade_de_injecao']))
    
    entries['Força de Fechamento (ton)'].delete(0, 'end')
    entries['Força de Fechamento (ton)'].insert(0, str(inj['forca_de_fechamento']))
    
    entries['Preço Médio (USD)'].delete(0, 'end')
    entries['Preço Médio (USD)'].insert(0, str(inj['preco_medio_USD'] or ""))
    
    entries['Preço Médio (BRL)'].delete(0, 'end')
    entries['Preço Médio (BRL)'].insert(0, str(inj['preco_medio_BRL'] or ""))
    
    entries['Quantidade'].delete(0, 'end')
    entries['Quantidade'].insert(0, str(inj['quantidade']))
    
    entries['Observações'].delete(0, 'end')
    entries['Observações'].insert(0, inj['observacao'] or "")
    
    # Fornecedor
    if inj['ID_Fornecedor'] and inj['ID_Fornecedor'] in fornecedores_disponiveis:
        nome_fornecedor = fornecedores_disponiveis[inj['ID_Fornecedor']]
        fornecedor_cb.set(f"{nome_fornecedor} (ID: {inj['ID_Fornecedor']})")
    else:
        fornecedor_cb.set('')

def limpar_campos_injetora(entries, fornecedor_cb, id_entry):
    """Limpa todos os campos do formulário"""
    id_entry.delete(0, 'end')
    for entry in entries.values():
        entry.delete(0, 'end')
    fornecedor_cb.set('')

def excluir_injetora_gui(id_entry, tabela):
    """Exclui uma injetora após confirmação"""
    if not id_entry.get():
        messagebox.showwarning("Aviso", "Selecione uma injetora para excluir")
        return
    
    if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta injetora?"):
        if deletar_injetora(int(id_entry.get())):
            messagebox.showinfo("Sucesso", "Injetora excluída com sucesso!")
            carregar_injetoras_na_tabela(tabela)
        else:
            messagebox.showerror("Erro", "Falha ao excluir injetora")