import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Frame, Label
from TELAS.TELA_ADM import TELA_ADM
from TELAS.TELA_USER import TELA_USER
from TELAS.TELA_GERENTE import TELA_GERENTE
from CONFIG import get_connection
class TELA_LOGIN:
    def __init__(self, root):
        self.root = root
        self.root.title("SA FornInjet - Login")
        self.root.geometry("600x300")
        self.root.configure(background="white")
        self.root.attributes("-alpha", 0.9)
        self.logo = PhotoImage(file="ICONES/LogoForneInjet.png")
        self.INTERFACE()

    def INTERFACE(self):
        # Frame esquerdo (logo)
        left_frame = Frame(self.root, width=200, height=300, bg="white", relief="raise")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        logo_label = Label(left_frame, image=self.logo, bg="white")
        logo_label.place(x=25, y=85)

        # Frame direito (formulário)
        right_frame = Frame(self.root, width=395, height=300, bg="white", relief="raise")
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Campos de login
        ttk.Label(right_frame, text="Usuário:", font=("Century Gothic", 20), background="white").place(x=5, y=100)
        self.usuario_entry = ttk.Entry(right_frame, width=30)
        self.usuario_entry.place(x=120, y=115)
        self.usuario_entry.focus()

        ttk.Label(right_frame, text="Senha:", font=("Century Gothic", 20), background="white").place(x=5, y=150)
        self.senha_entry = ttk.Entry(right_frame, width=30, show="*")
        self.senha_entry.place(x=120, y=165)

        # Botão de login
        ttk.Button(right_frame, text="LOGIN", width=15, command=self.VERIFICAR_LOGIN).place(x=80, y=225)
        self.root.bind('<Return>', lambda event: self.VERIFICAR_LOGIN())

    def VERIFICAR_LOGIN(self):
        usuario = self.usuario_entry.get().strip()
        senha = self.senha_entry.get().strip()

        if not usuario or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_funcionario, permissao 
            FROM funcionario 
            WHERE usuario = %s AND senha = %s AND situacao = 'ativo'
        """, (usuario, senha))
        resultado = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if resultado:
            id_funcionario, permissao = resultado
            self.ABRIR_TELA_PRINCIPAL(permissao, id_funcionario)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos ou funcionário inativo!")

    def ABRIR_TELA_PRINCIPAL(self, permissao, id_funcionario):
        main_window = tk.Toplevel()
        main_window.state('zoomed')

        if permissao == "admin":
            TELA_ADM(main_window, id_funcionario)
            self.root.withdraw()
        elif permissao == "gestor":
            TELA_GERENTE(main_window, id_funcionario)
            self.root.withdraw()
        else:
            TELA_USER(main_window, id_funcionario)
            self.root.withdraw()
        main_window.protocol("WM_DELETE_WINDOW", self.VOLTAR_LOGIN)
    
    def VOLTAR_LOGIN(self):
        self.root.destroy()
        novo_root = tk.Tk()
        TELA_LOGIN(novo_root)
        novo_root.mainloop()
