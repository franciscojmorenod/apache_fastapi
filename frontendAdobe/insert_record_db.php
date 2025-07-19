<?php
if($_SERVER["REQUEST_METHOD"] == "POST") {
    $ipaddress = $_POST["ipaddress"];
}


$payload = json_encode([
    "name" => $ipaddress
]);

$options = [
    "http" => [
        "method" => "POST",
        "header" => "Content-type: application/json; character= UTF-8",
        "content" => $payload
    ]
    ];

$context = stream_context_create($options);

$json_data = file_get_contents("http://192.168.1.21:8000/insertdb",false, $context);

// $data = json_decode($json_data, true);
// if(is_array($data)) {
//     foreach ($data as $item) {
//         echo "Name: " . $item['name'] . "<br>";
//     }
// }

var_dump($json_data);