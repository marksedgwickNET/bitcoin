<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Binary/Text Converter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            max-width: 400px;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
        }
        input[type="submit"] {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
        }
        .result {
            margin-top: 20px;
            font-weight: bold;
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>

<h2>Binary/Text Converter</h2>
<form method="post">
    <input type="text" name="inputValue" placeholder="Enter binary or text" required>
    <select name="conversionType">
        <option value="binaryToText">Binary to Text</option>
        <option value="textToBinary">Text to Binary</option>
    </select>
    <input type="submit" value="Convert">
</form>

<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    function binaryToText($binaryString) {
        $binaryArray = explode(' ', $binaryString);
        $text = '';

        foreach ($binaryArray as $binary) {
            $decimal = bindec($binary);
            $text .= chr($decimal);
        }

        return $text;
    }

    function textToBinary($text) {
        $binaryString = '';
        for ($i = 0; $i < strlen($text); $i++) {
            $binaryString .= sprintf("%08b", ord($text[$i])) . ' ';
        }
        return trim($binaryString);
    }

    $inputValue = $_POST['inputValue'];
    $conversionType = $_POST['conversionType'];
    $result = '';

    if ($conversionType == 'binaryToText') {
        $result = binaryToText($inputValue);
    } elseif ($conversionType == 'textToBinary') {
        $result = textToBinary($inputValue);
    }

    echo "<div class='result'>Result: " . htmlspecialchars($result) . "</div>";
}
?>

</body>
</html>