<?php
/*require_once('config.inc.php'); 

mysql_query("SET NAMES 'utf8'");

mysql_query("INSERT INTO movies(title,director,actors,description,ranking,greekTitle,imageUrl)
		VALUES('".$_POST["title"]."','".$_POST["director"]."',
		'".$_POST["actors"]."','".$_POST["description"]."',
		'".$_POST["ranking"]."','".$_POST["greekTitle"]."','".$_POST["imageUrl"]."')");

mysql_close($con); */

    class movie{
    public $title;
    public $director;
	public $url;
	public $description;
	public $actors;
	public $rank;
    public $id;
}

$source = file_get_contents('data/movieData.json');
$sourceArray=json_decode($source);
$len=count($sourceArray->movies);
$count=0;

        $params = new movie();
        $params->title=$_POST["title"];
        $params->director=$_POST["director"];
		$params->url=$_POST["imageUrl"];
		$params->description=$_POST["description"];
		$params->actors=$_POST["actors"];
		$params->rank=1;
        $params->id=$len;



if ($len) {
    echo $len;
        for ($i=0;$i<$len;$i++) {
            if ($sourceArray->movies[$i]->title===$params->title){
                echo "movie exists";
                $count++;
                break;
            } 
        } 
        if($count===0 && ($params->title!=null || $params->title!="")){
       array_push( $sourceArray->movies, $params );
                      echo "movie successfully saved"; }
}else{
    echo "nolen";
}

$jsonData = json_encode($sourceArray,JSON_PRETTY_PRINT);
file_put_contents('data/movieData.json',$jsonData);


?>