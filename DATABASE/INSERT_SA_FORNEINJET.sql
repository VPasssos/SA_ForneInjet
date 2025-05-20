USE forneinjet;
INSERT INTO Funcionario (nome, cargo, telefone, email, usuario, senha, permissao, situacao, data_admissao) VALUES
('Ana Carolina Mendes', 'Gerente Comercial', '(11) 98765-4321', 'ana.mendes@forneinjet.com', 'ana.mendes', "ana.123321", 'admin', 'ativo', '2018-05-10'),
('Carlos Eduardo Lima', 'Vendedor Sênior', '(11) 98765-1234', 'carlos.lima@forneinjet.com', 'carlos.lima', 'carlos.321123', 'usuario' , 'ativo', '2019-03-15'),
('Mariana Souza Santos', 'Compradora', '(11) 98765-5678', 'mariana.souza@forneinjet.com', 'mariana.souza', 'mariana.159951', 'gestor', 'ativo', '2020-02-20'),
('Ricardo Oliveira', 'Analista Financeiro', '(11) 98765-8765', 'ricardo.oliveira@forneinjet.com', 'ricardo.oliveira', "ricardo.753357", 'usuario', 'ativo', '2021-07-05'),
('Fernanda Costa', 'Assistente Administrativo', '(11) 98765-2345', 'fernanda.costa@forneinjet.com', 'fernanda.costa', "fernanda.357753", 'usuario', 'ativo', '2022-01-30');
INSERT INTO EnderecoFuncionario (ID_Funcionario, rua, numero, bairro, cidade, estado, cep) VALUES
(1, 'Avenida Paulista', '1000', 'Bela Vista', 'São Paulo', 'SP', '01310-100'),
(2, 'Rua Haddock Lobo', '200', 'Cerqueira César', 'São Paulo', 'SP', '01414-001'),
(3, 'Alameda Santos', '500', 'Jardim Paulista', 'São Paulo', 'SP', '01418-000'),
(4, 'Rua Augusta', '1500', 'Consolação', 'São Paulo', 'SP', '01305-100'),
(5, 'Rua Oscar Freire', '800', 'Jardins', 'São Paulo', 'SP', '01426-001');
INSERT INTO Fornecedor (NM_Fornecedor, CNPJ, telefone, email, website, cadastrado_por) VALUES
('Arburg do Brasil Ltda', '12.345.678/0001-99', '(11) 4003-5588', 'vendas@arburg.com.br', 'www.arburg.com.br', 3),
('Engel Máquinas Ind. Ltda', '23.456.789/0001-88', '(11) 4004-6699', 'contato@engel.com.br', 'www.engel.com.br', 3),
('Husky Injection Molding Systems', '34.567.890/0001-77', '(11) 4005-7788', 'brasil@husky.com', 'www.husky.com', 3),
('Milacron Tecnologia em Plásticos', '45.678.901/0001-66', '(11) 4006-8877', 'vendas@milacron.com.br', 'www.milacron.com.br', 3),
('Wittmann Battenfeld Brasil', '56.789.012/0001-55', '(11) 4007-9966', 'info@wittmann.com.br', 'www.wittmann-group.com', 3);
INSERT INTO EnderecoFornecedor (ID_Fornecedor, rua, numero, bairro, cidade, estado, cep) VALUES
(1, 'Rua Industrial', '100', 'Distrito Industrial', 'São Bernardo do Campo', 'SP', '09850-000'),
(2, 'Avenida das Nações Unidas', '200', 'Brooklin', 'São Paulo', 'SP', '04578-000'),
(3, 'Rodovia Presidente Dutra', '300', 'Vila Maria', 'São Paulo', 'SP', '02116-000'),
(4, 'Rua da Tecnologia', '400', 'Polo Tecnológico', 'Campinas', 'SP', '13098-000'),
(5, 'Alameda Araguaia', '500', 'Alphaville', 'Barueri', 'SP', '06455-000');
INSERT INTO Injetora (marca, modelo, tipo_de_controle, capacidade_de_injecao, forca_de_fechamento, preco_medio_BRL, quantidade, observacao, ID_Fornecedor) VALUES
('Arburg', 'Allrounder 470 E Golden Edition', 'Elétrica', 200, 500, 900000.00, 3, 'Máquina premium com controle SELOGICA', 1),
('Engel', 'Victory 200/50 Tech', 'Elétrica', 180, 450, 875000.00, 2, 'Tecnologia CC300 com baixo consumo', 2),
('Husky', 'HyPET 300/120', 'Híbrida', 300, 800, 1400000.00, 1, 'Especializada para embalagens PET', 3),
('Milacron', 'Elektron EVO 150', 'Elétrica', 150, 350, 675000.00, 4, 'Versão EVO com melhorias técnicas', 4),
('Wittmann', 'EcoPower 250/80', 'Elétrica', 250, 600, 1050000.00, 2, 'Sistema de energia recuperativa', 5),
('Arburg', 'Allrounder 370 S', 'Hidráulica', 150, 400, 600000.00, 5, 'Modelo básico para produção contínua', 1),
('Engel', 'E-motion 170/60 TL', 'Elétrica', 170, 600, 800000.00, 3, 'Tecnologia de moldagem por injeção de 2 componentes', 2);
INSERT INTO Cliente (nome, CNPJ, telefone, email, cadastrado_por) VALUES
('Plásticos ABC Indústria e Comércio Ltda', '01.234.567/0001-11', '(11) 4002-8922', 'compras@plasticosabc.com.br', 2),
('Injetados Total S.A.', '02.345.678/0001-22', '(11) 4003-9822', 'vendas@injetadostotal.com.br', 2),
('Moldes & Componentes Plásticos Ltda', '03.456.789/0001-33', '(11) 4004-8922', 'contato@moldescomponentes.com.br', 2),
('Embalagens Plásticas Rio Ltda', '04.567.890/0001-44', '(21) 4005-8922', 'compras@embalagensrio.com.br', 2),
('Tecnoplást Indústria de Transformação', '05.678.901/0001-55', '(11) 4006-8922', 'tecnoplast@tecnoplast.ind.br', 2);
INSERT INTO EnderecoCliente (ID_Cliente, rua, numero, bairro, cidade, estado, cep) VALUES
(1, 'Rua dos Plásticos', '100', 'Distrito Industrial', 'São Paulo', 'SP', '03301-000'),
(2, 'Avenida da Injeção', '200', 'Centro Industrial', 'São Paulo', 'SP', '04301-000'),
(3, 'Rua dos Moldes', '300', 'Polo Tecnológico', 'São Paulo', 'SP', '05301-000'),
(4, 'Alameda das Embalagens', '400', 'Industrial', 'Rio de Janeiro', 'RJ', '20001-000'),
(5, 'Rua Tecnológica', '500', 'Distrito Industrial', 'São Paulo', 'SP', '06301-000');
INSERT INTO Compra (ID_Fornecedor, ID_Funcionario, data_compra, data_entrega_prevista, data_entrega_real, status_compra, forma_pagamento, valor_total_BRL, numero_nota_fiscal, observacoes) VALUES
(1, 3, '2023-01-15', '2023-02-20', '2023-02-18', 'concluido', 'Boleto 30 dias', 360000.00, 'NF123456', 'Compra de 2 máquinas Arburg Allrounder 470'),
(2, 3, '2023-02-10', '2023-03-15', '2023-03-12', 'concluido', 'Cartão de Crédito', 350000.00, 'NF234567', 'Compra de 2 máquinas Engel Victory'),
(3, 3, '2023-03-05', '2023-04-10', NULL, 'processamento', 'Transferência Bancária', 280000.00, NULL, 'Máquina Husky em processo de importação'),
(4, 3, '2023-04-20', '2023-05-25', '2023-05-22', 'concluido', 'Financiamento', 540000.00, 'NF345678', 'Compra de 4 máquinas Milacron Elektron'),
(5, 3, '2023-05-12', '2023-06-17', NULL, 'pendente', 'Boleto 60 dias', 420000.00, NULL, 'Aguardando aprovação financeira');
INSERT INTO Venda (ID_Cliente, ID_Funcionario, data_venda, forma_pagamento, valor_total_BRL, observacoes, status_aprovacao, aprovado_por, data_aprovacao) VALUES
(1, 2, '2023-02-01', 'Financiamento', 900000.00, 'Venda de máquina Arburg Allrounder 470', 'Em análise', 1, '2023-02-01 10:30:00', 'Cliente com bom histórico de pagamentos'),
(2, 2, '2023-03-15', 'Boleto 30 dias', 875000.00, 'Venda de máquina Engel Victory', 'Em análise', 1, '2023-03-15 14:15:00', 'Pagamento à vista com desconto'),
(3, 2, '2023-04-10', 'Cartão de Crédito', 1400000.00, 'Venda de máquina Husky HyPET', 'Em análise', NULL, NULL, NULL),
(4, 2, '2023-05-20', 'Transferência Bancária', 675000.00, 'Venda de máquina Milacron Elektron', 'Em análise', 1, '2023-05-20 16:45:00', 'Cliente com restrição cadastral'),
(5, 2, '2023-06-05', 'Boleto 60 dias', 1050000.00, 'Venda de máquina Wittmann EcoPower', 'Em análise', 1, '2023-06-05 11:20:00', 'Cliente com garantia adicional');
INSERT INTO ItemVenda (ID_Venda, ID_Injetora, quantidade, preco_unitario_BRL) VALUES
(1, 1, 1, 900000.00),
(2, 2, 1, 875000.00),
(3, 3, 1, 1400000.00),
(4, 4, 1, 675000.00),
(5, 5, 1, 1050000.00);
