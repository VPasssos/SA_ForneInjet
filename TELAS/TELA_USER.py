from tkinter import ttk
from CRUDS.CRUD_FUNCIONARIO import UPD_DADOS_FUNCIONARIOS
from CRUDS.CRUD_VENDA import *

class TELA_USER:
    """Classe principal da interface do usuário (funcionário)"""
    
    def __init__(self, root, id_funcionario):
        """
        Inicializa a tela do usuário
        
        Args:
            root: Janela principal
            id_funcionario: ID do funcionário logado
        """
        self.root = root
        self.root.title("Sistema ForneInjet - Gestão Completa - USER")
        self.root.geometry("1200x800")
        self.funcionario_logado_id = id_funcionario
        # Carrega os dados do funcionário logado
        self.funcionario_dados = UPD_DADOS_FUNCIONARIOS(self.funcionario_logado_id)
        self.CRIAR_WIDGETS()
    
    def CRIAR_WIDGETS(self):
        """Cria os widgets principais da interface"""
        self.notebook = ttk.Notebook(self.root)  # Cria um notebook para abas
        self.notebook.pack(fill="both", expand=True)
        
        # Cria as abas principais
        self.ABA_VENDA()
        self.ABA_CONFIGURACAO()

    def ABA_VENDA(self):
        """Cria a aba de vendas com formulário e tabela"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="VENDAS")
        
        # Frame do formulário de venda
        form_frame = ttk.LabelFrame(frame, text="Dados da Venda", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        # Obtém listas de clientes e injetoras para os comboboxes
        from CRUDS.CRUD_CLIENTE import GET_CLIENTES  
        from CRUDS.CRUD_INJETORA import GET_INJETORA  
        clientes = GET_CLIENTES()
        injetoras = GET_INJETORA()
        
        # Prepara listas de nomes para os comboboxes
        nomes_clientes = [cliente[1] for cliente in clientes]
        nomes_injetoras = [injetora[1] for injetora in injetoras]
        
        # Configuração dos campos do formulário
        campos = [
            ("Cliente", 0, 0), ("Produto", 0, 2),
            ("Quantidade", 1, 0), ("Preço Unitário (BRL)", 1, 2),
            ("Forma Pagamento", 2, 0), ("Observações", 2, 2)
        ]
        
        self.entries_venda = {}  # Dicionário para armazenar referências aos campos
        for campo, row, col in campos:
            # Cria label para cada campo
            lbl = ttk.Label(form_frame, text=f"{campo}:")
            lbl.grid(row=row, column=col, padx=5, pady=5, sticky="e")
            
            # Cria campos específicos conforme o tipo
            if campo == "Cliente":
                entry = ttk.Combobox(form_frame, width=30, values=nomes_clientes) 
                self.cliente_cb_venda = entry  # Armazena referência especial para o combobox de cliente
            elif campo == "Produto":
                entry = ttk.Combobox(form_frame, width=30, values=nomes_injetoras) 
                self.produto_cb_venda = entry  # Armazena referência especial para o combobox de produto
            elif campo == "Status Aprovação":
                entry = ttk.Combobox(form_frame, width=27, 
                                    values=["Aprovado", "Reprovado", "Em análise"])
            elif campo == "Data Venda":
                entry = ttk.Entry(form_frame, width=30)  
            else:
                entry = ttk.Entry(form_frame, width=30)
            
            # Posiciona o campo na grade
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
            self.entries_venda[campo] = entry  # Armazena referência ao campo

        # Campo oculto para armazenar o ID da venda
        self.venda_id = ttk.Entry(form_frame)  
        self.venda_id.grid(row=0, column=4)
        self.venda_id.grid_remove()  # Oculta o campo

        # Frame para botões
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        # Botões principais
        botoes = [
            ("Novo", lambda: ADD_VENDA(self.entries_venda, self.cliente_cb_venda, 
                                      self.produto_cb_venda, self.tree_vendas, 
                                      self.funcionario_logado_id)),
            ("Consultar", lambda: CONSULTAR_SOLICITACAO(self.funcionario_logado_id, self.root))
        ]
        
        # Posiciona os botões na grade
        for i, (texto, cmd) in enumerate(botoes):
            btn = ttk.Button(btn_frame, text=texto, command=cmd)
            btn.grid(row=0, column=i, padx=5)

        # Frame para a tabela de vendas
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Configuração das colunas da tabela
        cols = ["ID", "Cliente", "Produto", "Quantidade", "Preço Unitário (BRL)", 
                "Data da Venda", "Forma Pagamento", "Status Aprovação", 
                "Cadastrante", "Observações"]
        self.tree_vendas = ttk.Treeview(table_frame, columns=cols, 
                                       show="headings", height=15)

        # Configura cada coluna da tabela
        for col in cols:
            width = 100 
            if col == "ID":
                width = 50  
            elif col == "Observações":
                width = 150 
            elif col == "Data da Venda":
                width = 120 
            self.tree_vendas.heading(col, text=col)
            self.tree_vendas.column(col, width=width, 
                                   anchor='w' if col == "Observações" else 'center')

        # Adiciona scrollbar à tabela
        scroll = ttk.Scrollbar(table_frame, orient="vertical", 
                              command=self.tree_vendas.yview)
        scroll.pack(side="right", fill="y")
        self.tree_vendas.configure(yscrollcommand=scroll.set)

        # Inicialmente oculta a tabela (será mostrada quando populada)
        self.tree_vendas.pack_forget()

    def Consultar_Solicitacao(self, event=None):
        """Filtra as vendas na tabela conforme termo de busca"""
        termo = self.search_entry_venda.get().lower()

        if termo == "":
            # Se busca vazia, recarrega todas as vendas
            UPD_TABELA_VENDAS(self.tree_vendas)
        else:
            if not termo:
                # Se termo vazio, mostra todos os itens
                for child in self.tree_vendas.get_children(""):  
                    self.tree_vendas.reattach(child, "", "end")
                return

            # Filtra os itens conforme o termo de busca
            for child in self.tree_vendas.get_children(""):
                valores = self.tree_vendas.item(child)["values"]
                texto = " ".join(str(v) for v in valores).lower()
                if termo in texto:
                    self.tree_vendas.reattach(child, "", "end")
                else:
                    self.tree_vendas.detach(child)

    def ABA_CONFIGURACAO(self):
        """Cria a aba de configuração do usuário"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="CONFIGURAÇÃO")

        # Frame com informações do funcionário
        info_frame = ttk.LabelFrame(frame, text="Dados do Funcionário")
        info_frame.pack(fill="x", padx=10, pady=10)

        dados = self.funcionario_dados

        # Exibe todos os dados do funcionário em labels
        ttk.Label(info_frame, text=f"Nome: {dados.get('nome', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Cargo: {dados.get('cargo', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Telefone: {dados.get('telefone', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"E-mail: {dados.get('email', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Usuário: {dados.get('usuario', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Permissão: {dados.get('permissao', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Situação: {dados.get('situacao', '')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Admissão: {dados.get('data_admissao', '')}").pack(anchor="w", padx=10, pady=2)

        # Formata e exibe o endereço completo
        endereco_str = f"{dados.get('rua', '')}, {dados.get('numero', '')}, {dados.get('bairro', '')}, {dados.get('cidade', '')} - {dados.get('estado', '')}, CEP: {dados.get('cep', '')}"
        ttk.Label(info_frame, text=f"Endereço: {endereco_str}").pack(anchor="w", padx=10, pady=2)

        # Frame para botões
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)

        # Botão de sair
        botoes = [("Sair", lambda: self.SAIR(self.funcionario_logado_id))]
        for i, (texto, cmd) in enumerate(botoes):
            btn = ttk.Button(btn_frame, text=texto, command=cmd)
            btn.grid(row=0, column=i, padx=5)

    def SAIR(self, funcionario_logado_id):
        """Encerra a sessão e volta para a tela de login"""
        import tkinter as tk
        from TELAS.TELA_LOGIN import TELA_LOGIN

        # Oculta a janela atual
        self.root.withdraw()
        # Cria nova janela para o login
        novo_root = tk.Toplevel()
        TELA_LOGIN(novo_root)
        novo_root.mainloop()
        print(f"Funcionário ID {funcionario_logado_id} saiu e retornou ao login.")