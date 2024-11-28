<!DOCTYPE html>
<html>
    <head>
        <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
    </head>
<body>
    <?php
    echo "<table>";
    echo "<tr>
            <th> rojas </th>
            <th> amarillas </th>
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
       $variable1 = $_GET['estadio'];
       $stmt = $pdo->prepare("
            SELECT
                (SELECT COUNT(*) 
                FROM fuchibol.encuentros en, fuchibol.tarjetas_rojas tr
                WHERE en.game_id = tr.game_id
                AND LOWER(venue) LIKE LOWER('%' || :valor1 || '%')) AS rojas,
                (SELECT COUNT(*) 
                FROM fuchibol.encuentros en, fuchibol.tarjetas_amarillas ta
                WHERE en.game_id = ta.game_id
                AND LOWER(venue) LIKE LOWER('%' || :valor1 || '%')) AS amarillas
           ");
       $stmt->execute(['valor1' => $variable1]);

       $result = $stmt->fetch(PDO::FETCH_ASSOC);

       echo "<tr>";
       echo "<td>" . $result['rojas'] . "</td>";
       echo "<td>" . $result['amarillas'] . "</td>";
       echo "</tr>";

    }
    catch(PDOException $e){
        echo $e->getMessage();
    }
    echo "</table>";
    ?>

</body>
</html>
