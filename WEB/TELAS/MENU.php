<?php   
$currentPage = basename($_SERVER['PHP_SELF']);

// Definir permissões baseadas no perfil do funcionário
$permissoes = [];

if (isset($_SESSION['permissao'])) {
    $permissao = $_SESSION['permissao'];
    
    // Administrador - Acesso completo
    if ($permissao == 'admin') {
        $permissoes = [
            'TELA_LOJA.php' => true,
            'TELA_GERENCIAR_INJETORAS.php' => true,
            'TELA_GERENCIAR_FORNECEDORES.php' => true,
            'TELA_GERENCIAR_FUNCIONARIOS.php' => true,
            'TELA_GERENCIAR_CLIENTES.php' => true,
            'TELA_RELATORIOS.php' => true,
            'TELA_VENDAS.php' => true
        ];
    }
    // Gestor - Acesso a gestão e vendas
    elseif ($permissao == 'gestor') {
        $permissoes = [
            'TELA_LOJA.php' => true,
            'TELA_GERENCIAR_INJETORAS.php' => true,
            'TELA_GERENCIAR_CLIENTES.php' => true,
            'TELA_RELATORIOS.php' => true,
            'TELA_VENDAS.php' => true
        ];
    }
    // Usuário - Acesso limitado
    elseif ($permissao == 'usuario') {
        $permissoes = [
            'TELA_LOJA.php' => true,
            'TELA_VENDAS.php' => true
        ];
    }
}

// Função para verificar se o usuário tem acesso à página
function temAcesso($pagina) {
    global $permissoes;
    return isset($permissoes[$pagina]) && $permissoes[$pagina];
}

// Nome do perfil para exibição
$nomes_perfis = [
    'admin' => 'Administrador',
    'gestor' => 'Gestor', 
    'usuario' => 'Usuário'
];

$nome_perfil = isset($_SESSION['permissao']) ? $nomes_perfis[$_SESSION['permissao']] : 'Visitante';
?>
<!DOCTYPE html>
<html lang="pt-br">
<head> 
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FORNEINJET</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="../ESTILOS/ESTILO_GERAL.css">
    <link rel="stylesheet" href="../ESTILOS/ESTILO_MENU.css">
</head>
<body>

<?php if (isset($_SESSION['usuario'])): ?>
<div class="user-info">
    <?= htmlspecialchars($_SESSION['usuario']) ?> - <?= $nome_perfil ?>
</div>
<?php endif; ?>

