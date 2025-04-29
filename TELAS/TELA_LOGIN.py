import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Frame, Label
from CRUD.CRUD_FUNCIONARIO import Database
from TELAS.TELA_ADM import TelaPrincipal

class TelaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("SA ForneInjet - Painel de Acesso")
        self.root.geometry("600x300")
        self.root.configure(background="white")
        self.root.attributes("-alpha", 0.9)
        
        # Carregar recursos
        self.logo = PhotoImage(file="ICONES/LogoForneInjet.png")
        
        # Configurar layout
        self.configurar_interface()
        
        # Conectar ao banco
        self.db = Database()

    def configurar_interface(self):
        """Configura todos os elementos da interface"""
        # Frame esquerdo (logo)
        left_frame = Frame(self.root, width=200, height=300, bg="white", relief="raise")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        logo_label = Label(left_frame, image=self.logo, bg="white")
        logo_label.place(x=25, y=85)

        # Frame direito (formulário)
        right_frame = Frame(self.root, width=395, height=300, bg="white", relief="raise")
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Campos de login
        ttk.Label(right_frame, text="Usuário:", font=("Century Gothic", 20), 
                 background="white").place(x=5, y=100)
        self.usuario_entry = ttk.Entry(right_frame, width=30)
        self.usuario_entry.place(x=120, y=115)
        self.usuario_entry.focus()

        ttk.Label(right_frame, text="Senha:", font=("Century Gothic", 20), 
                 background="white").place(x=5, y=150)
        self.senha_entry = ttk.Entry(right_frame, width=30, show="*")
        self.senha_entry.place(x=120, y=165)

        # Botão de login
        ttk.Button(right_frame, text="LOGIN", width=15, 
                  command=self.verificar_login).place(x=80, y=225)
        
        # Configurar tecla Enter para login
        self.root.bind('<Return>', lambda event: self.verificar_login())

    def verificar_login(self):
        """Verifica as credenciais do usuário"""
        usuario = self.usuario_entry.get().strip()
        senha = self.senha_entry.get().strip()

        if not usuario or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            self.db.cursor.execute("""
                SELECT permissao FROM funcionario
                WHERE usuario = %s AND senha = %s
            """, (usuario, senha))
            
            resultado = self.db.cursor.fetchone()

            if resultado:
                permissao = resultado[0]
                mensagem = "Bem-vindo, Administrador!" if permissao == "admin" else "Bem-vindo, Usuário!"
                messagebox.showinfo("Login", f"Acesso Confirmado. {mensagem}")
                
                self.root.withdraw()
                self.abrir_tela_principal(permissao)
            else:
                messagebox.showerror("Erro", "Credenciais inválidas!")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao verificar login: {str(e)}")

    def abrir_tela_principal(self, permissao):
        """Abre a tela principal conforme a permissão"""
        main_window = tk.Toplevel()
        main_window.state('zoomed')  # Maximiza a janela
        
        if permissao == "admin":
            TelaPrincipal(main_window)
        # else:
        #     TELAABAS_USUARIO(main_window)  # Descomente quando implementar
            
        main_window.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)

    def fechar_aplicacao(self):
        """Fecha todas as janelas e encerra a aplicação"""
        self.db.close_connection()
        self.root.destroy()
