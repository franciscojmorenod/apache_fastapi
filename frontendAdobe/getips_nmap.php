<?php
$json_data = file_get_contents("http://192.168.1.21:8000/getipsnmap");

$data = json_decode($json_data, true);

echo "<H1 style='text-align: center;'>" . "Currently Active IP addresses " . "</H1>";
echo "<H3 style='text-align: center;'>" . "Collected via nmap" . "</H1>";
echo "<table cellpadding='5'>";
echo "<style>";
echo "html, body { height: 100% }";
echo "html {display: table; margin: auto;}";
echo "body { display: table-cell; vertical-align: middle; }";
echo "table, th, td { border: 1px solid white; border-collapse; } th, td { background-color: #96D4D4;}";
echo "</style>";
foreach ($data as $item) {
    echo "<div>";
    echo "<tr>";
    echo  "<td>" . $item['id'] . "</td> " ;
    echo  "<td>" . $item['ip'] . "</td> " ;
    echo  "<td>" . $item['macadr'] . "</td> ";
    echo  "<td>" . $item['active'] . "</td> "; 
    echo  "<td>" . $item['engname']. "</td> " ; 
    echo  "<td>" . $item['description'] . "</td> ";
    echo "</tr>";   
    echo "</div>";    
}
echo "</table>";  
echo "
<form style='text-align: center;' action='index.html' method='get'> 
<button type='submit'>Back Home</button> 
</form> ";
