<?php
session_start();
include('../conexao.php');

// VERIFICA SE O USUARIO TEM PERMISSÃO (apenas admin)
if($_SESSION['permissao'] != 'admin'){
    $_SESSION['mensagem_erro'] = 'Acesso Negado';
    header('Location: TELA_INICIAL.php');
    exit();
}

// Função para buscar funcionários
function buscarFuncionarios($pdo, $termo = null) {
    $sql = "SELECT * FROM Funcionario WHERE 1=1";
    
    if ($termo) {
        $sql .= " AND (nome LIKE :termo OR email LIKE :termo OR usuario LIKE :termo)";
    }

    $sql .= " ORDER BY nome ASC";

    $stmt = $pdo->prepare($sql);

    if ($termo) {
        $stmt->bindValue(':termo', '%' . $termo . '%');
    }

    $stmt->execute();
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

// Função para excluir um funcionário
if (isset($_GET['excluir'])) {
    $ID_Funcionario = $_GET['excluir'];

    $sql = "DELETE FROM Funcionario WHERE ID_Funcionario = :ID_Funcionario";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':ID_Funcionario', $ID_Funcionario, PDO::PARAM_INT);
    
    if ($stmt->execute()) {
        $_SESSION['mensagem_sucesso'] = 'Funcionário excluído com sucesso!';
    } else {
        $_SESSION['mensagem_erro'] = 'Erro ao excluir funcionário!';
    }
    header('Location: TELA_GERENCIAR_FUNCIONARIOS.php');
    exit();
}

// Função para adicionar um novo funcionário
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['adicionar_funcionario'])) {
    $nome = $_POST['nome'];
    $cargo = $_POST['cargo'];
    $telefone = $_POST['telefone'];
    $email = $_POST['email'];
    $usuario = $_POST['usuario'];
    $senha = password_hash($_POST['senha'], PASSWORD_DEFAULT);
    $permissao = $_POST['permissao'];
    $situacao = $_POST['situacao'];
    $data_admissao = $_POST['data_admissao'];

    $sql = "INSERT INTO Funcionario (nome, cargo, telefone, email, usuario, senha, permissao, situacao, data_admissao) 
            VALUES (:nome, :cargo, :telefone, :email, :usuario, :senha, :permissao, :situacao, :data_admissao)";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':nome', $nome);
    $stmt->bindParam(':cargo', $cargo);
    $stmt->bindParam(':telefone', $telefone);
    $stmt->bindParam(':email', $email);
    $stmt->bindParam(':usuario', $usuario);
    $stmt->bindParam(':senha', $senha);
    $stmt->bindParam(':permissao', $permissao);
    $stmt->bindParam(':situacao', $situacao);
    $stmt->bindParam(':data_admissao', $data_admissao);
    
    if ($stmt->execute()) {
        $_SESSION['mensagem_sucesso'] = 'Funcionário adicionado com sucesso!';
    } else {
        $_SESSION['mensagem_erro'] = 'Erro ao adicionar funcionário!';
    }
    header('Location: TELA_GERENCIAR_FUNCIONARIOS.php');
    exit();
}

// Função para alterar um funcionário
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['alterar_funcionario'])) {
    $ID_Funcionario = $_POST['ID_Funcionario'];
    $nome = $_POST['nome'];
    $cargo = $_POST['cargo'];
    $telefone = $_POST['telefone'];
    $email = $_POST['email'];
    $usuario = $_POST['usuario'];
    $permissao = $_POST['permissao'];
    $situacao = $_POST['situacao'];
    $data_admissao = $_POST['data_admissao'];
    $nova_senha = !empty($_POST['nova_senha']) ? password_hash($_POST['nova_senha'], PASSWORD_DEFAULT) : null;

    if ($nova_senha) {
        $sql = "UPDATE Funcionario SET nome = :nome, cargo = :cargo, telefone = :telefone, 
                email = :email, usuario = :usuario, senha = :senha, permissao = :permissao, 
                situacao = :situacao, data_admissao = :data_admissao 
                WHERE ID_Funcionario = :ID_Funcionario";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':senha', $nova_senha);
    } else {
        $sql = "UPDATE Funcionario SET nome = :nome, cargo = :cargo, telefone = :telefone, 
                email = :email, usuario = :usuario, permissao = :permissao, 
                situacao = :situacao, data_admissao = :data_admissao 
                WHERE ID_Funcionario = :ID_Funcionario";
        $stmt = $pdo->prepare($sql);
    }
    
    $stmt->bindParam(':ID_Funcionario', $ID_Funcionario);
    $stmt->bindParam(':nome', $nome);
    $stmt->bindParam(':cargo', $cargo);
    $stmt->bindParam(':telefone', $telefone);
    $stmt->bindParam(':email', $email);
    $stmt->bindParam(':usuario', $usuario);
    $stmt->bindParam(':permissao', $permissao);
    $stmt->bindParam(':situacao', $situacao);
    $stmt->bindParam(':data_admissao', $data_admissao);
    
    if ($stmt->execute()) {
        $_SESSION['mensagem_sucesso'] = 'Funcionário alterado com sucesso!';
    } else {
        $_SESSION['mensagem_erro'] = 'Erro ao alterar funcionário!';
    }
    header('Location: TELA_GERENCIAR_FUNCIONARIOS.php');
    exit();
}

