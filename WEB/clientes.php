<?php include "includes/config.php"; ?>
<?php include "includes/header.php"; ?>
<div class="container"><h3>Gerenciar Clientes</h3>
<form method="POST">
 <input type="text" name="nome" placeholder="Nome" required>
 <input type="text" name="cnpj" placeholder="CNPJ">
 <input type="text" name="telefone" placeholder="Telefone">
 <input type="email" name="email" placeholder="Email">
 <button type="submit" name="add">Adicionar</button>
</form>
<table><tr><th>ID</th><th>Nome</th><th>CNPJ</th><th>Telefone</th><th>Email</th><th>Ações</th></tr>
<?php
if(isset($_POST["add"])){
 $stmt=$conn->prepare("INSERT INTO cliente (Nome,CNPJ,Telefone,Email) VALUES (?,?,?,?)");
 $stmt->bind_param("ssss",$_POST["nome"],$_POST["cnpj"],$_POST["telefone"],$_POST["email"]);
 $stmt->execute();
}
if(isset($_GET["del"])){ $id=intval($_GET["del"]); $conn->query("DELETE FROM cliente WHERE id_cliente=$id"); }
$result=$conn->query("SELECT * FROM cliente");
while($row=$result->fetch_assoc()){
 echo "<tr><td>{$row['id_cliente']}</td><td>{$row['Nome']}</td><td>{$row['CNPJ']}</td><td>{$row['Telefone']}</td><td>{$row['Email']}</td>
 <td><a href='?del={$row['id_cliente']}'>Excluir</a></td></tr>";
} ?>
</table></div><?php include "includes/footer.php"; ?>