<?php if (substr_count($_SERVER['HTTP_ACCEPT_ENCODING'], 'gzip')) ob_start("ob_gzhandler"); else ob_start();  //gzip
header("Content-Type:text/plain");
?>
<html>
<head>
<title>
<?php
$username = file_get_contents($_SERVER['NFSN_SITE_ROOT'] . "/protected/mysql_username");
$password = file_get_contents($_SERVER['NFSN_SITE_ROOT'] . "/protected/mysql_password");
$link = mysql_connect("chasepersonal.db",$username,$password) 
	or die("Could not connect! " . mysql_error());
mysql_select_db('blog',$link);
$post_query = "SELECT * FROM `posts` WHERE time = " . $_GET['time'];
$result = mysql_query($post_query)
	or die("Query error: " . mysql_error());
while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
	echo stripslashes($row["title"]);
}?>
 - H. Chase Stevens</title>
<meta name="author" content="H. Chase Stevens" />
<meta name="keywords" content="
<?php
	$meta_query = "SELECT tag FROM `tags` WHERE time = " . $_GET['time'];
	$meta_result = mysql_query($meta_query)
		or die("programming,philosophy,internet,linguistics");
	$out = "";
	while ($row = mysql_fetch_array($meta_result, MYSQL_ASSOC)) {
		$out = $out . stripslashes($row['tag']) . ",";
	}
	echo substr($out, 0, -1);
?>" />
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
$sidebar_query = "SELECT * FROM (SELECT `tag`, Count(`tag`) AS `tag_count` FROM `tags` GROUP BY `tag`) AS `tag_cloud` ORDER BY `tag_count` DESC LIMIT 0,10";
$result = mysql_query($sidebar_query)
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
$result = mysql_query($post_query)
	or die("Query error: " . mysql_error());
while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
	printf("<div class=\"blog_post\"><h2>%s </h2><h3>posted on: %s by <a class='author' href='https://plus.google.com/103927236717396636563?rel=author'>Chase Stevens</a></h3><p>%s</p>", stripslashes($row["title"]), date("l, F j, Y (g:i a)",$row["time"]), stripslashes($row["content"]));
	$tag_query = "SELECT tag FROM `tags` WHERE time = " . $row["time"] . " ORDER BY (tag) ASC";
	$tag_result = mysql_query($tag_query);
	echo "Tags: <em>";
	$tag_list = "";
	while ($tag = mysql_fetch_array($tag_result, MYSQL_ASSOC)) {
		$tag_list = $tag_list . "<a href='/blog/blog_tag_search.php?tag=" . $tag['tag'] . "'>" . $tag['tag'] . "</a>, ";
	}
	echo substr($tag_list, 0, -2);
	echo "</em>";
	//if ($_GET['time'] != "1347552063")
	//	echo "<div id='disembl'></div><script type='text/javascript' src='//disembl.com/disembl.js'></script></div>";
}
?>
</div>
</script>
</body>
</html>
