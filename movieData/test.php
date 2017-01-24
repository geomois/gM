<?php
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'imdb.wemakesites.net/api/nm0000115?api_key=ed3bafe9-287b-4b42-8265-97027f2755ae'); // Nicolas Cage
$output = curl_exec($ch);
echo $output;
if (gettype($ch) == "resource") {
    if (mysql_num_rows($ch) != 0 ) {
        while ($row = mysql_fetch_assoc($ch)) {
            $output[] =$row;
        }
    }
}
echo $output;
curl_close($ch);
?>