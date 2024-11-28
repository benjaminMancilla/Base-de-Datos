<!DOCTYPE html>
<html>
    <head>
        <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
    </head>
<body>
    <?php
        echo "<table>";
        echo "<tr>
                <th> equipo </th>
                <th> victorias </th>
                <th> derrotas </th>
                <th> empates </th>
              </tr>";

        class TableRows extends RecursiveIteratorIterator {
            function __construct($it) {
                parent::__construct($it, self::LEAVES_ONLY);
            }
            function current() {
                return "<td>" . parent::current(). "</td>";
            }
            function beginChildren() {
                echo "<tr>";
            }
            function endChildren() {
                echo "</tr>" . "\n";
            }
        }

        try {
           $pdo = new PDO('pgsql:
                           host=localhost;
                           port=5432;
                           dbname=cc3201;
                           user=webuser;
                           password=vegeta777');
           $variable1=$_GET['ano1'];
           $variable2=$_GET['ano2'];
           $stmt = $pdo->prepare('
               SELECT team, SUM(won) AS victorias, SUM(lost) AS derrotas, SUM(drew) AS empates
               FROM fuchibol.Stats s
               WHERE year BETWEEN :valor1 AND :valor2
               GROUP BY team
               ORDER BY team');
           $stmt->execute(['valor1' => $variable1, 'valor2' => $variable2]);
           $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);

           foreach(new TableRows(new RecursiveArrayIterator($stmt->fetchAll())) as $k=>$v) {
               echo $v;
           }
        }
        catch(PDOException $e){
            echo $e->getMessage();
        }
        echo "</table>";
    ?>
</body>
</html>
