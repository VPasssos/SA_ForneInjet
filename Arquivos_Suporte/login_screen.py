import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tela_abas import TelaAbas  # Importando a classe com as abas

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Tela de Login")
        self.root.geometry("600x300")
        self.root.configure(background="white")

        # Tela de login com campos de usuário e senha
        self.create_widgets()

    def create_widgets(self):
        # Campos de Login
        self.usuario_label = tk.Label(self.root, text="Usuário:", font=("Century Gothic", 14), bg="white")
        self.usuario_label.pack(pady=10)

        self.usuario_entry = ttk.Entry(self.root, width=30)
        self.usuario_entry.pack(pady=5)

        self.senha_label = tk.Label(self.root, text="Senha:", font=("Century Gothic", 14), bg="white")
        self.senha_label.pack(pady=10)

        self.senha_entry = ttk.Entry(self.root, width=30, show="*")
        self.senha_entry.pack(pady=5)

        # Botão de login
        self.login_button = ttk.Button(self.root, text="Login", width=15, command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()

        # Aqui você pode validar o login com um banco de dados ou uma lista de usuários.
        # Por enquanto, vamos usar uma validação simples:
        if usuario == "1" and senha == "1":
            # Login bem-sucedido, chama a tela com as abas
            self.root.withdraw()  # Oculta a tela de login
            self.show_main_screen()  # Chama a função para mostrar as abas
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    def show_main_screen(self):
        main_window = tk.Toplevel()  # Cria uma nova janela
        main_window.geometry("600x400")  # Define o tamanho da nova janela
        app = TelaAbas(main_window)  # Cria a instância da tela com as abas
        main_window.mainloop()
