import tkinter as tk
from tkinter import ttk

class AbasDinamicasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fechar Aba pelo Nome")
        self.root.geometry("400x300")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.contador_abas = 1

        # Frame de botões
        frame_controle = ttk.Frame(root)
        frame_controle.pack(pady=10)

        # Botão para abrir nova aba
        ttk.Button(frame_controle, text="Abrir Aba", command=self.abrir_aba).grid(row=0, column=0, padx=5)

        # Entrada + botão para fechar aba por nome
        self.entrada_nome = ttk.Entry(frame_controle, width=15)
        self.entrada_nome.grid(row=0, column=1)
        ttk.Button(frame_controle, text="Fechar por Nome", command=self.fechar_aba_por_nome).grid(row=0, column=2, padx=5)

    def abrir_aba(self):
        nova_aba = ttk.Frame(self.notebook)
        nome_aba = f"Aba {self.contador_abas}"
        self.notebook.add(nova_aba, text=nome_aba)

        label = ttk.Label(nova_aba, text=f"Conteúdo da {nome_aba}")
        label.pack(pady=20)

        self.contador_abas += 1

    def fechar_aba_por_nome(self):
        nome_procurado = self.entrada_nome.get()
        for aba_id in self.notebook.tabs():
            if self.notebook.tab(aba_id, option="text") == nome_procurado:
                self.notebook.forget(aba_id)
                break
        else:
            print(f"Aba '{nome_procurado}' não encontrada.")

# Executa a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = AbasDinamicasApp(root)
    root.mainloop()
