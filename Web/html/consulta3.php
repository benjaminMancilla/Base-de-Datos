<!DOCTYPE html>
<html>
    <head>
        <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
    </head>
<body>
    <?php
        echo "<table>";
        echo "<tr>
                <th> Anho </th>
                <th> Equipo </th>
                <th> Porcentaje de victorias </th>
		<th> Publico siendo local </th>
		<th> Publico siendo visita </th>
		<th> Publico total </th>
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
           $variable1=$_GET['equipo'];
           $stmt = $pdo->prepare('
				SELECT s.year, s.team, 
					ROUND((s.won / s.games_played::numeric) * 100, 2) AS porcentaje_victorias, 
					ah.att_home, aa.att_away, (ah.att_home+aa.att_away) AS att_tot
				FROM fuchibol.stats s, fuchibol.att_home ah, fuchibol.att_away aa
				WHERE s.team = :valor1 
				AND ah.home_team = s.team 
				AND ah.year = s.year
				AND aa.away_team = s.team
				AND aa.year = s.year
				ORDER BY porcentaje_victorias DESC
                                ');
           $stmt->execute(['valor1' => $variable1]);
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
