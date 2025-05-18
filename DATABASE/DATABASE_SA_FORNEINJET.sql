-- ======================
-- CRIAÇÃO DO BANCO
-- ======================
CREATE DATABASE ForneInjet;
USE ForneInjet;

-- ======================
-- TABELA: Funcionário
-- ======================
CREATE TABLE Funcionario (
    ID_Funcionario INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(50),
    telefone VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    permissao VARCHAR(20), -- Ex: 'admin', 'usuario'
    situacao VARCHAR(20),  -- Ex: 'ativo', 'inativo'
    data_admissao DATE
);

-- ======================
-- TABELA: Endereço do Funcionário
-- ======================
CREATE TABLE EnderecoFuncionario (
    ID_EnderecoFunc INT PRIMARY KEY AUTO_INCREMENT,
    ID_Funcionario INT,
    rua VARCHAR(100),
    numero VARCHAR(10),
    bairro VARCHAR(50),
    cidade VARCHAR(50),
    estado VARCHAR(50),
    cep VARCHAR(20),
    FOREIGN KEY (ID_Funcionario) REFERENCES Funcionario(ID_Funcionario)
);

-- ======================
-- TABELA: Fornecedor
-- ======================
CREATE TABLE Fornecedor (
    ID_Fornecedor INT PRIMARY KEY AUTO_INCREMENT,
    NM_Fornecedor VARCHAR(100) NOT NULL,
    CNPJ VARCHAR(20) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(100),
    cadastrado_por INT,
    FOREIGN KEY (cadastrado_por) REFERENCES Funcionario(ID_Funcionario)
);

-- ======================
-- TABELA: Endereço do Fornecedor
-- ======================
CREATE TABLE EnderecoFornecedor (
    ID_EnderecoForn INT PRIMARY KEY AUTO_INCREMENT,
    ID_Fornecedor INT,
    rua VARCHAR(100),
    numero VARCHAR(10),
    bairro VARCHAR(50),
    cidade VARCHAR(50),
    estado VARCHAR(50),
    cep VARCHAR(20),
    FOREIGN KEY (ID_Fornecedor) REFERENCES Fornecedor(ID_Fornecedor)
);

-- ======================
-- TABELA: Injetora
-- ======================
CREATE TABLE Injetora (
    ID_Injetora INT PRIMARY KEY AUTO_INCREMENT,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    tipo_de_controle VARCHAR(50),
    capacidade_de_injecao INT,
    forca_de_fechamento INT,
    preco_medio_USD DECIMAL(10,2),
    preco_medio_BRL DECIMAL(10,2),
    quantidade INT DEFAULT 0,
    observacao TEXT,
    ID_Fornecedor INT,
    FOREIGN KEY (ID_Fornecedor) REFERENCES Fornecedor(ID_Fornecedor)
);

-- ======================
-- TABELA: Compra
-- ======================
CREATE TABLE Compra (
    ID_Compra INT PRIMARY KEY AUTO_INCREMENT,
    ID_Fornecedor INT NOT NULL,
    ID_Funcionario INT NOT NULL,
    data_compra DATE NOT NULL,
    data_entrega_prevista DATE,
    data_entrega_real DATE,
    status_compra VARCHAR(20) NOT NULL DEFAULT 'pendente',
    forma_pagamento VARCHAR(50),
    valor_total_USD DECIMAL(12,2),
    valor_total_BRL DECIMAL(12,2),
    numero_nota_fiscal VARCHAR(50),
    observacoes TEXT,
    FOREIGN KEY (ID_Fornecedor) REFERENCES Fornecedor(ID_Fornecedor),
    FOREIGN KEY (ID_Funcionario) REFERENCES Funcionario(ID_Funcionario)
);

-- ======================
-- TABELA: ItemCompra
-- ======================
CREATE TABLE ItemCompra (
    ID_ItemCompra INT PRIMARY KEY AUTO_INCREMENT,
    ID_Compra INT,
    ID_Injetora INT,
    quantidade INT NOT NULL,
    preco_unitario_BRL DECIMAL(10,2),
    preco_unitario_USD DECIMAL(10,2),
    FOREIGN KEY (ID_Compra) REFERENCES Compra(ID_Compra),
    FOREIGN KEY (ID_Injetora) REFERENCES Injetora(ID_Injetora)
);

-- ======================
-- TABELA: Cliente
-- ======================
CREATE TABLE Cliente (
    ID_Cliente INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    CNPJ VARCHAR(20) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    cadastrado_por INT,
    FOREIGN KEY (cadastrado_por) REFERENCES Funcionario(ID_Funcionario)
);

-- ======================
-- TABELA: Endereço do Cliente
-- ======================
CREATE TABLE EnderecoCliente (
    ID_EnderecoCli INT PRIMARY KEY AUTO_INCREMENT,
    ID_Cliente INT,
    rua VARCHAR(100),
    numero VARCHAR(10),
    bairro VARCHAR(50),
    cidade VARCHAR(50),
    estado VARCHAR(50),
    cep VARCHAR(20),
    FOREIGN KEY (ID_Cliente) REFERENCES Cliente(ID_Cliente)
);

-- ======================
-- TABELA: Venda
-- ======================
CREATE TABLE Venda (
    ID_Venda INT PRIMARY KEY AUTO_INCREMENT,
    ID_Cliente INT NOT NULL,
    ID_Funcionario INT NOT NULL,
    data_venda DATE NOT NULL,
    forma_pagamento VARCHAR(50),
    valor_total_BRL DECIMAL(12,2),
    valor_total_USD DECIMAL(12,2),
    observacoes TEXT,
    status_aprovacao VARCHAR(20),
    FOREIGN KEY (ID_Cliente) REFERENCES Cliente(ID_Cliente),
    FOREIGN KEY (ID_Funcionario) REFERENCES Funcionario(ID_Funcionario)
);

-- ======================
-- TABELA: ItemVenda
-- ======================
CREATE TABLE ItemVenda (
    ID_ItemVenda INT PRIMARY KEY AUTO_INCREMENT,
    ID_Venda INT,
    ID_Injetora INT,
    quantidade INT NOT NULL,
    preco_unitario_BRL DECIMAL(10,2),
    preco_unitario_USD DECIMAL(10,2),
    FOREIGN KEY (ID_Venda) REFERENCES Venda(ID_Venda),
    FOREIGN KEY (ID_Injetora) REFERENCES Injetora(ID_Injetora)
);
