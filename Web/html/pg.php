<?php

try {
   $pdo = new PDO('pgsql:host=localhost;port=5432;dbname=cc3201;user=webuser;password=vegeta777');
   echo "PDO connection object created";
   $stmt = $pdo->query('SELECT * FROM fuchibol.team LIMIT 10');
   while ($row = $stmt->fetch())
   {
     print_r($row);
   }
}
catch(PDOException $e)
{
      echo $e->getMessage();
}

?>
