# Importa os módulos necessários do tkinter e os módulos personalizados do projeto
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Frame, Label
from TELAS.TELA_ADM import TELA_ADM
from TELAS.TELA_USER import TELA_USER
from TELAS.TELA_GERENTE import TELA_GERENTE
from CONFIG import get_connection

# Classe principal da tela de login
class TELA_LOGIN:
    def __init__(self, root):
        self.root = root
        self.root.title("SA FornInjet - Login")  # Define o título da janela
        self.root.geometry("600x300")  # Define tamanho da janela
        self.root.configure(background="white")  # Cor de fundo branca
        self.root.attributes("-alpha", 0.9)  # Transparência da janela

        # Carrega a imagem da logo
        self.logo = PhotoImage(file="ICONES/LogoForneInjet.png")

        # Chama o método que monta a interface
        self.INTERFACE()

    def INTERFACE(self):
        # Cria o frame esquerdo com a logo
        left_frame = Frame(self.root, width=200, height=300, bg="white", relief="raise")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Insere a logo no frame esquerdo
        logo_label = Label(left_frame, image=self.logo, bg="white")
        logo_label.place(x=25, y=85)

        # Cria o frame direito com o formulário de login
        right_frame = Frame(self.root, width=395, height=300, bg="white", relief="raise")
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Campo de entrada para o nome de usuário
        ttk.Label(right_frame, text="Usuário:", font=("Century Gothic", 20), background="white").place(x=5, y=100)
        self.usuario_entry = ttk.Entry(right_frame, width=30)
        self.usuario_entry.place(x=120, y=115)
        self.usuario_entry.focus()  # Define foco inicial no campo de usuário

        # Campo de entrada para senha (com ocultação de caracteres)
        ttk.Label(right_frame, text="Senha:", font=("Century Gothic", 20), background="white").place(x=5, y=150)
        self.senha_entry = ttk.Entry(right_frame, width=30, show="*")
        self.senha_entry.place(x=120, y=165)

        # Botão de login que chama o método de verificação
        ttk.Button(right_frame, text="LOGIN", width=15, command=self.VERIFICAR_LOGIN).place(x=80, y=225)

        # Permite pressionar Enter para fazer login
        self.root.bind('<Return>', lambda event: self.VERIFICAR_LOGIN())

    def VERIFICAR_LOGIN(self):
        # Obtém os dados dos campos de entrada
        usuario = self.usuario_entry.get().strip()
        senha = self.senha_entry.get().strip()

        # Valida se ambos os campos foram preenchidos
        if not usuario or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        # Conecta ao banco de dados
        conn = get_connection()
        cursor = conn.cursor()

        # Executa a consulta para verificar as credenciais
        cursor.execute("""
            SELECT id_funcionario, permissao 
            FROM funcionario 
            WHERE usuario = %s AND senha = %s AND situacao = 'ativo'
        """, (usuario, senha))

        # Recupera o primeiro resultado da consulta
        resultado = cursor.fetchone()

        # Fecha o cursor e a conexão com o banco
        cursor.close()
        conn.close()

        # Se encontrou um usuário válido, redireciona para a tela correspondente
        if resultado:
            id_funcionario, permissao = resultado
            self.ABRIR_TELA_PRINCIPAL(permissao, id_funcionario)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos ou funcionário inativo!")

    def ABRIR_TELA_PRINCIPAL(self, permissao, id_funcionario):
        # Cria uma nova janela principal
        main_window = tk.Toplevel()
        main_window.state('zoomed')  # Abre a janela em tela cheia

        # Direciona para a tela correta com base na permissão do usuário
        if permissao == "admin":
            TELA_ADM(main_window, id_funcionario)
        elif permissao == "gestor":
            TELA_GERENTE(main_window, id_funcionario)
        else:
            TELA_USER(main_window, id_funcionario)

        # Esconde a tela de login
        self.root.withdraw()

        # Define ação para quando a nova janela for fechada
        main_window.protocol("WM_DELETE_WINDOW", self.VOLTAR_LOGIN)
    
    def VOLTAR_LOGIN(self):
        # Fecha a tela atual e reabre a tela de login
        self.root.destroy()
        novo_root = tk.Tk()
        TELA_LOGIN(novo_root)
        novo_root.mainloop()
