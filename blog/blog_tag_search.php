<html>
<head>
<title>Posts about <?php echo $_GET['tag']; ?> - Blog - H. Chase Stevens</title>
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
$tag_query = "SELECT time FROM `tags` WHERE tag = \"" . $_GET['tag'] . "\" ORDER BY (time) DESC LIMIT " . $limit . ",5";
$search_tag_result = mysql_query($tag_query)
	or die("Query error: " . mysql_error());
echo "<!--Post success.-->";
echo "<h1>Posts with tag \"". $_GET['tag'] . "\":</h1>";
while ($tag_row = mysql_fetch_array($search_tag_result, MYSQL_ASSOC)) {
	$post_query = "SELECT * FROM `posts` WHERE time = " . $tag_row['time'];
	$result = mysql_query($post_query);
	while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
		$url_title = strtolower(urlencode(stripslashes($row["title"])));
		printf("<div class=\"blog_post\"><h2><a href='http://blog.chasestevens.com/read_post.php?title=%s&time=%s'>%s </a></h2><h3>posted on: %s by <a class='author' href='https://plus.google.com/103927236717396636563?rel=author'>Chase Stevens</a></h3><p>%s</p>", $url_title, $row["time"], stripslashes($row["title"]), date("l, F j, Y (g:i a)",$row["time"]), stripslashes($row["content"]));
		$tag_query = "SELECT tag FROM `tags` WHERE time = " . $row["time"] . " ORDER BY (tag) ASC";
		$tag_result = mysql_query($tag_query);
		echo "Tags: <em>";
		$tag_list = "";
		while ($tag = mysql_fetch_array($tag_result, MYSQL_ASSOC)) {
			$tag_list = $tag_list . "<a href='/blog/blog_tag_search.php?tag=" . $tag['tag'] . "'>" . $tag['tag'] . "</a>, ";
		}
		echo substr($tag_list, 0, -2);
		echo "</em></div>";
	}
}
$next_page_query = "SELECT time FROM `tags` WHERE tag = \"" . $_GET['tag'] . "\" ORDER BY (time) DESC LIMIT " . ($limit+5) . ",1";
$next_page_result = mysql_query($next_page_query);
$more_results = False;
while ($result = mysql_fetch_array($next_page_result, MYSQL_ASSOC)){
	$more_results = True;
}
$less_results = $limit > 0;
$less_results_limit = max(($limit - 5), 0)
?>
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