<div class="blog_sidebar">
<b>Most Common Tags</b>
<?php
$username = file_get_contents($_SERVER['NFSN_SITE_ROOT'] . "/protected/mysql_username");
$password = file_get_contents($_SERVER['NFSN_SITE_ROOT'] . "/protected/mysql_password");
$link = mysql_connect("chasepersonal.db",$username,$password) 
	or die("Could not connect! " . mysql_error());
echo "<!--Connection success!<br />-->";
mysql_select_db('blog',$link);
$post_query = "SELECT * FROM (SELECT `tag`, Count(`tag`) AS `tag_count` FROM `tags` GROUP BY `tag`) AS `tag_cloud` ORDER BY `tag_count` DESC LIMIT 0,10";
echo "<!--" . $post_query . "-->";
$result = mysql_query($post_query)
	or die("Query error: " . mysql_error());
echo "<!--Post success.-->";
echo "<ol>";
while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
	echo "<li><a href='/blog/blog_tag_search.php?tag=" . $row['tag'] . "'>" . $row['tag'] . "</a></li>\n";
}
echo "</ol>";
?>
<h2><a href="http://blog.chasestevens.com/archives.php">Archives</a></h2>
<div id="cse" style="width: 100%;">Loading</div>
<script src="//www.google.co.uk/jsapi" type="text/javascript"></script>
<script type="text/javascript"> 
  google.load('search', '1', {language : 'en', style : google.loader.themes.MINIMALIST});
  google.setOnLoadCallback(function() {
    var customSearchControl = new google.search.CustomSearchControl(
      '009406669255211514830:v5iubimgoum');

    customSearchControl.setResultSetSize(google.search.Search.SMALL_RESULTSET);
    customSearchControl.draw('cse');
  }, true);
</script>
 <style type="text/css">
  .gsc-control-cse {
    font-family: Georgia, serif;
    border-color: #e8e8e8;
    background-color: #e8e8e8;
  }
  input.gsc-input {
    border-color: #777777;
  }
  input.gsc-search-button {
    border-color: #333333;
    background-color: #333333;
  }
  .gsc-tabHeader.gsc-tabhInactive {
    border-color: #777777;
    background-color: #777777;
  }
  .gsc-tabHeader.gsc-tabhActive {
    border-color: #333333;
    background-color: #333333;
  }
  .gsc-tabsArea {
    border-color: #333333;
  }
  .gsc-webResult.gsc-result,
  .gsc-results .gsc-imageResult {
    border-color: #e8e8e8;
    background-color: #e8e8e8;
  }
  .gsc-webResult.gsc-result:hover,
  .gsc-imageResult:hover {
    border-color: #000000;
    background-color: #FFFFFF;
  }
  .gs-webResult.gs-result a.gs-title:link,
  .gs-webResult.gs-result a.gs-title:link b,
  .gs-imageResult a.gs-title:link,
  .gs-imageResult a.gs-title:link b {
    color: #444444;
  }
  .gs-webResult.gs-result a.gs-title:visited,
  .gs-webResult.gs-result a.gs-title:visited b,
  .gs-imageResult a.gs-title:visited,
  .gs-imageResult a.gs-title:visited b {
    color: #444444;
  }
  .gs-webResult.gs-result a.gs-title:hover,
  .gs-webResult.gs-result a.gs-title:hover b,
  .gs-imageResult a.gs-title:hover,
  .gs-imageResult a.gs-title:hover b {
    color: #444444;
  }
  .gs-webResult.gs-result a.gs-title:active,
  .gs-webResult.gs-result a.gs-title:active b,
  .gs-imageResult a.gs-title:active,
  .gs-imageResult a.gs-title:active b {
    color: #777777;
  }
  .gsc-cursor-page {
    color: #444444;
  }
  a.gsc-trailing-more-results:link {
    color: #444444;
  }
  .gs-webResult .gs-snippet,
  .gs-imageResult .gs-snippet,
  .gs-fileFormatType {
    color: #333333;
  }
  .gs-webResult div.gs-visibleUrl,
  .gs-imageResult div.gs-visibleUrl {
    color: #000000;
  }
  .gs-webResult div.gs-visibleUrl-short {
    color: #000000;
  }
  .gs-webResult div.gs-visibleUrl-short {
    display: block;
  }
  .gs-webResult div.gs-visibleUrl-long {
    display: none;
  }
  .gsc-cursor-box {
    border-color: #e8e8e8;
  }
  .gsc-results .gsc-cursor-box .gsc-cursor-page {
    border-color: #777777;
    background-color: #e8e8e8;
    color: #444444;
  }
  .gsc-results .gsc-cursor-box .gsc-cursor-current-page {
    border-color: #333333;
    background-color: #333333;
    color: #444444;
  }
  .gs-promotion {
    border-color: #CCCCCC;
    background-color: #E6E6E6;
  }
  .gs-promotion a.gs-title:link,
  .gs-promotion a.gs-title:link *,
  .gs-promotion .gs-snippet a:link {
    color: #0000CC;
  }
  .gs-promotion a.gs-title:visited,
  .gs-promotion a.gs-title:visited *,
  .gs-promotion .gs-snippet a:visited {
    color: #0000CC;
  }
  .gs-promotion a.gs-title:hover,
  .gs-promotion a.gs-title:hover *,
  .gs-promotion .gs-snippet a:hover {
    color: #444444;
  }
  .gs-promotion a.gs-title:active,
  .gs-promotion a.gs-title:active *,
  .gs-promotion .gs-snippet a:active {
    color: #00CC00;
  }
  .gs-promotion .gs-snippet,
  .gs-promotion .gs-title .gs-promotion-title-right,
  .gs-promotion .gs-title .gs-promotion-title-right *  {
    color: #333333;
  }
  .gs-promotion .gs-visibleUrl,
  .gs-promotion .gs-visibleUrl-short {
    color: #00CC00;
  }
</style></div>