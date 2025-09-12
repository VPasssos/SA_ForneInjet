<?php include "includes/config.php"; ?>
<?php include "includes/header.php"; ?>
<div class="container"><h3>Gerenciar Fornecedores</h3>
<form method="POST">
 <input type="text" name="nome" placeholder="Nome" required>
 <input type="text" name="cnpj" placeholder="CNPJ">
 <input type="text" name="telefone" placeholder="Telefone">
 <input type="email" name="email" placeholder="Email">
 <input type="text" name="website" placeholder="Website">
 <button type="submit" name="add">Adicionar</button>
</form>
<table><tr><th>ID</th><th>Nome</th><th>CNPJ</th><th>Telefone</th><th>Email</th><th>Website</th><th>Ações</th></tr>
<?php
if(isset($_POST["add"])){
 $stmt=$conn->prepare("INSERT INTO fornecedor (Nome,CNPJ,Telefone,Email,Website) VALUES (?,?,?,?,?)");
 $stmt->bind_param("sssss",$_POST["nome"],$_POST["cnpj"],$_POST["telefone"],$_POST["email"],$_POST["website"]);
 $stmt->execute();
}
if(isset($_GET["del"])){ $id=intval($_GET["del"]); $conn->query("DELETE FROM fornecedor WHERE id_fornecedor=$id"); }
$result=$conn->query("SELECT * FROM fornecedor");
while($row=$result->fetch_assoc()){
 echo "<tr><td>{$row['id_fornecedor']}</td><td>{$row['Nome']}</td><td>{$row['CNPJ']}</td><td>{$row['Telefone']}</td><td>{$row['Email']}</td><td>{$row['Website']}</td>
 <td><a href='?del={$row['id_fornecedor']}'>Excluir</a></td></tr>";
} ?>
</table></div><?php include "includes/footer.php"; ?>