// Verifica se há um termo de busca
$funcionarios = isset($_POST['busca']) ? buscarFuncionarios($pdo, $_POST['busca']) : buscarFuncionarios($pdo);

// Buscar funcionário para edição se houver ID na URL
$funcionario_edicao = null;
if (isset($_GET['editar'])) {
    $ID_Funcionario = $_GET['editar'];
    $sql = "SELECT * FROM Funcionario WHERE ID_Funcionario = :ID_Funcionario";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':ID_Funcionario', $ID_Funcionario, PDO::PARAM_INT);
    $stmt->execute();
    $funcionario_edicao = $stmt->fetch(PDO::FETCH_ASSOC);
}
?>

<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GERENCIAR FUNCIONÁRIOS</title>
    <link rel="stylesheet" href="../ESTILOS/ESTILO_GERAL.css">
    <link rel="stylesheet" href="../ESTILOS/ESTILO_GERENCIAR_FUNCIONARIO.css">
    <script src="../JS/mascaras.js"></script>
</head>
<body>
    <?php include("MENU.php"); ?>

    <main>
        <h1>GERENCIAR FUNCIONÁRIOS</h1>
        
        <?php
        if (isset($_SESSION['mensagem_sucesso'])) {
            echo '<div class="mensagem sucesso">' . $_SESSION['mensagem_sucesso'] . '</div>';
            unset($_SESSION['mensagem_sucesso']);
        }
        if (isset($_SESSION['mensagem_erro'])) {
            echo '<div class="mensagem erro">' . $_SESSION['mensagem_erro'] . '</div>';
            unset($_SESSION['mensagem_erro']);
        }
        ?>

        <div class="ops_func">
            <button id="btnAdicionar" onclick="abrirModal('modalAdicionar')">Adicionar</button>
            <form action="TELA_GERENCIAR_FUNCIONARIOS.php" method="POST">
                <input type="text" name="busca" id="busca" placeholder="Pesquisar funcionário">
                <button type="submit">Pesquisar</button>
            </form>
        </div>

        <div class="tabela_func">
            <?php if (!empty($funcionarios)): ?>
                <table class="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nome</th>
                            <th>Cargo</th>
                            <th>Telefone</th>
                            <th>E-mail</th>
                            <th>Usuário</th>
                            <th>Permissão</th>
                            <th>Situação</th>
                            <th>Data Admissão</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($funcionarios as $funcionario): ?>
                            <tr>
                                <td><?= htmlspecialchars($funcionario['ID_Funcionario']) ?></td>
                                <td><?= htmlspecialchars($funcionario['nome']) ?></td>
                                <td><?= htmlspecialchars($funcionario['cargo']) ?></td>
                                <td><?= htmlspecialchars($funcionario['telefone']) ?></td>
                                <td><?= htmlspecialchars($funcionario['email']) ?></td>
                                <td><?= htmlspecialchars($funcionario['usuario']) ?></td>
                                <td><?= htmlspecialchars($funcionario['permissao']) ?></td>
                                <td><?= htmlspecialchars($funcionario['situacao']) ?></td>
                                <td><?= htmlspecialchars($funcionario['data_admissao']) ?></td>
                                <td>
                                    <a href="TELA_GERENCIAR_FUNCIONARIOS.php?editar=<?= htmlspecialchars($funcionario['ID_Funcionario']) ?>">Alterar</a>
                                    <a href="TELA_GERENCIAR_FUNCIONARIOS.php?excluir=<?= htmlspecialchars($funcionario['ID_Funcionario']) ?>" 
                                       class="excluir" 
                                       onclick="return confirm('Tem certeza que deseja excluir este funcionário?')">Excluir</a>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            <?php else: ?>
                <p>Nenhum funcionário encontrado</p>
            <?php endif; ?>
        </div>
    </main>

    <!-- Modal para Adicionar Funcionário -->
    <div id="modalAdicionar" class="modal">
        <div class="modal-content">
            <h2>Adicionar Funcionário</h2>
            <form method="POST" action="TELA_GERENCIAR_FUNCIONARIOS.php">
                <label for="nome">Nome:</label>
                <input type="text" name="nome" required>

                <label for="cargo">Cargo:</label>
                <input type="text" name="cargo" required>

                <label for="telefone">Telefone:</label>
                <input type="text" name="telefone" placeholder="(00) 00000-0000" required>

                <label for="email">E-mail:</label>
                <input type="email" name="email" required>

                <label for="usuario">Usuário:</label>
                <input type="text" name="usuario" required>

                <label for="senha">Senha:</label>
                <input type="password" name="senha" required>

                <label for="permissao">Permissão:</label>
                <select name="permissao" required>
                    <option value="usuario">Usuário</option>
                    <option value="gestor">Gestor</option>
                    <option value="admin">Administrador</option>
                </select>

                <label for="situacao">Situação:</label>
                <select name="situacao" required>
                    <option value="ativo">Ativo</option>
                    <option value="inativo">Inativo</option>
                </select>

                <label for="data_admissao">Data de Admissão:</label>
                <input type="date" name="data_admissao" required>

                <button type="submit" name="adicionar_funcionario" class="btn_acao">Adicionar</button>
                <button type="button" class="btn_acao btn_cancelar" onclick="fecharModal('modalAdicionar')">Cancelar</button>
            </form>
        </div>
    </div>

    <!-- Modal para Alterar Funcionário -->
    <?php if ($funcionario_edicao): ?>
    <div id="modalAlterar" class="modal" style="display: flex;">
        <div class="modal-content">
            <h2>Alterar Funcionário</h2>
            <form method="POST" action="TELA_GERENCIAR_FUNCIONARIOS.php">
                <input type="hidden" name="ID_Funcionario" value="<?= $funcionario_edicao['ID_Funcionario'] ?>">
                
                <label for="nome_editar">Nome:</label>
                <input type="text" name="nome" id="nome_editar" value="<?= htmlspecialchars($funcionario_edicao['nome']) ?>" required>

                <label for="cargo_editar">Cargo:</label>
                <input type="text" name="cargo" id="cargo_editar" value="<?= htmlspecialchars($funcionario_edicao['cargo']) ?>" required>

                <label for="telefone_editar">Telefone:</label>
                <input type="text" name="telefone" id="telefone_editar" value="<?= htmlspecialchars($funcionario_edicao['telefone']) ?>" required>

                <label for="email_editar">E-mail:</label>
                <input type="email" name="email" id="email_editar" value="<?= htmlspecialchars($funcionario_edicao['email']) ?>" required>

                <label for="usuario_editar">Usuário:</label>
                <input type="text" name="usuario" id="usuario_editar" value="<?= htmlspecialchars($funcionario_edicao['usuario']) ?>" required>

                <label for="permissao_editar">Permissão:</label>
                <select name="permissao" id="permissao_editar" required>
                    <option value="usuario" <?= $funcionario_edicao['permissao'] == 'usuario' ? 'selected' : '' ?>>Usuário</option>
                    <option value="gestor" <?= $funcionario_edicao['permissao'] == 'gestor' ? 'selected' : '' ?>>Gestor</option>
                    <option value="admin" <?= $funcionario_edicao['permissao'] == 'admin' ? 'selected' : '' ?>>Administrador</option>
                </select>

                <label for="situacao_editar">Situação:</label>
                <select name="situacao" id="situacao_editar" required>
                    <option value="ativo" <?= $funcionario_edicao['situacao'] == 'ativo' ? 'selected' : '' ?>>Ativo</option>
                    <option value="inativo" <?= $funcionario_edicao['situacao'] == 'inativo' ? 'selected' : '' ?>>Inativo</option>
                </select>

                <label for="data_admissao_editar">Data de Admissão:</label>
                <input type="date" name="data_admissao" id="data_admissao_editar" value="<?= htmlspecialchars($funcionario_edicao['data_admissao']) ?>" required>

                <label for="nova_senha">Nova Senha (deixe em branco para manter a atual):</label>
                <input type="password" name="nova_senha" id="nova_senha">

                <button type="submit" name="alterar_funcionario" class="btn_acao">Alterar</button>
                <button type="button" class="btn_acao btn_cancelar" onclick="fecharModal('modalAlterar')">Cancelar</button>
            </form>
        </div>
    </div>
    <?php endif; ?>

    <script>
        function abrirModal(id) {
            document.getElementById(id).style.display = 'flex';
        }

        function fecharModal(id) {
            document.getElementById(id).style.display = 'none';
            window.location.href = 'TELA_GERENCIAR_FUNCIONARIOS.php';
        }

        window.onclick = function(event) {
            if (event.target.classList.contains('modal')) {
                event.target.style.display = 'none';
                window.location.href = 'TELA_GERENCIAR_FUNCIONARIOS.php';
            }
        }

        <?php if ($funcionario_edicao): ?>
            document.addEventListener('DOMContentLoaded', function() {
                abrirModal('modalAlterar');
            });
        <?php endif; ?>
    </script>
</body>
</html>