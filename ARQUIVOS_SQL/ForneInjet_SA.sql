CREATE DATABASE ForneInjet_SA;
USE ForneInjet_SA;

CREATE TABLE Funcionario (
    idFuncionario INT NOT NULL AUTO_INCREMENT,
    nome_funcionario VARCHAR(100),
    cargo VARCHAR(100),
    telefone VARCHAR(20),
    email VARCHAR(100),
    data_admissao DATE,
    situacao VARCHAR(50),
    permissao VARCHAR(50),
    usuario VARCHAR(50),
    senha VARCHAR(100),
    PRIMARY KEY (idFuncionario)
);

CREATE TABLE Injetora (
    idMaquinas INT NOT NULL AUTO_INCREMENT,
    quantidade INT,
    marca VARCHAR(100),
    modelo VARCHAR(100),
    capacidade_de_injecao VARCHAR(100),
    forca_de_fechamento VARCHAR(100),
    tipo_de_controle VARCHAR(100),
    preco_medio_USD DECIMAL(10,2),
    preco_medio_BRL DECIMAL(10,2),
    fornecedor VARCHAR(100),
    observacao TEXT,
    PRIMARY KEY (idMaquinas)
);

CREATE TABLE Fornecedor (
    idFornecedor INT NOT NULL AUTO_INCREMENT,
    nome_fornecedor VARCHAR(100),  
    cnpj VARCHAR(20),
    email VARCHAR(100),
    endereco VARCHAR(150),
    telefone VARCHAR(20),
    contato_principal VARCHAR(100),
    website VARCHAR(100),
    PRIMARY KEY (idFornecedor)
);
