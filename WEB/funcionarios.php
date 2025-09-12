<?php include "includes/config.php"; ?>
<?php include "includes/header.php"; ?>
<div class="container"><h3>Gerenciar Funcionários</h3>
<form method="POST">
 <input type="text" name="nome" placeholder="Nome" required>
 <input type="text" name="cargo" placeholder="Cargo">
 <input type="text" name="telefone" placeholder="Telefone">
 <input type="email" name="email" placeholder="Email">
 <input type="text" name="usuario" placeholder="Usuário">
 <input type="password" name="senha" placeholder="Senha">
 <button type="submit" name="add">Adicionar</button>
</form>
<table><tr><th>ID</th><th>Nome</th><th>Cargo</th><th>Telefone</th><th>Email</th><th>Usuário</th><th>Ações</th></tr>
<?php
if(isset($_POST["add"])){
 $stmt=$conn->prepare("INSERT INTO funcionario (Nome,Cargo,Telefone,Email,Usuario,Senha) VALUES (?,?,?,?,?,?)");
 $stmt->bind_param("ssssss",$_POST["nome"],$_POST["cargo"],$_POST["telefone"],$_POST["email"],$_POST["usuario"],$_POST["senha"]);
 $stmt->execute();
}
if(isset($_GET["del"])){ $id=intval($_GET["del"]); $conn->query("DELETE FROM funcionario WHERE id_funcionario=$id"); }
$result=$conn->query("SELECT * FROM funcionario");
while($row=$result->fetch_assoc()){
 echo "<tr><td>{$row['id_funcionario']}</td><td>{$row['Nome']}</td><td>{$row['Cargo']}</td><td>{$row['Telefone']}</td><td>{$row['Email']}</td><td>{$row['Usuario']}</td>
 <td><a href='?del={$row['id_funcionario']}'>Excluir</a></td></tr>";
} ?>
</table></div><?php include "includes/footer.php"; ?>