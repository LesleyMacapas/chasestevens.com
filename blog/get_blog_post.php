<?php 
if (substr_count($_SERVER['HTTP_ACCEPT_ENCODING'], 'gzip')) ob_start("ob_gzhandler"); else ob_start();  //gzip
header("Content-Type:text/plain");
?>
<?php
$username = file_get_contents($_SERVER['NFSN_SITE_ROOT'] . "/protected/mysql_username");
$password = file_get_contents($_SERVER['NFSN_SITE_ROOT'] . "/protected/mysql_password");
$link = mysql_connect("chasepersonal.db",$username,$password) 
	or die("Could not connect! " . mysql_error());
mysql_select_db('blog',$link);
$post_query = "SELECT * FROM `posts` WHERE time = " . $_GET['time'];
$result = mysql_query($post_query)
	or die("Query error: " . mysql_error());
?>
<div class="blog_post">
<?php
$result = mysql_query($post_query)
	or die("Query error: " . mysql_error());
while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
	printf("<h2><a href='http://blog.chasestevens.com/read_post.php?title=%s&time=%s'>%s </a></h2><h3>posted on: %s by <a class='author' href='https://plus.google.com/103927236717396636563?rel=author'>Chase Stevens</a></h3><p>%s</p>", $url_title, $row["time"], stripslashes($row["title"]), date("l, F j, Y (g:i a)",$row["time"]), stripslashes($row["content"]));
	$tag_query = "SELECT tag FROM `tags` WHERE time = " . $row["time"] . " ORDER BY (tag) ASC";
	$tag_result = mysql_query($tag_query);
	echo "Tags: <em>";
	$tag_list = "";
	while ($tag = mysql_fetch_array($tag_result, MYSQL_ASSOC)) {
		$tag_list = $tag_list . "<a href='/blog/blog_tag_search.php?tag=" . $tag['tag'] . "'>" . $tag['tag'] . "</a>, ";
	}
	echo substr($tag_list, 0, -2);
	echo "</em>";
}
?>
</div>
