import tkinter as tk
from tkinter import ttk, messagebox

class TabelaSimples:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Contatos")
        self.root.geometry("900x650")
        
        self.contador_id = 1
        self.criar_widgets()
    
    def criar_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame do formulário
        form_frame = ttk.LabelFrame(main_frame, text="Cadastro de Contato", padding=10)
        form_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Campos do formulário
        campos = [("Nome", 0, 0), ("Telefone", 0, 2), 
                 ("E-mail", 1, 0), ("Cidade", 1, 2)]
        
        self.entries = {}
        for campo, row, col in campos:
            lbl = ttk.Label(form_frame, text=f"{campo}:")
            lbl.grid(row=row, column=col, padx=5, pady=5, sticky="e")
            

            entry = ttk.Entry(form_frame, width=30)
            
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
            self.entries[campo] = entry
        
        # Frame dos botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Botões
        botoes = [
            ("Adicionar", self.adicionar_item),
            ("Editar", self.editar_item),
            ("Remover", self.remover_item),
            ("Limpar", self.limpar_campos),
            ("Filtrar", self.filtrar_itens),
        ]
        
        for i, (texto, cmd) in enumerate(botoes):
            btn = ttk.Button(btn_frame, text=texto, command=cmd)
            btn.grid(row=0, column=i, padx=5, sticky="ew")
            btn_frame.columnconfigure(i, weight=1)
        
        # Frame da tabela
        table_frame = ttk.LabelFrame(main_frame, text="Lista de Contatos", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Barra de pesquisa
        search_frame = ttk.Frame(table_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        lbl_search = ttk.Label(search_frame, text="Pesquisar:")
        lbl_search.pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind("<KeyRelease>", self.filtrar_itens)
        
        # Colunas da tabela
        cols = ["Nome", "Telefone", "E-mail", "Cidade"]
        self.tree = ttk.Treeview(
            table_frame, 
            columns=cols, 
            show="headings", 
            height=10,
            selectmode="browse"
        )
        
        # Configurar cabeçalhos e colunas
        for col in cols:
            self.tree.heading(col, text=col, command=lambda c=col: self.ordenar_por(col))
            self.tree.column(col, width=180, anchor="w")
        
        # Barra de rolagem
        scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Vincular eventos
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_item)
        
        # Dados de exemplo
        self.carregar_dados_exemplo()
    
    def formatar_telefone(self, event):
        """Formata o número de telefone enquanto digita"""
        entry = self.entries["Telefone"]
        texto = entry.get()
        
        # Remove tudo que não for dígito
        digitos = [c for c in texto if c.isdigit()]
        telefone = "".join(digitos)
        
        # Formatação básica
        if len(telefone) > 0:
            telefone_formatado = f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:10]}"
        else:
            telefone_formatado = ""
        
        # Atualiza o valor real
        entry.delete(0, tk.END)
        entry.insert(0, telefone_formatado)

    def carregar_dados_exemplo(self):
        dados = [
            ("João Silva", "(11) 9999-8888", "joao@email.com", "São Paulo"),
            ("Maria Souza", "(21) 7777-6666", "maria@email.com", "Rio de Janeiro"),
            ("Carlos Oliveira", "(31) 5555-4444", "carlos@email.com", "Belo Horizonte")
        ]
        
        for dado in dados:
            self.tree.insert("", tk.END, values=dado)
            self.contador_id += 1
    
    def validar_campos(self):
        """Valida se os campos obrigatórios foram preenchidos"""
        if not self.entries["Nome"].get().strip():
            messagebox.showwarning("Aviso", "O campo Nome é obrigatório!")
            return False
        return True
    
    def adicionar_item(self):
        if not self.validar_campos():
            return
            
        valores = (
            self.entries["Nome"].get().strip(),
            self.entries["Telefone"].get().strip(),
            self.entries["E-mail"].get().strip(),
            self.entries["Cidade"].get().strip()
        )
        
        self.tree.insert("", tk.END, values=valores)
        self.contador_id += 1
        self.limpar_campos()
    
    def editar_item(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para editar!")
            return
            
        if not self.validar_campos():
            return
            
        valores = (
            self.entries["Nome"].get().strip(),
            self.entries["Telefone"].get().strip(),
            self.entries["E-mail"].get().strip(),
            self.entries["Cidade"].get().strip()
        )
        
        self.tree.item(item_selecionado, values=valores)
        self.limpar_campos()
    
    def remover_item(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para remover!")
            return
            
        if messagebox.askyesno("Confirmar", "Deseja realmente remover o contato selecionado?"):
            self.tree.delete(item_selecionado)
            self.limpar_campos()
    
    def selecionar_item(self, event):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            valores = self.tree.item(item_selecionado)["values"]
            for i, campo in enumerate(["Nome", "Telefone", "E-mail", "Cidade"]):
                self.entries[campo].delete(0, tk.END)
                
                if campo == "Telefone":
                    # Mostra asteriscos ou o valor real conforme a configuração
                    self.entries[campo].config(show="")
                    self.entries[campo].insert(0, valores[i] if i < len(valores) else "")
                else:
                    self.entries[campo].insert(0, valores[i] if i < len(valores) else "")
    
    def limpar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    
    def ordenar_por(self, col):
        """Ordena os itens da tabela pela coluna especificada"""
        items = [(self.tree.set(child, col), child) for child in self.tree.get_children("")]
        items.sort()
        
        for index, (val, child) in enumerate(items):
            self.tree.move(child, "", index)
    
    def filtrar_itens(self, event=None):
        """Filtra os itens da tabela conforme o texto digitado"""
        termo = self.search_entry.get().lower()
        
        # Mostra todos os itens se o termo estiver vazio
        if not termo:
            for child in self.tree.get_children(""):
                self.tree.reattach(child, "", "end")
            return
        
        # Filtra os itens
        for child in self.tree.get_children(""):
            valores = self.tree.item(child)["values"]
            texto = " ".join(str(v) for v in valores).lower()
            if termo in texto:
                self.tree.reattach(child, "", "end")
            else:
                self.tree.detach(child)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = TabelaSimples(root)
    root.mainloop()