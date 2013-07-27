<html>
<head>
<title>Archives - Blog - H. Chase Stevens</title>
<meta name="author" content="H. Chase Stevens" />
<meta name="keywords" content="<?php echo $_GET['tag']; ?>" />
<link href="/style.css" rel="stylesheet" type="text/css">
<?php
	echo file_get_contents($_SERVER['DOCUMENT_ROOT'] . "blog/syntax_highlighter.html") . "\n";
	echo file_get_contents($_SERVER['DOCUMENT_ROOT'] . "bitp_script.html") . "\n";
	echo file_get_contents($_SERVER['DOCUMENT_ROOT'] . "analytics_script.html") . "\n"; ?>
</head>
<body>
<?php echo file_get_contents($_SERVER['DOCUMENT_ROOT'] . "header.html") . "\n"; ?>
<div class="blog_wrapper">

<!-- Sidebar -->

<div class="blog_sidebar">
<h2>Most Common Tags</h2>
<?php
$username = file_get_contents($_SERVER['NFSN_SITE_ROOT'] . "/protected/mysql_username");
$password = file_get_contents($_SERVER['NFSN_SITE_ROOT'] . "/protected/mysql_password");
$link = mysql_connect("chasepersonal.db",$username,$password) 
	or die("Could not connect! " . mysql_error());
mysql_select_db('blog',$link);
$post_query = "SELECT * FROM (SELECT `tag`, Count(`tag`) AS `tag_count` FROM `tags` GROUP BY `tag`) AS `tag_cloud` ORDER BY `tag_count` DESC LIMIT 0,10";
$result = mysql_query($post_query)
	or die("Query error: " . mysql_error());
echo "<ol>";
while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
	echo "<li><a href='/blog/blog_tag_search.php?tag=" . $row['tag'] . "'>" . $row['tag'] . "</a></li>\n";
}
echo "</ol>";
?>
<h2><a href="http://blog.chasestevens.com/archives.php">Archives</a></h2>
<? echo file_get_contents($_SERVER['DOCUMENT_ROOT'] . "blog/blog_search.html") . "\n"; ?>
</div>

<!-- Body -->

<div class="blog_post_container"> 
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
$post_query = "SELECT * FROM `posts` ORDER BY (time) DESC";
$post_result = mysql_query($post_query)
	or die("Query error: " . mysql_error());
echo "<div class='blog_post'>";
echo "<h1>Archives</h1>";
while ($row = mysql_fetch_array($post_result, MYSQL_ASSOC)) {
	$url_title = strtolower(urlencode(stripslashes($row["title"])));
	echo "<strong><a href='./read_post.php?title=" . $url_title . "&time=" . $row['time'] . "'>" . stripslashes($row['title']) . "</a></strong><br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>(Posted " . date("F j, Y",$row["time"]) . ")</i>";
	echo "<br /><br />";
}
?>
</div>
</div>
<div class="blog_footer">
<center>
<table border="0" cellspacing="12" cellpadding="0">
<tr>
	<?php
	if ($less_results) {
		echo "<td><a href=\"blog_tag_search.php?tag=" . $_GET['tag'] . "&limit=" . $less_results_limit . "\">newer posts</a></td>";
	}
	if ($less_results and $more_results){
		echo "<td><strong>&middot;</strong></td>";
	}
	if ($more_results) {
		echo "<td><a href=\"blog_tag_search.php?tag=" . $_GET['tag'] . "&limit=" . ($limit + 5) . "\">older posts</a></td>";
	}
	?>
</tr>
</table>
</center>
</div>

</div>
</body>
</html>