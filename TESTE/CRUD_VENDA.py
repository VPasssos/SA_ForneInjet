from tkinter import messagebox
from CONFIG import get_connection
from tkinter import ttk
import tkinter as tk
from datetime import datetime

def ADD_VENDA(entries, cliente_cb, produto_cb_venda, tree, funcionario_id):
    """
    Cadastra uma nova venda no sistema com validações e tratamento de dados.
    
    Args:
        entries (dict): Campos do formulário de venda
        cliente_cb (Combobox): Combobox com seleção de clientes
        produto_cb_venda (Combobox): Combobox com seleção de produtos
        tree (Treeview): Componente de tabela para exibição
        funcionario_id (int/str): ID do funcionário responsável pela venda
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Validação do ID do funcionário (pode ser Entry ou variável)
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

        # Obter ID do cliente selecionado
        nome_cliente = cliente_cb.get()
        cursor.execute("SELECT ID_Cliente FROM Cliente WHERE nome = %s", (nome_cliente,))
        id_cliente = cursor.fetchone()
        if not id_cliente:
            messagebox.showwarning("Aviso", "Cliente não encontrado!")
            return

        # Obter ID do produto selecionado
        nome_produto = produto_cb_venda.get()
        cursor.execute("SELECT ID_Injetora FROM Injetora WHERE modelo = %s", (nome_produto,))
        id_produto = cursor.fetchone()
        if not id_produto:
            messagebox.showwarning("Aviso", "Produto não encontrado!")
            return

        # Cálculo do valor total da venda
        quantidade = int(entries["Quantidade"].get())
        preco_unitario = float(entries["Preço Unitário (BRL)"].get())
        valor_total = quantidade * preco_unitario

        # Query para inserir a venda principal
        query = """
        INSERT INTO Venda (data_venda, valor_total_BRL, 
        status_aprovacao, ID_Cliente, ID_Funcionario, observacoes, forma_pagamento)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        # Verifica permissões do funcionário para definir status
        cursor.execute("SELECT permissao FROM funcionario WHERE id_funcionario = %s", (funcionario_id,))
        permissao = cursor.fetchone()
        
        if permissao and permissao[0] == "admin":   
            # Administradores podem definir status diretamente
            valores = (
                entries["Data Venda"].get(),
                valor_total,
                entries["Status Aprovação"].get(),
                id_cliente[0],
                funcionario_id,
                entries["Observações"].get(),
                entries["Forma Pagamento"].get()
            )
        else:
            # Outros funcionários cadastram como "Em análise"
            status_aprovacao = "Em análise"
            from datetime import date
            data_atual = date.today()
            valores = (
                data_atual,
                valor_total,
                status_aprovacao,
                id_cliente[0],
                funcionario_id,
                entries["Observações"].get(),
                entries["Forma Pagamento"].get()
            )

        cursor.execute(query, valores)
        id_venda = cursor.lastrowid  # Obtém o ID da venda recém-criada

        # Query para inserir o item da venda
        query_item = """
        INSERT INTO ItemVenda (ID_Venda, ID_Injetora, quantidade, preco_unitario_BRL)
        VALUES (%s, %s, %s, %s)
        """
        valores_item = (
            id_venda,
            id_produto[0],
            quantidade,
            preco_unitario
        )

        cursor.execute(query_item, valores_item)
        conn.commit()

        messagebox.showinfo("Sucesso", "Venda cadastrada com sucesso!")
        UPD_TABELA_VENDAS(tree)  # Atualiza a tabela de exibição
        LIMPAR_CAMPOS(entries)   # Limpa os campos do formulário

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao cadastrar a venda:\n{str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def DEL_VENDA(venda_id, tree):
    """
    Remove uma venda do sistema após confirmação.
    
    Args:
        venda_id (StringVar/IntVar): ID da venda a ser removida
        tree (Treeview): Componente de tabela para atualização
    """
    id_venda = venda_id.get()
    if not id_venda:
        messagebox.showwarning("Aviso", "Selecione uma venda para excluir!")
        return

    # Confirmação de exclusão
    resposta = messagebox.askyesno("Confirmar", "Deseja realmente excluir esta venda?")
    if resposta:
        conn = get_connection()
        cursor = conn.cursor()

        # Primeiro exclui os itens associados (integridade referencial)
        cursor.execute("DELETE FROM ItemVenda WHERE ID_Venda = %s", (id_venda,))
        # Depois exclui a venda principal
        cursor.execute("DELETE FROM Venda WHERE ID_Venda = %s", (id_venda,))
        conn.commit()

        messagebox.showinfo("Sucesso", "Venda excluída com sucesso!")
        UPD_TABELA_VENDAS(tree)  # Atualiza a tabela
        cursor.close()
        conn.close()

def UPD_VENDA(entries, cliente_cb, venda_id, tree, funcionario_logado_id):
    """
    Atualiza os dados de uma venda existente.
    
    Args:
        entries (dict): Campos do formulário com os novos valores
        cliente_cb (Combobox): Combobox de seleção de cliente
        venda_id (StringVar/IntVar): ID da venda sendo editada
        tree (Treeview): Tabela para atualização visual
        funcionario_logado_id (int/str): ID do funcionário realizando a edição
    """
    try:
        id_venda = venda_id.get()
        if not id_venda:
            messagebox.showwarning("Aviso", "Selecione uma venda para atualizar!")
            return

        # Validação do ID do funcionário
        if hasattr(funcionario_logado_id, 'get'):
            funcionario_logado_id = funcionario_logado_id.get()
        if not funcionario_logado_id:
            messagebox.showwarning("Aviso", "Funcionário não identificado!")
            return
        try:
            funcionario_logado_id = int(funcionario_logado_id)
        except ValueError:
            messagebox.showwarning("Aviso", "ID do funcionário inválido!")
            return

        conn = get_connection()
        cursor = conn.cursor()

        # Validação do cliente
        nome_cliente = cliente_cb.get()
        cursor.execute("SELECT ID_Cliente FROM Cliente WHERE nome = %s", (nome_cliente,))
        resultado_cliente = cursor.fetchone()
        if not resultado_cliente:
            messagebox.showwarning("Aviso", "Cliente não encontrado!")
            return
        id_cliente = resultado_cliente[0]

        # Validação do produto
        nome_produto = entries["Produto"].get()
        cursor.execute("SELECT ID_Injetora FROM Injetora WHERE modelo = %s", (nome_produto,))
        resultado_produto = cursor.fetchone()
        if not resultado_produto:
            messagebox.showwarning("Aviso", "Produto não encontrado!")
            return
        id_produto = resultado_produto[0]

        # Query de atualização da venda principal
        query = """
        UPDATE Venda SET 
            data_venda = %s,
            valor_total_BRL = %s,
            status_aprovacao = %s,
            ID_Cliente = %s,
            observacoes = %s,
            forma_pagamento = %s
        WHERE ID_Venda = %s
        """
        valores = (
            entries["Data Venda"].get(),
            float(entries["Preço Unitário (BRL)"].get()),
            entries["Status Aprovação"].get(),
            id_cliente,
            entries["Observações"].get(),
            entries["Forma Pagamento"].get(),
            id_venda
        )
        cursor.execute(query, valores)

        # Query de atualização do item da venda
        query_item = """
        UPDATE ItemVenda SET 
            ID_Injetora = %s,
            quantidade = %s,
            preco_unitario_BRL = %s
        WHERE ID_Venda = %s
        """
        valores_item = (
            id_produto,
            int(entries["Quantidade"].get()),
            float(entries["Preço Unitário (BRL)"].get()),
            id_venda
        )
        cursor.execute(query_item, valores_item)

        conn.commit()
        messagebox.showinfo("Sucesso", "Venda atualizada com sucesso!")
        UPD_TABELA_VENDAS(tree)
        LIMPAR_CAMPOS(entries)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao atualizar a venda:\n{str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def UPD_TABELA_VENDAS(tree):
    """
    Atualiza a tabela de exibição com todas as vendas cadastradas.
    
    Args:
        tree (Treeview): Componente de tabela a ser atualizado
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Limpa a tabela atual
    for item in tree.get_children():
        tree.delete(item)

    # Query que combina dados de múltiplas tabelas (JOIN)
    query = """
    SELECT v.ID_Venda, c.nome AS cliente, i.modelo AS produto, 
        iv.quantidade, iv.preco_unitario_BRL,
        v.data_venda, v.forma_pagamento, v.status_aprovacao, f.nome AS cadastrante, v.observacoes
    FROM Venda v
    JOIN Cliente c ON v.ID_Cliente = c.ID_Cliente
    JOIN ItemVenda iv ON v.ID_Venda = iv.ID_Venda
    JOIN Injetora i ON iv.ID_Injetora = i.ID_Injetora
    JOIN Funcionario f ON v.ID_Funcionario = f.ID_Funcionario
    """
    cursor.execute(query)
    vendas = cursor.fetchall()

    # Preenche a tabela com os dados formatados
    for venda in vendas:
        tree.insert("", "end", values=(
            venda["ID_Venda"],
            venda["cliente"],
            venda["produto"],
            venda["quantidade"],
            venda["preco_unitario_BRL"],
            venda["data_venda"],
            venda["forma_pagamento"],
            venda["status_aprovacao"],
            venda["cadastrante"],
            venda["observacoes"]
        ))

    cursor.close()
    conn.close()

def UPD_CAMPOS_VENDA(entries, cliente_cb, venda_id, id_venda):
    """
    Preenche os campos do formulário com os dados de uma venda selecionada.
    
    Args:
        entries (dict): Campos do formulário a serem preenchidos
        cliente_cb (Combobox): Combobox de seleção de cliente
        venda_id (StringVar/IntVar): Variável para armazenar o ID da venda
        id_venda (int): ID da venda a ser carregada
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Query que busca todos os dados da venda e relacionamentos
    query = """
    SELECT v.*, c.nome AS cliente, i.modelo AS produto, 
           iv.quantidade, iv.preco_unitario_BRL,
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
        # Preenche cada campo do formulário
        entries["Data Venda"].delete(0, "end")
        entries["Data Venda"].insert(0, venda["data_venda"])

        entries["Forma Pagamento"].delete(0, "end")
        entries["Forma Pagamento"].insert(0, str(venda["forma_pagamento"]))

        entries["Preço Unitário (BRL)"].delete(0, "end")
        entries["Preço Unitário (BRL)"].insert(0, str(venda["preco_unitario_BRL"]))

        entries["Quantidade"].delete(0, "end")
        entries["Quantidade"].insert(0, str(venda["quantidade"]))

        entries["Status Aprovação"].delete(0, "end")
        entries["Status Aprovação"].insert(0, venda["status_aprovacao"])

        entries["Cadastrante"].delete(0, "end")
        entries["Cadastrante"].insert(0, venda["cadastrante"])

        entries["Observações"].delete(0, "end")
        entries["Observações"].insert(0, venda["observacoes"])

        # Configura os comboboxes
        cliente_cb.set(venda["cliente"])
        entries["Produto"].delete(0, "end")
        entries["Produto"].insert(0, venda["produto"])

        # Atualiza o ID da venda no formulário
        venda_id.delete(0, "end")
        venda_id.insert(0, str(venda["ID_Venda"]))

    cursor.close()
    conn.close()

def CONSULTAR_SOLICITACAO(funcionario_id, parent_window):
    """
    Exibe uma janela com todas as solicitações de venda de um funcionário.
    
    Args:
        funcionario_id (int): ID do funcionário para filtrar as vendas
        parent_window (Tk): Janela pai para ancorar a nova janela
    """
    # Configuração da janela
    solicitacao_window = tk.Toplevel(parent_window)
    solicitacao_window.title("Minhas Solicitações de Venda")
    solicitacao_window.geometry("1200x600")
    
    # Frame para a tabela
    table_frame = ttk.Frame(solicitacao_window)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Configuração da Treeview
    cols = ["ID", "Cliente", "Produto", "Quantidade", "Preço BRL",
            "Data", "Status", "Forma Pagamento", "Observações"]
    
    tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=20)
    
    # Configura as colunas
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')
    
    # Adiciona scrollbar
    scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    scroll.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(fill="both", expand=True)
    
    # Busca as vendas do funcionário
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT v.ID_Venda, c.nome AS cliente, i.modelo AS produto, 
           iv.quantidade, iv.preco_unitario_BRL,
           v.data_venda, v.status_aprovacao, v.forma_pagamento, v.observacoes
    FROM Venda v
    JOIN Cliente c ON v.ID_Cliente = c.ID_Cliente
    JOIN ItemVenda iv ON v.ID_Venda = iv.ID_Venda
    JOIN Injetora i ON iv.ID_Injetora = i.ID_Injetora
    WHERE v.ID_Funcionario = %s
    ORDER BY v.data_venda DESC
    """
    
    cursor.execute(query, (funcionario_id,))
    vendas = cursor.fetchall()
    
    # Preenche a tabela com os resultados
    for venda in vendas:
        tree.insert("", "end", values=(
            venda["ID_Venda"],
            venda["cliente"],
            venda["produto"],
            venda["quantidade"],
            venda["preco_unitario_BRL"],
            venda["data_venda"],
            venda["status_aprovacao"],
            venda["forma_pagamento"],
            venda["observacoes"]
        ))
    
    cursor.close()
    conn.close()
    
    # Botão de fechar
    btn_frame = ttk.Frame(solicitacao_window)
    btn_frame.pack(fill="x", padx=10, pady=10)
    
    ttk.Button(btn_frame, text="Fechar", command=solicitacao_window.destroy).pack(side="right")

def UPDATE_STATUS_VENDA(venda_id, novo_status, id_gestor):
    """
    Atualiza o status de aprovação de uma venda.
    
    Args:
        venda_id (int): ID da venda a ser atualizada
        novo_status (str): Novo status ('Aprovado', 'Reprovado', 'Em análise')
        id_gestor (int): ID do funcionário que está aprovando
        
    Returns:
        bool: True se a atualização foi bem-sucedida, False caso contrário
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se a venda existe
    cursor.execute("SELECT ID_Venda FROM Venda WHERE ID_Venda = %s", (venda_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return False

    # Atualiza o status com data e responsável
    query = """
    UPDATE Venda 
    SET status_aprovacao = %s, 
        aprovado_por = %s, 
        data_aprovacao = %s
    WHERE ID_Venda = %s
    """
    data_aprovacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(query, (novo_status, id_gestor, data_aprovacao, venda_id))

    conn.commit()
    cursor.close()
    conn.close()
    return True

def GET_DETALHES_VENDA(venda_id):
    """
    Obtém todos os detalhes de uma venda específica.
    
    Args:
        venda_id (int): ID da venda a ser consultada
        
    Returns:
        dict: Dicionário com todos os detalhes da venda ou None se não encontrada
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Consulta os dados principais da venda
    query_venda = """
    SELECT 
        v.ID_Venda,
        c.nome AS nome_cliente,
        f.nome AS nome_vendedor,
        v.data_venda,
        v.status_aprovacao,
        v.valor_total_BRL,
        v.forma_pagamento,
        v.observacoes,
        ap.nome AS nome_aprovador,
        v.data_aprovacao
    FROM Venda v
    JOIN Cliente c ON v.ID_Cliente = c.ID_Cliente
    JOIN Funcionario f ON v.ID_Funcionario = f.ID_Funcionario
    LEFT JOIN Funcionario ap ON v.aprovado_por = ap.ID_Funcionario
    WHERE v.ID_Venda = %s
    """
    cursor.execute(query_venda, (venda_id,))
    venda = cursor.fetchone()

    if not venda:
        cursor.close()
        conn.close()
        return None

    # Consulta os itens da venda
    query_itens = """
    SELECT 
        i.marca, 
        i.modelo,
        iv.quantidade,
        iv.preco_unitario_BRL,
        (iv.quantidade * iv.preco_unitario_BRL) AS subtotal_BRL
    FROM ItemVenda iv
    JOIN Injetora i ON iv.ID_Injetora = i.ID_Injetora
    WHERE iv.ID_Venda = %s
    """
    cursor.execute(query_itens, (venda_id,))
    itens = cursor.fetchall()

    # Formata os dados para retorno
    detalhes = {
        'id_venda': venda['ID_Venda'],
        'nome_cliente': venda['nome_cliente'],
        'nome_vendedor': venda['nome_vendedor'],
        'data_venda': venda['data_venda'].strftime('%d/%m/%Y') if venda['data_venda'] else '',
        'status_aprovacao': venda['status_aprovacao'],
        'valor_total_BRL': float(venda['valor_total_BRL']) if venda['valor_total_BRL'] else 0.0,
        'forma_pagamento': venda['forma_pagamento'],
        'observacoes': venda['observacoes'],
        'aprovado_por': venda['nome_aprovador'],
        'data_aprovacao': venda['data_aprovacao'].strftime('%d/%m/%Y %H:%M') if venda.get('data_aprovacao') else '',
        'itens': [],
    }

    # Adiciona os itens ao resultado
    for item in itens:
        detalhes['itens'].append({
            'nome_produto': f"{item['marca']} {item['modelo']}",
            'quantidade': item['quantidade'],
            'preco_unitario_BRL': float(item['preco_unitario_BRL']),
            'subtotal_BRL': float(item['subtotal_BRL'])
        })

    cursor.close()
    conn.close()
    return detalhes

def LIMPAR_CAMPOS(entries):
    """
    Limpa todos os campos de entrada do formulário.
    
    Args:
        entries (dict): Dicionário com referências aos campos de entrada
    """
    for entry in entries.values():
        entry.delete(0, "end")