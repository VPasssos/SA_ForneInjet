import tkinter as tk 
from tkinter import messagebox 
from CRUD_Funcionarios import create_funcioario,read_funcionario, update_funcionario,delete_funcionario
#nome_funcionario,telefone,email,cargo,departamento,data_addmissao,situacao,permicao

class CRUDApp: 
    def __init__(self,root):
        self.root = root
        self.root.title("CRUD funcionarios")

        #ccriacao de widgets 
        self.create_widgets()  

    def create_widgets(self):
        #labels
        tk.Label(self.root,text="funcionario:").grid(row=0,column=0)
        tk.Label(self.root,text="telefone:").grid(row=1,column=0)
        tk.Label(self.root,text="email:").grid(row=2,column=0)
        tk.Label(self.root,text="cargo:").grid(row=3,column=0)
        tk.Label(self.root,text="departamento:").grid(row=4,column=0)
        tk.Label(self.root,text="data de admissão:").grid(row=5,column=0)
        tk.Label(self.root,text="situação:").grid(row=6,column=0)
        tk.Label(self.root,text="permição:").grid(row=7,column=0)
                   
              
        tk.Label(self.root,text="IDFUNCIONARIO(for update/delete)").grid(row=8,column=0)


        #CRIAR AS CAIXAS PARA DIGITAR OS VALORES
        self.nome_funcionario_entry = tk.Entry(self.root)
        self.telefone_entry = tk.Entry(self.root)
        self.email_entry = tk.Entry(self.root)
        self.cargo_entry = tk.Entry(self.root)
        self.departamento_entry = tk.Entry(self.root)
        self.data_admissao_entry = tk.Entry(self.root)
        self.situacao_entry = tk.Entry(self.root)
        self.permicao_entry = tk.Entry(self.root)
        self.idfuncionario_entry = tk.Entry(self.root)

        self.nome_funcionario_entry(row=0,column=1)
        self.telefone_entry.grid(row=1,column=1)
        self.email_entry.grid(row=2,column=1)
        self.cargo_entry.grid(row=3,column=1)
        self.departamento_entry(row=4,column=1)
        self.data_admissao_entry.grid(row=5,column=1)
        self.situacao_entry.grid(row=6,column=1)
        self.situacao_entry(row=7,column=1)

        self.idfuncionario_entry.grid(row=8,column=1)
        

        #botoes do crud
        tk.Button(self.root,text="adicionar funcionario",command=self.create_user).grid(row=6,column=0,columnspan=1)
        tk.Button(self.root,text="listar funcionario",command=self.create_user).grid(row=6,column=1,columnspan=1)
        tk.Button(self.root,text="alterar funcionario",command=self.create_user).grid(row=7,column=0,columnspan=1)
        tk.Button(self.root,text="excluir funcionario",command=self.create_user).grid(row=7,column=1,columnspan=1)
        self.text_area = tk.Text(self.root,heigth=10,witdh=80)
        self.text_area.grid(row=10,column=0,cplomnspan=4)

    def create_funcioario(self):
        nome = self.nome_funcionario_entry.get()
        telefone = self.telefone_entry.get()
        email = self.email_entry.get()
        cargo = self.cargo_entry.get()
        departamento = self.departamento_entry.get()
        data_admissao = self.data_admissao_entry.get()
        situacao = self.situacao_entry.get()
        permicao = self.permicao_entry.get()
       
        if  nome and telefone and email and cargo and departamento and data_admissao and situacao and permicao:
            create_funcioario(nome,telefone,email,cargo,departamento,data_admissao,situacao,permicao)
            self.nome_funcionario_entry.delete(0,tk.END) 
            self.telefone_entry.delete(0,tk.END)
            self.email_entry.delete(0,tk.END)
            self.cargo_entry.delete(0,tk.END)
            self.departamento_entry.delete(0,tk.END)
            self.data_admissao_entry.delete(0,tk.END)
            self.situacao_entry.delete(0,tk.END)
            self.permicao_entry.delete(0,tk.END)
            messagebox.showerror("sucess","funcionario adicionado com sucesso")

        else:
             messagebox.showerror("error","todos os  campos sao obrigatorios")

    def read_funcionario(self):
        users = read_funcionario()
        self.text_area.delete(1.0,tk.END)
        for user in users:
            self.text_area.insert(tk.END,f"id: {user[0]},nome:{user[1]},telefone:{user[2]},cargo:{user[3]}departamento: {user[4]},data_admissao:{user[5]},situcao:{user[6]},permicao:{user[7]}\n")
    
    def   update_funcionario(self):
        idfuncionario = self.idfuncionario_entry.get() 
        nome = self.nome_funcionario_entry.get()    
        telefone = self.telefone_entry.get()    
        email = self.email_entry.get() 
        cargo = self.cargo_entry.get()    
        usuario = self.departamento_entry.get()
        data_admissao = self.data_admissao_entry.get()    
        situacao = self.situacao_entry.get()
        permicao = self.permicao_entry.get()


        if  idfuncionario and nome and telefone and email and cargo and usuario and data_admissao and situacao and permicao:
                update_funcionario(idfuncionario,nome,telefone,email,usuario,data_admissao,situacao,permicao)
                self.nome_funcionario_entry.delete(0,tk.END) 
                self.telefone_entry.delete(0,tk.END)
                self.email_entry.delete(0,tk.END)
                self.cargo_entry.delete(0,tk.END)
                self.data_admissao_entry.delete(0,tk.END)  
                self.situacao_entry.delete(0,tk.END)
                self.permicao_entry.delete(0,tk.END)  
                messagebox.showerror("sucesso","funcionario alterado com sucesso")
        else:
            messagebox.showerror("error","todos os  campos sao obrigatorios")
                

    def delete_funcionario(self):
        idfuncionario = self.idfuncionario_entry.get()  
        if idfuncionario:
            delete_funcionario(idfuncionario)
            self. idfuncionario_entry.delete(0,tk.END)
            messagebox.showerror("sucesso","funcionario exluido com sucesso!")
        else:        
            messagebox.showerror("error","id de funcionario e necessario!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()
           
