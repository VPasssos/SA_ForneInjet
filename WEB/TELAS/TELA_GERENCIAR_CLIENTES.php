<?php
session_start();
include('../conexao.php');

// VERIFICA PERMISSÃO
if ($_SESSION['permissao'] !== 'admin' && $_SESSION['permissao'] !== 'gestor') {
    $_SESSION['mensagem_erro'] = 'Acesso Negado';
    header('Location: TELA_INICIAL.php');
    exit();
}

// Função para buscar clientes
function buscarClientes($pdo, $termo = null) {
    $sql = "SELECT c.*, f.nome AS cadastrado_por_nome 
            FROM Cliente c 
            LEFT JOIN Funcionario f ON c.cadastrado_por = f.ID_Funcionario 
            WHERE 1=1";

    if ($termo) {
        $sql .= " AND (c.nome LIKE :termo OR c.email LIKE :termo OR c.CNPJ LIKE :termo)";
    }

    $sql .= " ORDER BY c.nome ASC";

    $stmt = $pdo->prepare($sql);
    if ($termo) {
        $stmt->bindValue(':termo', '%' . $termo . '%');
    }
    $stmt->execute();
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

// EXCLUSÃO
if (isset($_GET['excluir'])) {
    $ID_Cliente = $_GET['excluir'];

    try {
        $pdo->beginTransaction();

        $stmt_end = $pdo->prepare("DELETE FROM EnderecoCliente WHERE ID_Cliente = :ID_Cliente");
        $stmt_end->bindParam(':ID_Cliente', $ID_Cliente);
        $stmt_end->execute();

        $stmt = $pdo->prepare("DELETE FROM Cliente WHERE ID_Cliente = :ID_Cliente");
        $stmt->bindParam(':ID_Cliente', $ID_Cliente);
        $stmt->execute();

        $pdo->commit();
        $_SESSION['mensagem_sucesso'] = "Cliente excluído com sucesso!";
    } catch (Exception $e) {
        $pdo->rollBack();
        $_SESSION['mensagem_erro'] = "Erro ao excluir cliente.";
    }
    header('Location: GERENCIAR_CLIENTES.php');
    exit();
}

// ADICIONAR CLIENTE
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['adicionar_cliente'])) {
    $stmt = $pdo->prepare("INSERT INTO Cliente (nome, CNPJ, telefone, email, cadastrado_por) 
                           VALUES (:nome, :CNPJ, :telefone, :email, :cadastrado_por)");
    try {
        $stmt->execute([
            ':nome' => $_POST['nome'],
            ':CNPJ' => $_POST['CNPJ'],
            ':telefone' => $_POST['telefone'],
            ':email' => $_POST['email'],
            ':cadastrado_por' => $_SESSION['ID_Funcionario']
        ]);
        $_SESSION['mensagem_sucesso'] = "Cliente adicionado com sucesso!";
    } catch (Exception $e) {
        $_SESSION['mensagem_erro'] = "Erro ao adicionar cliente.";
    }
    header('Location: GERENCIAR_CLIENTES.php');
    exit();
}

// ALTERAR CLIENTE
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['alterar_cliente'])) {
    $stmt = $pdo->prepare("UPDATE Cliente 
                           SET nome = :nome, CNPJ = :CNPJ, telefone = :telefone, email = :email 
                           WHERE ID_Cliente = :ID_Cliente");
    try {
        $stmt->execute([
            ':nome' => $_POST['nome'],
            ':CNPJ' => $_POST['CNPJ'],
            ':telefone' => $_POST['telefone'],
            ':email' => $_POST['email'],
            ':ID_Cliente' => $_POST['ID_Cliente']
        ]);
        $_SESSION['mensagem_sucesso'] = "Cliente atualizado com sucesso!";
    } catch (Exception $e) {
        $_SESSION['mensagem_erro'] = "Erro ao atualizar cliente.";
    }
    header('Location: GERENCIAR_CLIENTES.php');
    exit();
}

$clientes = isset($_POST['busca']) ? buscarClientes($pdo, $_POST['busca']) : buscarClientes($pdo);
?>

<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Gerenciar Clientes</title>
    <link rel="stylesheet" href="../ESTILOS/ESTILO_GERAL.css">
    <link rel="stylesheet" href="../ESTILOS/ESTILO_GERENCIAR_CLIENTES.css">
    <style>
        /* Estilo extra para modal responsivo e centralizado */
        .modal {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 90%;
            max-width: 500px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 0 10px #00000050;
            padding: 20px;
            z-index: 999;
        }
        .overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 998;
        }
        .modal input {
            width: 100%;
            padding: 8px;
            margin-bottom: 10px;
        }
        .modal button {
            margin-top: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 10px;
            border-bottom: 1px solid #ccc;
            text-align: left;
        }
        .mensagem {
            padding: 10px;
            margin-bottom: 15px;
            border-radius: 5px;
        }
        .sucesso { background: #d4edda; color: #155724; }
        .erro { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <?php include("MENU.php"); ?>

    <main>
        <h1>Gerenciar Clientes</h1>

        <?php if (isset($_SESSION['mensagem_sucesso'])): ?>
            <div class="mensagem sucesso"><?= $_SESSION['mensagem_sucesso']; unset($_SESSION['mensagem_sucesso']); ?></div>
        <?php endif; ?>
        <?php if (isset($_SESSION['mensagem_erro'])): ?>
            <div class="mensagem erro"><?= $_SESSION['mensagem_erro']; unset($_SESSION['mensagem_erro']); ?></div>
        <?php endif; ?>

        <form method="POST">
            <input type="text" name="busca" placeholder="Buscar cliente...">
            <button type="submit">Buscar</button>
        </form>

        <button onclick="abrirModalNovo()">+ Adicionar Cliente</button>

        <table>
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>CNPJ</th>
                    <th>Email</th>
                    <th>Telefone</th>
                    <th>Cadastrado por</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($clientes as $cliente): ?>
                    <tr>
                        <td><?= $cliente['nome'] ?></td>
                        <td><?= $cliente['CNPJ'] ?></td>
                        <td><?= $cliente['email'] ?></td>
                        <td><?= $cliente['telefone'] ?></td>
                        <td><?= $cliente['cadastrado_por_nome'] ?></td>
                        <td>
                            <button onclick='abrirModalEditar(<?= json_encode($cliente) ?>)'>Editar</button>
                            <a href="?excluir=<?= $cliente['ID_Cliente'] ?>" onclick="return confirm('Deseja excluir este cliente?')">Excluir</a>
                        </td>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>

        <!-- Modal -->
        <div class="overlay" id="overlay" style="display:none;" onclick="fecharModal()"></div>
        <div class="modal" id="modal_form" style="display:none;">
            <h2 id="titulo_modal">Novo Cliente</h2>
            <form method="POST" id="form_cliente">
                <input type="hidden" name="ID_Cliente" id="ID_Cliente">
                <input type="text" name="nome" id="nome" placeholder="Nome" required>
                <input type="text" name="CNPJ" id="CNPJ" placeholder="CNPJ" required>
                <input type="text" name="telefone" id="telefone" placeholder="Telefone">
                <input type="email" name="email" id="email" placeholder="Email">
                <button type="submit" name="adicionar_cliente" id="btn_add">Salvar</button>
                <button type="submit" name="alterar_cliente" id="btn_edit" style="display:none;">Salvar Alterações</button>
                <button type="button" onclick="fecharModal()">Cancelar</button>
            </form>
        </div>
    </main>

    <script>
        function abrirModalNovo() {
            document.getElementById("form_cliente").reset();
            document.getElementById("titulo_modal").textContent = "Adicionar Cliente";
            document.getElementById("btn_add").style.display = "inline-block";
            document.getElementById("btn_edit").style.display = "none";
            document.getElementById("modal_form").style.display = "block";
            document.getElementById("overlay").style.display = "block";
        }

        function abrirModalEditar(cliente) {
            document.getElementById("ID_Cliente").value = cliente.ID_Cliente;
            document.getElementById("nome").value = cliente.nome;
            document.getElementById("CNPJ").value = cliente.CNPJ;
            document.getElementById("telefone").value = cliente.telefone;
            document.getElementById("email").value = cliente.email;
            document.getElementById("titulo_modal").textContent = "Editar Cliente";
            document.getElementById("btn_add").style.display = "none";
            document.getElementById("btn_edit").style.display = "inline-block";
            document.getElementById("modal_form").style.display = "block";
            document.getElementById("overlay").style.display = "block";
        }

        function fecharModal() {
            document.getElementById("modal_form").style.display = "none";
            document.getElementById("overlay").style.display = "none";
        }
    </script>
</body>
</html>
