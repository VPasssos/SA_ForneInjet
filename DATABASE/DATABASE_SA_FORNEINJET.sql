-- ======================
-- CRIAÇÃO DO BANCO
-- ======================
CREATE DATABASE IF NOT EXISTS forneinjet;
USE forneinjet;

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
    permissao VARCHAR(20), -- Ex: 'admin', 'usuario', 'gestor'
    situacao VARCHAR(20) DEFAULT 'ativo',  -- Ex: 'ativo', 'inativo'
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
    preco_medio_BRL DECIMAL(10,2),
    quantidade INT DEFAULT 0,
    observacao TEXT,
    ID_Fornecedor INT,
    FOREIGN KEY (ID_Fornecedor) REFERENCES Fornecedor(ID_Fornecedor)
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
    observacoes TEXT,
    status_aprovacao VARCHAR(20) DEFAULT 'Em análise', -- 'Aprovado', 'Reprovado', 'Em análise'
    aprovado_por INT, -- ID do gestor que aprovou/reprovou
    data_aprovacao DATETIME, -- Data e hora da aprovação/reprovação
    FOREIGN KEY (ID_Cliente) REFERENCES Cliente(ID_Cliente),
    FOREIGN KEY (ID_Funcionario) REFERENCES Funcionario(ID_Funcionario),
    FOREIGN KEY (aprovado_por) REFERENCES Funcionario(ID_Funcionario)
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
    FOREIGN KEY (ID_Venda) REFERENCES Venda(ID_Venda),
    FOREIGN KEY (ID_Injetora) REFERENCES Injetora(ID_Injetora)
);


-- ======================
-- ÍNDICES PARA MELHOR PERFORMANCE
-- ======================
CREATE INDEX idx_venda_status ON Venda(status_aprovacao);
CREATE INDEX idx_venda_cliente ON Venda(ID_Cliente);
CREATE INDEX idx_venda_funcionario ON Venda(ID_Funcionario);
CREATE INDEX idx_venda_data ON Venda(data_venda);
CREATE INDEX idx_item_venda ON ItemVenda(ID_Venda);

-- ======================
-- TRIGGERS DE ESTOQUE BASEADO EM APROVAÇÃO
-- ======================
DELIMITER $$

-- Abaixa o estoque ao aprovar a venda
CREATE TRIGGER tr_aprova_venda_estoque
AFTER UPDATE ON Venda
FOR EACH ROW
BEGIN
    IF OLD.status_aprovacao <> 'Aprovado' AND NEW.status_aprovacao = 'Aprovado' THEN
        UPDATE Injetora i
        JOIN ItemVenda iv ON iv.ID_Injetora = i.ID_Injetora
        SET i.quantidade = i.quantidade - iv.quantidade
        WHERE iv.ID_Venda = NEW.ID_Venda;
    END IF;
END$$

-- Reverte o estoque se a venda aprovada for reprovada depois
CREATE TRIGGER tr_reprova_venda_estoque
AFTER UPDATE ON Venda
FOR EACH ROW
BEGIN
    IF OLD.status_aprovacao = 'Aprovado' AND NEW.status_aprovacao = 'Reprovado' THEN
        UPDATE Injetora i
        JOIN ItemVenda iv ON iv.ID_Injetora = i.ID_Injetora
        SET i.quantidade = i.quantidade + iv.quantidade
        WHERE iv.ID_Venda = NEW.ID_Venda;
    END IF;
END$$

DELIMITER ;
