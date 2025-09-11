<?php
// CONFIG.php - conexão com banco ForneInjet usando PDO e utf8mb4

$host = "localhost";       // servidor do banco
$dbname = "sa_forneinjet";    // nome do banco
$user = "root";            // usuário do banco
$pass = "";                // senha do banco

try {
    // Conexão PDO com charset utf8mb4 para evitar problemas de acentuação
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $user, $pass, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, // erros lançam exceções
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, // fetch como array associativo
        PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8mb4" // garante encoding na conexão
    ]);
} catch (PDOException $e) {
    die("Erro de conexão com o banco de dados: " . $e->getMessage());
}

// Função de segurança para limpar entradas do usuário
function limparDados($dado) {
    return htmlspecialchars(trim($dado), ENT_QUOTES, 'UTF-8');
}
?>
