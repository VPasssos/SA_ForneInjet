from tkinter import ttk
class TELA_USER:
    def __init__(self, root, id_funcionario):
        self.root = root
        self.root.title("Sistema ForneInjet - Gestão Completa - USER")
        self.root.geometry("1200x800")
        self.funcionario_logado_id = id_funcionario
        self.CRIAR_WIDGETS()
    def CRIAR_WIDGETS(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        self.ABA_CONFIGURACAO()
from tkinter import ttk

class TELA_USER:
    def __init__(self, root, id_funcionario):
        self.root = root
        self.root.title("Sistema ForneInjet - Gestão Completa - USER")
        self.root.geometry("1200x800")
        self.funcionario_logado_id = id_funcionario
        self.CRIAR_WIDGETS()
    
    def CRIAR_WIDGETS(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        self.ABA_CONFIGURACAO()
    
    def ABA_CONFIGURACAO(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Configuração")
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=5)
        botoes = [
            ("Sair", lambda: self.SAIR(self.funcionario_logado_id))
        ]
        for i, (texto, cmd) in enumerate(botoes):
            btn = ttk.Button(btn_frame, text=texto, command=cmd)
            btn.grid(row=0, column=i, padx=5)
    
    def SAIR(self, funcionario_logado_id):
        print(f"Funcionário ID {funcionario_logado_id} solicitou sair")