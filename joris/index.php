<html><head></head><body>
<h2>Joris Automated Help Desk</h2>
<?php
$conversation = $_GET['conversation'];
$input = $_GET['input'];
$prev_resp = $_GET['prev_resp'];
$response = "";
echo $conversation;
if ($input == $prev_resp && $prev_resp != ""){
	$response = "We agree. This is <i>excellent</i>.";
} elseif (strpos($input, "they")){
	$response = "No they don't.";
} elseif (strlen($input) > 50) {
	$response =  "Macro towards the present.";
} elseif ($input[strlen($input)-1] == "?") {
	$response =  "How about no?";
} else {
	$response = "You should reconsider your position on that.";
}
if (rand(0, 10) == 1){
	$response = "What?";
}
$prev_resp = $response;
$response = "<b>Joris:</b> " . $response . "<br />";
$input = "<b>You:</b> " . $input . "<br />";
if ($input != "<b>You:</b> <br />"){
	echo $input;
	echo $response;
	$conversation .= $input . $response;
}
?>
<form action="index.php" method="get">
<b>You:</b> <input type="text" name="input" />
<input type="hidden" name="conversation" value=<?php echo '"'; echo $conversation; echo '"'; ?> />
<input type="hidden" name="prev_resp" value=<?php echo '"'; echo $prev_resp; echo '"'; ?> />
<input type="submit" />
</form>
</body>
</html>
