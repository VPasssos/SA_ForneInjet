<?php include "includes/config.php"; ?>
<?php include "includes/header.php"; ?>
<div class="container"><h3>Gerenciar Vendas</h3>
<form method="POST">
 <input type="number" name="id_cliente" placeholder="ID Cliente" required>
 <input type="number" name="id_injetora" placeholder="ID Injetora" required>
 <input type="number" name="quantidade" placeholder="Quantidade" required>
 <input type="number" step="0.01" name="preco" placeholder="Preço Unitário">
 <input type="text" name="status" placeholder="Status">
 <button type="submit" name="add">Adicionar</button>
</form>
<table><tr><th>ID</th><th>Cliente</th><th>Injetora</th><th>Qtd</th><th>Preço</th><th>Status</th><th>Ações</th></tr>
<?php
if(isset($_POST["add"])){
 $stmt=$conn->prepare("INSERT INTO venda (id_cliente,id_injetora,Quantidade,PrecoUnitario,Status) VALUES (?,?,?,?,?)");
 $stmt->bind_param("iiids",$_POST["id_cliente"],$_POST["id_injetora"],$_POST["quantidade"],$_POST["preco"],$_POST["status"]);
 $stmt->execute();
}
if(isset($_GET["del"])){ $id=intval($_GET["del"]); $conn->query("DELETE FROM venda WHERE id_venda=$id"); }
$result=$conn->query("SELECT * FROM venda");
while($row=$result->fetch_assoc()){
 echo "<tr><td>{$row['id_venda']}</td><td>{$row['id_cliente']}</td><td>{$row['id_injetora']}</td><td>{$row['Quantidade']}</td><td>{$row['PrecoUnitario']}</td><td>{$row['Status']}</td>
 <td><a href='?del={$row['id_venda']}'>Excluir</a></td></tr>";
} ?>
</table></div><?php include "includes/footer.php"; ?>