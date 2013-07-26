#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#enable debugging
import cgitb
import cgi
import random
cgitb.enable()

#get books
global books
f = open('/home/public/broverbs/books.txt')
books = [book.replace('\n','') for book in f.readlines()]
f.close()

#get names
global names
f = open('/home/public/broverbs/names.txt')
names = [name.replace('\n','') for name in f.readlines()]
f.close()

#get proverbs
global proverbs
f = open('/home/public/broverbs/proverbs.txt')
proverbs = [proverb.replace('\n','') for proverb in f.readlines()]
f.close() 

#get hashtags
global hashtags
f = open('/home/public/broverbs/hashtags.txt')
hashtags = [hashtag.replace('\n','') for hashtag in f.readlines()]
f.close() 

_preamble,_name,_proverb,_homo,_hashtag,_book,_n1,_n2 = [None] * 8

def get_book(book=None,n1=None,n2=None):
	try:
		book = books[book]
	except:
		book = random.choice(books)
	global _book
	global _n1
	global _n2
	_book = books.index(book)
	_n1 = random.randrange(1,80) if n1 == None else n1
	_n2 = random.randrange(1,180) if n2 == None else n2
	return "-%s %s:%s" %(book,str(_n1),str(_n2))

def get_name(name=None):
	try:
		name = names[name]
	except:
		name = random.choice(names)
	global _name
	_name = names.index(name)
	return name

def get_proverb(proverb=None):
	try:
		proverb = proverbs[proverb]
	except:
		proverb = random.choice(proverbs)
	global _proverb
	_proverb = proverbs.index(proverb)
	return proverb
	
def get_homo(homo=None):
	global _homo
	if homo==None:
		_homo = int(random.random() > 0.75)
		return "No homo. " if _homo else ""
	if homo:
		_homo = 1
		return "No homo. "
	_homo = 0
	return ""
	
def get_hashtag(hashtag=None):
	global _hashtag
	if hashtag == -1:
		_hashtag = -1
		return ""
	try:
		hashtag = hashtags[hashtag]
		_hashtag = hashtags.index(hashtag)
	except:
		has_hashtag = random.random() > 0.65
		hashtag = random.choice(hashtags) if has_hashtag else ""
		if has_hashtag:
			_hashtag = hashtags.index(hashtag)
		else:
			_hashtag = -1
	return hashtag

def get_broverb(preamble=None,name=None,proverb=None,homo=None,hashtag=None,book=None,n1=None,n2=None):
	output = "<div id='broverb'>"
	global _preamble
	if preamble == None:
		preamble = random.choice((True,False))
		_preamble = int(preamble)
	if preamble:
		output += "And lo, the brophet %s did say, \"%s\" " %(get_name(name),get_proverb(proverb)[:-1])
		_preamble = 1
	else:
		output += get_proverb(proverb)
		_preamble = 0
	output += get_homo(homo)
	output += get_hashtag(hashtag)
	output += '''</div>
	<div id='bottomhalf'>
		<div id='refresh'>
			<a href='http://broverbs.chasestevens.com'>
				<img src='refresh.png' alt='Refresh page' />
			</a>
		</div>
		<div id='book'>%s</div>
	</div>''' %(get_book(book,n1,n2))
	return output

print "Content-Type: text/html"
print
html_template = '''
<html>
	<head>
		<title>
			Broverbs
		</title>
		<link href="./style.css" rel="stylesheet" type="text/css">

	</head>
	<!-- Google Analytics Script -->
	<script type="text/javascript">

	  var _gaq = _gaq || [];
	  _gaq.push(['_setAccount', 'UA-7655653-1']);
	  _gaq.push(['_trackPageview']);

	  (function() {
		var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
		ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
		var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
	  })();

	</script>
	<!-- onLoad='window.history.pushState("object or string", "Title", "_ADDRESSBAR");' -->
	<body>
		<div id='wrapper'>
			<div id='header'>
			</div>
			<div id='broverb_container'>
				_BROVERB
			</div>
			<div id="links">
				<div id="submit">
					<a href="mailto:broverbs@chasestevens.com?subject=Broverb" target="_blank">Submit a broverb</a>
				</div>
				<div id="social">
					<a href="_PERMALINK"><img src="permalink.png" alt="Permalink" /></a>
					<a href="http://www.facebook.com/sharer.php?u=_URIPERMALINK&t=Broverbs" target="_blank">
					<img src="facebook.png" /></a>
					<a href="https://twitter.com/share" class="twitter-share-button" data-via="hchasestevens" data-url="_PERMALINK" data-size="large" data-count="none">Tweet</a>
					<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
					<a href="http://www.reddit.com/submit" onclick="window.location = 'http://www.reddit.com/submit?url=' + encodeURIComponent('_PERMALINK'); return false"> <img src="reddit.png" alt="submit to reddit" /> </a>
				</div>
			</div>
			<div id='footer'>
			<a href='http://www.chasestevens.com/'>Who made this?</a>
			</div>
		</div>
	</body>
</html>
'''
form = cgi.FieldStorage()
if form.has_key("id"):
	try:
		values = map(int,form["id"].value.replace('None','0').split(','))
		broverb = get_broverb(values[0],values[1],values[2],values[3],values[4],values[5],values[6],values[7])
		html_template = html_template.replace('_BROVERB',broverb)
	except Exception as e:
		print "<!-- %s -->" %(e)
		html_template = html_template.replace('_BROVERB',get_broverb())
else:
	html_template = html_template.replace('_BROVERB',get_broverb())
html_template = html_template.replace('_PERMALINK',"http://broverbs.chasestevens.com/index.cgi?id=%s"%(','.join(map(str,[_preamble,_name,_proverb,_homo,_hashtag,_book,_n1,_n2]))))
html_template = html_template.replace('_ADDRESSBAR',"/broverbs/index.cgi?id=%s"%(','.join(map(str,[_preamble,_name,_proverb,_homo,_hashtag,_book,_n1,_n2]))))
import urllib
html_template = html_template.replace('_URIPERMALINK',urllib.quote_plus("http://broverbs.chasestevens.com/index.cgi?id=%s"%(','.join(map(str,[_preamble,_name,_proverb,_homo,_hashtag,_book,_n1,_n2])))))
print html_template
print "<!-- http://broverbs.chasestevens.com/index.cgi?id=%s -->"\
%(','.join(map(str,[_preamble,_name,_proverb,_homo,_hashtag,_book,_n1,_n2])))