div_template = "<div id='{post_id}' class='blog_post'><img src='loading.gif' alt='Post loading' /></div>\n";

var get_vars = document.location.search.replace('?', '').split('&');
var limit = 0;
for (i in get_vars) {
    var get_var = get_vars[i];
    if (get_var.indexOf('limit') != -1) {
        limit = get_var.split('=')[1];
        break;
    }
}
var container = document.getElementById('container');
var _xmlhttp = new XMLHttpRequest();
_xmlhttp.onreadystatechange = function () {
    if (_xmlhttp.readyState == 4) {
        fetch_posts(_xmlhttp.responseText.split(','));
    }
}
_xmlhttp.open('GET', 'get_posts.php?limit=' + limit, true);
_xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
_xmlhttp.send();

function fetch_posts(post_ids) {
    var placeholders = "";
    post_ids.map(function (post_id) {
        placeholders += div_template.replace('{post_id}',post_id);
    });
    container.innerHTML = placeholders;
    post_ids.map(populate_post);
}

function populate_post(post_id) {
    var div = document.getElementById(post_id);
    var _xmlhttp = new XMLHttpRequest();
    _xmlhttp.onreadystatechange = function () {
        if (_xmlhttp.readyState == 4 ) {
            div.outerHTML = _xmlhttp.responseText;
        }
    }
    _xmlhttp.open('GET', 'get_blog_post.php?time=' + post_id, true);
    _xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    _xmlhttp.send();
    
    pre = document.evaluate('.//pre', div, null, XPathResult.UNORDERED_NODE_ITERATOR_TYPE, null).iterateNext();
    if (pre) {
        pre.innerHTML = pre.innerHTML.split('<').join('&lt;')
    }
}