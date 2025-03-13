import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.inicio_frame = ttk.Frame(root)
        self.inicio_frame.pack(fill="both", expand=True)

        # Criando a Treeview
        self.inic_table = ttk.Treeview(self.inicio_frame, columns=("ID", "Tipo", "Marca", "Modelo", "Capacidade de Injeção", "Força de Fechamento", "Tipo de Controle", "Preço USD", "Preço BRL", "Fornecedor", "Observação"), show="headings")
        self.inic_table.pack(padx=10, pady=10, fill="both", expand=True)

        # Definindo os cabeçalhos
        for col in self.inic_table["columns"]:
            self.inic_table.heading(col, text=col)

        # Adicionar uma barra de rolagem
        self.scrollbar = ttk.Scrollbar(self.inicio_frame, orient="vertical", command=self.inic_table.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.inic_table.configure(yscrollcommand=self.scrollbar.set)

        # Ajustar a largura das colunas
        self.ajustar_largura_colunas()

    def ajustar_largura_colunas(self):
        for col in self.inic_table["columns"]:
            max_length = 0
        for item in self.inic_table.get_children():
            # Obter o texto da célula para cada item
            text = self.inic_table.item(item)["values"][self.inic_table["columns"].index(col)]
            max_length = max(max_length, len(str(text)))
        
        # Ajustar a largura da coluna com base no comprimento máximo do texto
        self.inic_table.column(col, width=max_length * 1)  # Multiplicar por 10 para ajustar um pouco mais

# Exemplo de uso
root = tk.Tk()
app = App(root)
root.mainloop()
