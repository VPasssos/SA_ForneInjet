create database ForneInjet_SA

    create table Funcionario(
        idFuncionario int not null auto_increment,
        nome_funcionario text,
        cargo text,
        telefone text,
        email text,
        data_admissao text,
        situacao text,
        permissao text,
        usuario text,
        senha text,
        primary key (idFuncionario)    
    );

    create table Produto(
        idMaquinas int not null auto_increment,
        tipo text,
        marca text,
        modelo text,
        capacidade_de_injeçao text,
        força_de_fechamento text,
        tipo_de_controle text,
        preço_medio_USD text,
        preço_medio_BRL text,
        fornecedor text,
        observacao text,
        primary key (idMaquinas)    
    );

    create table Fornecedor(
        idFornecedor int not null auto_increment,
        nome_fornecedor text,  
        endereco text,
        telefone text,
        email text,
        contato_principal text,
        website text,
        primary key (idFornecedor)    
    );