<?php
session_start();

// Simulação de usuário
$usuario_simulado = "admin";
$senha_simulada_hash = password_hash("123456", PASSWORD_DEFAULT); // Senha simulada: 123456

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $usuario = $_POST['usuario'];
    $senha = $_POST['senha'];

    // Simula uma consulta ao banco
    if ($usuario === $usuario_simulado && password_verify($senha, $senha_simulada_hash)) {
        $_SESSION['ID_Funcionario'] = 1; // ID fictício
        $_SESSION['usuario'] = $usuario_simulado;
        $_SESSION['permissao'] = 'admin'; // Permissão fictícia

        header("Location: TELAS/TELA_GERENCIAR_FUNCIONARIOS.php");
        exit();
    } else {
        echo "<script>alert('Usuário ou senha incorretos!');</script>";
    }
}
?>

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login (Simulação)</title>
    <link rel="stylesheet" type="text/css" href="ESTILOS/ESTILO_GERAL.css" media="all"> 
    <link rel="stylesheet" type="text/css" href="ESTILOS/ESTILO_LOGIN.css" media="all">
</head>
<body>
    <div class="main_login">
        <div class="card_login">
            <h1>Login</h1>
            <form action="login.php" method="POST">
                <div class="textfield">
                    <label for="usuario">Usuário</label>
                    <input type="text" id="usuario" name="usuario" required>
                </div>
                <div class="textfield">
                    <label for="senha">Senha</label>
                    <input type="password" id="senha" name="senha" required>
                </div>
                <button type="submit" class="btn_login">Entrar</button>
            </form>
            <p><a href="recuperar_senha.php">Esqueci minha senha</a></p>
        </div>
    </div>
</body>
</html>
