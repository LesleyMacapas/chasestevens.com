<?php
$username = file_get_contents($_SERVER['NFSN_SITE_ROOT'] . "/protected/mysql_username");
$password = file_get_contents($_SERVER['NFSN_SITE_ROOT'] . "/protected/mysql_password");
$link = mysql_connect("chasepersonal.db",$username,$password) 
	or die("Could not connect! " . mysql_error());
mysql_select_db('blog',$link);
$limit = mysql_real_escape_string($_GET['limit'],$link);
if ($_GET['limit'] == '') {
	$limit = 0;
}
$post_query = "SELECT time FROM `posts` ORDER BY (time) DESC LIMIT " . $limit . ",5";
$result = mysql_query($post_query)
	or die("Query error: " . mysql_error());
$results = array();
while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
	$results[] = $row['time'];
}
echo implode('\n',$results);
?>