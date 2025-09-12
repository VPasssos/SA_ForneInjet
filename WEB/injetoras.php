<?php include "includes/config.php"; ?>
<?php include "includes/header.php"; ?>
<div class="container"><h3>Gerenciar Injetoras</h3>
<form method="POST">
 <input type="text" name="marca" placeholder="Marca" required>
 <input type="text" name="modelo" placeholder="Modelo">
 <input type="text" name="tipo" placeholder="Tipo de Controle">
 <input type="text" name="capacidade" placeholder="Capacidade">
 <input type="text" name="forca" placeholder="Força">
 <input type="number" step="0.01" name="preco" placeholder="Preço Médio">
 <input type="number" name="quantidade" placeholder="Quantidade">
 <button type="submit" name="add">Adicionar</button>
</form>
<table><tr><th>ID</th><th>Marca</th><th>Modelo</th><th>Tipo</th><th>Capacidade</th><th>Força</th><th>Preço</th><th>Qtd</th><th>Ações</th></tr>
<?php
if(isset($_POST["add"])){
 $stmt=$conn->prepare("INSERT INTO injetora (Marca,Modelo,Tipo,Capacidade,Forca,Preco,Quantidade) VALUES (?,?,?,?,?,?,?)");
 $stmt->bind_param("ssssidi",$_POST["marca"],$_POST["modelo"],$_POST["tipo"],$_POST["capacidade"],$_POST["forca"],$_POST["preco"],$_POST["quantidade"]);
 $stmt->execute();
}
if(isset($_GET["del"])){ $id=intval($_GET["del"]); $conn->query("DELETE FROM injetora WHERE id_injetora=$id"); }
$result=$conn->query("SELECT * FROM injetora");
while($row=$result->fetch_assoc()){
 echo "<tr><td>{$row['id_injetora']}</td><td>{$row['Marca']}</td><td>{$row['Modelo']}</td><td>{$row['Tipo']}</td><td>{$row['Capacidade']}</td><td>{$row['Forca']}</td><td>{$row['Preco']}</td><td>{$row['Quantidade']}</td>
 <td><a href='?del={$row['id_injetora']}'>Excluir</a></td></tr>";
} ?>
</table></div><?php include "includes/footer.php"; ?>