<nav id="dock"> 
    <div id="dock_content">
        <ul id="dock_items">
            <!-- Loja - Todos os usuários -->
            <li class="dock-item <?= temAcesso('TELA_LOJA.php') ? '' : 'disabled' ?> <?= ($currentPage == 'TELA_LOJA.php') ? 'active' : '' ?>">
                <a href="<?= temAcesso('TELA_LOJA.php') ? 'TELA_LOJA.php' : '#' ?>">
                    <i class="fa-solid fa-house"></i>
                    <span class="tooltip"><?= temAcesso('TELA_LOJA.php') ? 'Início' : 'Acesso negado' ?></span>
                </a>
            </li>

            <!-- Gerenciar Injetoras - Admin e Gestor -->
            <li class="dock-item <?= temAcesso('TELA_GERENCIAR_INJETORAS.php') ? '' : 'disabled' ?> <?= ($currentPage == 'TELA_GERENCIAR_INJETORAS.php') ? 'active' : '' ?>">
                <a href="<?= temAcesso('TELA_GERENCIAR_INJETORAS.php') ? 'TELA_GERENCIAR_INJETORAS.php' : '#' ?>">
                    <i class="fa-solid fa-industry"></i>
                    <span class="tooltip"><?= temAcesso('TELA_GERENCIAR_INJETORAS.php') ? 'Injetoras' : 'Acesso negado' ?></span>
                </a>
            </li>

            <!-- Gerenciar Fornecedores - Apenas Admin -->
            <li class="dock-item <?= temAcesso('TELA_GERENCIAR_FORNECEDORES.php') ? '' : 'disabled' ?> <?= ($currentPage == 'TELA_GERENCIAR_FORNECEDORES.php') ? 'active' : '' ?>">
                <a href="<?= temAcesso('TELA_GERENCIAR_FORNECEDORES.php') ? 'TELA_GERENCIAR_FORNECEDORES.php' : '#' ?>">
                    <i class="fa-solid fa-truck"></i>
                    <span class="tooltip"><?= temAcesso('TELA_GERENCIAR_FORNECEDORES.php') ? 'Fornecedores' : 'Acesso negado' ?></span>
                </a>
            </li>
            
            <!-- Gerenciar Funcionários - Apenas Admin -->
            <li class="dock-item <?= temAcesso('TELA_GERENCIAR_FUNCIONARIOS.php') ? '' : 'disabled' ?> <?= ($currentPage == 'TELA_GERENCIAR_FUNCIONARIOS.php') ? 'active' : '' ?>">
                <a href="<?= temAcesso('TELA_GERENCIAR_FUNCIONARIOS.php') ? 'TELA_GERENCIAR_FUNCIONARIOS.php' : '#' ?>">
                    <i class="fa-solid fa-users"></i>
                    <span class="tooltip"><?= temAcesso('TELA_GERENCIAR_FUNCIONARIOS.php') ? 'Funcionários' : 'Acesso negado' ?></span>
                </a>
            </li>

            <!-- Gerenciar Clientes - Admin e Gestor -->
            <li class="dock-item <?= temAcesso('TELA_GERENCIAR_CLIENTES.php') ? '' : 'disabled' ?> <?= ($currentPage == 'TELA_GERENCIAR_CLIENTES.php') ? 'active' : '' ?>">
                <a href="<?= temAcesso('TELA_GERENCIAR_CLIENTES.php') ? 'TELA_GERENCIAR_CLIENTES.php' : '#' ?>">
                    <i class="fa-solid fa-address-book"></i>
                    <span class="tooltip"><?= temAcesso('TELA_GERENCIAR_CLIENTES.php') ? 'Clientes' : 'Acesso negado' ?></span>
                </a>
            </li>

            <!-- Vendas - Todos os usuários logados -->
            <li class="dock-item <?= temAcesso('TELA_VENDAS.php') ? '' : 'disabled' ?> <?= ($currentPage == 'TELA_VENDAS.php') ? 'active' : '' ?>">
                <a href="<?= temAcesso('TELA_VENDAS.php') ? 'TELA_VENDAS.php' : '#' ?>">
                    <i class="fa-solid fa-cash-register"></i>
                    <span class="tooltip"><?= temAcesso('TELA_VENDAS.php') ? 'Vendas' : 'Acesso negado' ?></span>
                </a>
            </li>

            <!-- Relatórios - Admin e Gestor -->
            <li class="dock-item <?= temAcesso('TELA_RELATORIOS.php') ? '' : 'disabled' ?> <?= ($currentPage == 'TELA_RELATORIOS.php') ? 'active' : '' ?>">
                <a href="<?= temAcesso('TELA_RELATORIOS.php') ? 'TELA_RELATORIOS.php' : '#' ?>">
                    <i class="fa-solid fa-chart-bar"></i>
                    <span class="tooltip"><?= temAcesso('TELA_RELATORIOS.php') ? 'Relatórios' : 'Acesso negado' ?></span>
                </a>
            </li>

            <!-- Logout - Disponível para todos os perfis logados -->
            <li class="dock-item <?= ($currentPage == '../logout.php') ? 'active' : '' ?>">
                <a href="../logout.php">
                    <i class="fa-solid fa-right-from-bracket"></i>
                    <span class="tooltip">Sair</span>
                </a>
            </li>
        </ul>
    </div>
</nav>

<script src="../CODIGOS/script.js"></script>
</body>
</html>