from tkinter import ttk
from datetime import datetime
import tkinter as tk
from CRUDS.CRUD_FUNCIONARIO import UPD_DADOS_FUNCIONARIOS
from CRUDS.CRUD_VENDA import ADD_ITEM_VENDA, ADD_VENDA, GET_CLIENTES
class TELA_USER:
    def __init__(self, root, id_funcionario):
        self.root = root
        self.root.title("Sistema ForneInjet - Gestão Completa - USER")
        self.root.geometry("1200x800")
        self.funcionario_logado_id = id_funcionario
        self.funcionario_dados = UPD_DADOS_FUNCIONARIOS(self.funcionario_logado_id)
        self.CRIAR_WIDGETS()
    
    def CRIAR_WIDGETS(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        self.ABA_VENDAS()
        self.ABA_CONFIGURACAO()

    def ABA_VENDAS(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="VENDAS")

        form_frame = ttk.LabelFrame(frame, text="Nova Venda", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        # Cliente
        ttk.Label(form_frame, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.cb_cliente_venda = ttk.Combobox(form_frame, width=40)
        self.cb_cliente_venda.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Data
        ttk.Label(form_frame, text="Data da Venda:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_data_venda = ttk.Entry(form_frame, width=20)
        self.entry_data_venda.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_data_venda.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Forma de pagamento
        ttk.Label(form_frame, text="Forma de Pagamento:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_pagamento_venda = ttk.Entry(form_frame, width=40)
        self.entry_pagamento_venda.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Observações
        ttk.Label(form_frame, text="Observações:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.entry_obs_venda = ttk.Entry(form_frame, width=40)
        self.entry_obs_venda.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        # Tabela de Injetoras disponíveis
        item_frame = ttk.LabelFrame(frame, text="Itens da Venda", padding=10)
        item_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(item_frame, text="Injetora:").grid(row=0, column=0, padx=5, pady=5)
        self.cb_injetora_venda = ttk.Combobox(item_frame, width=40)
        self.cb_injetora_venda.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(item_frame, text="Quantidade:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_qtd_injetora = ttk.Entry(item_frame, width=10)
        self.entry_qtd_injetora.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(item_frame, text="Preço BRL:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_preco_brl = ttk.Entry(item_frame, width=15)
        self.entry_preco_brl.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(item_frame, text="Preço USD:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_preco_usd = ttk.Entry(item_frame, width=15)
        self.entry_preco_usd.grid(row=1, column=3, padx=5, pady=5)

        btn_add_item = ttk.Button(item_frame, text="Adicionar Item", command=self.adicionar_item_venda)
        btn_add_item.grid(row=2, column=0, columnspan=4, pady=10)

        self.itens_venda = []
        self.tree_itens_venda = ttk.Treeview(frame, columns=["Injetora", "Qtd", "BRL", "USD"], show="headings", height=6)
        for col in ["Injetora", "Qtd", "BRL", "USD"]:
            self.tree_itens_venda.heading(col, text=col)
            self.tree_itens_venda.column(col, width=100)
        self.tree_itens_venda.pack(fill="x", padx=10)

        # Botão para salvar venda
        btn_salvar = ttk.Button(frame, text="Salvar Venda", command=self.salvar_venda)
        btn_salvar.pack(pady=10)

        self.carregar_clientes()
        self.carregar_injetoras()


    def carregar_clientes(self):
        # Simule ou carregue do banco: [(ID, Nome)]
        clientes = GET_CLIENTES()  # Você deve criar isso no CRUD_CLIENTE
        self.clientes_dict = {f"{nome} (ID:{id})": id for id, nome in clientes}
        self.cb_cliente_venda["values"] = list(self.clientes_dict.keys())

    def carregar_injetoras(self):
        injetoras = GET_INJETORAS()  # Você deve criar isso no CRUD_INJETORA
        self.injetoras_dict = {f"{marca} {modelo} (ID:{id})": id for id, marca, modelo in injetoras}
        self.cb_injetora_venda["values"] = list(self.injetoras_dict.keys())

    def adicionar_item_venda(self):
        inj_nome = self.cb_injetora_venda.get()
        qtd = int(self.entry_qtd_injetora.get())
        preco_brl = float(self.entry_preco_brl.get())
        preco_usd = float(self.entry_preco_usd.get())

        if inj_nome and qtd > 0:
            self.itens_venda.append({
                "id_injetora": self.injetoras_dict[inj_nome],
                "quantidade": qtd,
                "preco_brl": preco_brl,
                "preco_usd": preco_usd
            })
            self.tree_itens_venda.insert("", "end", values=(inj_nome, qtd, preco_brl, preco_usd))
            self.cb_injetora_venda.set("")
            self.entry_qtd_injetora.delete(0, "end")
            self.entry_preco_brl.delete(0, "end")
            self.entry_preco_usd.delete(0, "end")

    def salvar_venda(self):
        id_cliente = self.clientes_dict.get(self.cb_cliente_venda.get())
        data_venda = self.entry_data_venda.get()
        pagamento = self.entry_pagamento_venda.get()
        obs = self.entry_obs_venda.get()

        total_brl = sum(item["quantidade"] * item["preco_brl"] for item in self.itens_venda)
        total_usd = sum(item["quantidade"] * item["preco_usd"] for item in self.itens_venda)

        id_venda = ADD_VENDA(id_cliente, self.funcionario_logado_id, data_venda, pagamento, total_brl, total_usd, obs)
        
        for item in self.itens_venda:
            ADD_ITEM_VENDA(id_venda, item["id_injetora"], item["quantidade"], item["preco_brl"], item["preco_usd"])

        self.tree_itens_venda.delete(*self.tree_itens_venda.get_children())
        self.itens_venda = []
        self.cb_cliente_venda.set("")
        self.entry_pagamento_venda.delete(0, "end")
        self.entry_obs_venda.delete(0, "end")
        print("Venda salva com sucesso!")


    def ABA_CONFIGURACAO(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Configuração")

        info_frame = ttk.LabelFrame(frame, text="Dados do Funcionário")
        info_frame.pack(fill="x", padx=10, pady=10)

        dados = self.funcionario_dados

        # Labels com os dados do funcionário
        ttk.Label(info_frame, text=f"ID: {dados.get('ID_Funcionario', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Nome: {dados.get('nome', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Cargo: {dados.get('cargo', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Telefone: {dados.get('telefone', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"E-mail: {dados.get('email', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Usuário: {dados.get('usuario', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Permissão: {dados.get('permissao', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Situação: {dados.get('situacao', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Admissão: {dados.get('data_admissao', '')}").pack(anchor="w", padx=10, pady=2)

        endereco_str = f"{dados.get('rua', '')}, {dados.get('numero', '')}, {dados.get('bairro', '')}, {dados.get('cidade', '')} - {dados.get('estado', '')}, CEP: {dados.get('cep', '')}"
        ttk.Label(info_frame, text=f"Endereço: {endereco_str}").pack(anchor="w", padx=10, pady=2)

        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)

        botoes = [("Sair", lambda: self.SAIR(self.funcionario_logado_id))]
        for i, (texto, cmd) in enumerate(botoes):
            btn = ttk.Button(btn_frame, text=texto, command=cmd)
            btn.grid(row=0, column=i, padx=5)

    
    def SAIR(self, funcionario_logado_id):
        import tkinter as tk
        from TELAS.TELA_LOGIN import TELA_LOGIN

        self.root.withdraw()
        novo_root = tk.Toplevel()
        TELA_LOGIN(novo_root)
        novo_root.mainloop()
        print(f"Funcionário ID {funcionario_logado_id} saiu e retornou ao login.")
