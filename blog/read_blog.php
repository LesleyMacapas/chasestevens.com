<?php
$username = file_get_contents($_SERVER['NFSN_SITE_ROOT'] . "/protected/mysql_username");
$password = file_get_contents($_SERVER['NFSN_SITE_ROOT'] . "/protected/mysql_password");
$link = mysql_connect("chasepersonal.db",$username,$password) 
	or die("Could not connect! " . mysql_error());
mysql_select_db('blog',$link);
$post_query = "SELECT * FROM `posts` ORDER BY (time) DESC";
$result = mysql_query($post_query)
	or die("Query error: " . mysql_error());
while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
    printf("<div class=\"blog_post\"><h2><a href='google.com'>%s </a></h2><h3>posted on: %s </h3><p>%s</p>", stripslashes($row["title"]), date("l, F j, Y (g:i a)",$row["time"]), stripslashes($row["content"]));
	echo "<br />";
	$tag_query = "SELECT tag FROM `tags` WHERE time = " . $row["time"];
	$tag_result = mysql_query($tag_query);
	echo "Tags: <em>";
	$tag_list = "";
	while ($tag = mysql_fetch_array($tag_result, MYSQL_ASSOC)) {
		$tag_list = $tag_list . "<a href='/blog/blog_tag_search.php?tag=" . $tag['tag'] . "'>" . $tag['tag'] . "</a>, ";
	}
	echo substr($tag_list, 0, -2);
	echo "</em></div>";
}
?>