# Importação de bibliotecas necessárias
from tkinter import ttk
from CRUDS.CRUD_FUNCIONARIO import UPD_DADOS_FUNCIONARIOS  # Função para buscar os dados do funcionário
from CRUDS.CRUD_VENDA import *  # Importa todas as funções relacionadas à venda

# Classe principal da tela do gerente (gestor de vendas)
class TELA_GERENTE:
    def __init__(self, root, id_funcionario):
        self.root = root
        self.root.title("Sistema ForneInjet - GESTOR DE VENDAS")  # Define título da janela
        self.root.geometry("1200x800")  # Define o tamanho da janela
        self.funcionario_logado_id = id_funcionario  # Guarda o ID do funcionário logado
        self.funcionario_dados = UPD_DADOS_FUNCIONARIOS(self.funcionario_logado_id)  # Busca dados do funcionário no BD
        self.CRIAR_WIDGETS()  # Cria os componentes da interface

    def CRIAR_WIDGETS(self):
        # Notebook com abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        # Criação das abas principais
        self.ABA_GESTAO_VENDAS()
        self.ABA_VENDA()
        self.ABA_CONFIGURACAO()

    def ABA_GESTAO_VENDAS(self):
        # Aba de gestão de vendas
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="GESTÃO VENDAS")
        
        # Frame de pesquisa de vendas
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        # Campo e botão de pesquisa
        ttk.Label(search_frame, text="Pesquisar:").pack(side="left", padx=5)
        self.search_entry_gestao = ttk.Entry(search_frame, width=40)
        self.search_entry_gestao.pack(side="left", padx=5)
        self.search_entry_gestao.bind("<KeyRelease>", self.FILTRAR_VENDAS_GESTAO)
        
        ttk.Button(search_frame, text="Atualizar", 
                   command=lambda: UPD_TABELA_VENDAS(self.tree_gestao)).pack(side="left", padx=5)
        
        # Frame da tabela
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Define colunas
        cols = ["ID", "Cliente", "Produto", "Quantidade", "Preço Unitário (BRL)",
                "Data da Venda", "Forma Pagamento", "Status Aprovação", "Cadastrante", "Observações"]
        
        self.tree_gestao = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
        
        # Ajuste de largura de colunas
        widths = {"ID": 50, "Cliente": 120, "Produto": 120, "Quantidade": 80, 
                  "Valor Total (BRL)": 100, "Data Venda": 100, "Status": 100, 
                  "Vendedor": 120, "Observações": 150}
        
        for col in cols:
            self.tree_gestao.heading(col, text=col)
            self.tree_gestao.column(col, width=widths.get(col, 100), 
                                    anchor='center' if col != "Observações" else 'w')
        
        # Scrollbar para a tabela
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_gestao.yview)
        scroll.pack(side="right", fill="y")
        self.tree_gestao.configure(yscrollcommand=scroll.set)
        self.tree_gestao.pack(fill="both", expand=True)
        
        # Frame de botões de ação
        action_frame = ttk.Frame(frame)
        action_frame.pack(fill="x", padx=10, pady=5)

        # Botões para atualização de status
        ttk.Button(action_frame, text="Aprovar", 
                   command=lambda: self.ATUALIZAR_STATUS_VENDA("Aprovado")).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Reprovar", 
                   command=lambda: self.ATUALIZAR_STATUS_VENDA("Reprovado")).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Colocar em Análise", 
                   command=lambda: self.ATUALIZAR_STATUS_VENDA("Em análise")).pack(side="left", padx=5)
        
        # Carrega as vendas inicialmente
        UPD_TABELA_VENDAS(self.tree_gestao)

        # Permite ver detalhes ao dar duplo clique
        self.tree_gestao.bind("<Double-1>", self.MOSTRAR_DETALHES_VENDA)

    def FILTRAR_VENDAS_GESTAO(self, event=None):
        # Filtra a tabela com base no que foi digitado
        termo = self.search_entry_gestao.get().lower()
        for child in self.tree_gestao.get_children():
            valores = self.tree_gestao.item(child)["values"]
            texto = " ".join(str(v) for v in valores).lower()
            if termo in texto:
                self.tree_gestao.reattach(child, "", "end")
            else:
                self.tree_gestao.detach(child)

    def ATUALIZAR_STATUS_VENDA(self, novo_status):
        # Atualiza o status da venda selecionada
        selected = self.tree_gestao.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma venda para atualizar o status")
            return
        
        venda_id = self.tree_gestao.item(selected[0])["values"][0]
        from CRUDS.CRUD_VENDA import UPDATE_STATUS_VENDA  # Importa função que atualiza status no BD
        if UPDATE_STATUS_VENDA(venda_id, novo_status, self.funcionario_logado_id):
            messagebox.showinfo("Sucesso", f"Status da venda atualizado para '{novo_status}'")
            UPD_TABELA_VENDAS(self.tree_gestao)
        else:
            messagebox.showerror("Erro", "Não foi possível atualizar o status da venda")

    def MOSTRAR_DETALHES_VENDA(self, event):
        # Abre nova janela com os detalhes da venda
        selected = self.tree_gestao.selection()
        if not selected:
            return
        
        venda_id = self.tree_gestao.item(selected[0])["values"][0]
        detalhes_window = tk.Toplevel(self.root)
        detalhes_window.title(f"Detalhes da Venda #{venda_id}")
        detalhes_window.geometry("600x400")
        
        from CRUDS.CRUD_VENDA import GET_DETALHES_VENDA
        detalhes = GET_DETALHES_VENDA(venda_id)

        if not detalhes:
            ttk.Label(detalhes_window, text="Não foi possível carregar os detalhes da venda").pack(pady=20)
            return

        # Exibe os dados principais da venda
        frame_detalhes = ttk.Frame(detalhes_window)
        frame_detalhes.pack(fill="both", expand=True, padx=10, pady=10)

        campos = [
            ("ID Venda:", detalhes["id_venda"]),
            ("Cliente:", detalhes["nome_cliente"]),
            ("Vendedor:", detalhes["nome_vendedor"]),
            ("Data:", detalhes["data_venda"]),
            ("Status:", detalhes["status_aprovacao"]),
            ("Valor Total BRL:", f"R$ {detalhes['valor_total_BRL']:.2f}"),
            ("Forma Pagamento:", detalhes["forma_pagamento"]),
            ("Observações:", detalhes["observacoes"])
        ]

        for i, (label, valor) in enumerate(campos):
            ttk.Label(frame_detalhes, text=label, font=('Arial', 10, 'bold')).grid(row=i, column=0, sticky="e", padx=5, pady=2)
            ttk.Label(frame_detalhes, text=valor).grid(row=i, column=1, sticky="w", padx=5, pady=2)

        # Lista de itens da venda
        ttk.Label(frame_detalhes, text="Itens da Venda:", font=('Arial', 10, 'bold')).grid(row=len(campos), column=0, columnspan=2, pady=10)
        
        cols = ["Produto", "Quantidade", "Preço Unitário (BRL)", "Subtotal (BRL)"]
        tree_itens = ttk.Treeview(frame_detalhes, columns=cols, show="headings", height=5)

        for col in cols:
            tree_itens.heading(col, text=col)
            tree_itens.column(col, width=100, anchor='center')

        tree_itens.grid(row=len(campos)+1, column=0, columnspan=2, sticky="nsew")

        scroll = ttk.Scrollbar(frame_detalhes, orient="vertical", command=tree_itens.yview)
        scroll.grid(row=len(campos)+1, column=2, sticky="ns")
        tree_itens.configure(yscrollcommand=scroll.set)

        for item in detalhes.get("itens", []):
            subtotal = item["quantidade"] * item["preco_unitario_BRL"]
            tree_itens.insert("", "end", values=(
                item["nome_produto"],
                item["quantidade"],
                f"R$ {item['preco_unitario_BRL']:.2f}",
                f"R$ {subtotal:.2f}"
            ))

    def ABA_VENDA(self):
        # Aba para cadastrar/consultar vendas
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="VENDAS")

        form_frame = ttk.LabelFrame(frame, text="Dados da Venda", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        from CRUDS.CRUD_CLIENTE import GET_CLIENTES
        from CRUDS.CRUD_INJETORA import GET_INJETORA
        clientes = GET_CLIENTES()
        injetoras = GET_INJETORA()

        nomes_clientes = [cliente[1] for cliente in clientes]
        nomes_injetoras = [injetora[1] for injetora in injetoras]

        # Criação dos campos do formulário
        campos = [
            ("Cliente", 0, 0), ("Produto", 0, 2),
            ("Quantidade", 1, 0), ("Preço Unitário (BRL)", 1, 2),
            ("Forma Pagamento", 2, 0), ("Observações", 2, 2)
        ]

        self.entries_venda = {}
        for campo, row, col in campos:
            lbl = ttk.Label(form_frame, text=f"{campo}:")
            lbl.grid(row=row, column=col, padx=5, pady=5, sticky="e")

            if campo == "Cliente":
                entry = ttk.Combobox(form_frame, width=30, values=nomes_clientes)
                self.cliente_cb_venda = entry
            elif campo == "Produto":
                entry = ttk.Combobox(form_frame, width=30, values=nomes_injetoras)
                self.produto_cb_venda = entry
            else:
                entry = ttk.Entry(form_frame, width=30)

            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
            self.entries_venda[campo] = entry

        self.venda_id = ttk.Entry(form_frame)  # Oculto
        self.venda_id.grid(row=0, column=4)
        self.venda_id.grid_remove()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=5)
        botoes = [
            ("Novo", lambda: ADD_VENDA(self.entries_venda, self.cliente_cb_venda, self.produto_cb_venda, self.tree_vendas, self.funcionario_logado_id)),
            ("Consultar", lambda: CONSULTAR_SOLICITACAO(self.funcionario_logado_id, self.root))
        ]
        for i, (texto, cmd) in enumerate(botoes):
            ttk.Button(btn_frame, text=texto, command=cmd).grid(row=0, column=i, padx=5)

        # Tabela de vendas (inicialmente oculta)
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        cols = ["ID", "Cliente", "Produto", "Quantidade", "Preço Unitário (BRL)", "Data da Venda", "Forma Pagamento", "Status Aprovação", "Cadastrante", "Observações"]
        self.tree_vendas = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
        for col in cols:
            width = 100
            if col == "ID":
                width = 50
            elif col == "Observações":
                width = 150
            elif col == "Data da Venda":
                width = 120
            self.tree_vendas.heading(col, text=col)
            self.tree_vendas.column(col, width=width, anchor='w' if col == "Observações" else 'center')

        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_vendas.yview)
        scroll.pack(side="right", fill="y")
        self.tree_vendas.configure(yscrollcommand=scroll.set)
        self.tree_vendas.pack_forget()

    def Consultar_Solicitacao(self, event=None):
        # Filtra a aba de vendas conforme termo digitado
        termo = self.search_entry_venda.get().lower()
        if termo == "":
            UPD_TABELA_VENDAS(self.tree_vendas)
        else:
            for child in self.tree_vendas.get_children(""):
                valores = self.tree_vendas.item(child)["values"]
                texto = " ".join(str(v) for v in valores).lower()
                if termo in texto:
                    self.tree_vendas.reattach(child, "", "end")
                else:
                    self.tree_vendas.detach(child)

    def ABA_CONFIGURACAO(self):
        # Aba de configurações do usuário logado
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="CONFIGURAÇÃO")

        info_frame = ttk.LabelFrame(frame, text="Dados do Funcionário")
        info_frame.pack(fill="x", padx=10, pady=10)

        dados = self.funcionario_dados

        # Exibe dados do funcionário
        campos = [
            f"Nome: {dados.get('nome', '')}",
            f"Cargo: {dados.get('cargo', '')}",
            f"Telefone: {dados.get('telefone', '')}",
            f"E-mail: {dados.get('email', '')}",
            f"Usuário: {dados.get('usuario', '')}",
            f"Permissão: {dados.get('permissao', '')}",
            f"Situação: {dados.get('situacao', '')}",
            f"Admissão: {dados.get('data_admissao', '')}"
        ]
        for campo in campos:
            ttk.Label(info_frame, text=campo).pack(anchor="w", padx=10, pady=2)

        endereco_str = f"{dados.get('rua', '')}, {dados.get('numero', '')}, {dados.get('bairro', '')}, {dados.get('cidade', '')} - {dados.get('estado', '')}, CEP: {dados.get('cep', '')}"
        ttk.Label(info_frame, text=f"Endereço: {endereco_str}").pack(anchor="w", padx=10, pady=2)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(btn_frame, text="Sair", command=lambda: self.SAIR(self.funcionario_logado_id)).grid(row=0, column=0, padx=5)

    def SAIR(self, funcionario_logado_id):
        # Fecha a tela atual e retorna ao login
        import tkinter as tk
        from TELAS.TELA_LOGIN import TELA_LOGIN

        self.root.withdraw()
        novo_root = tk.Toplevel()
        TELA_LOGIN(novo_root)
        novo_root.mainloop()
        print(f"Funcionário ID {funcionario_logado_id} saiu e retornou ao login.")
