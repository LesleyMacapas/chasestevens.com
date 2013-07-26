import urllib
import urllib2
import os
import ID3
xml_url = "http://pinochan.net/overbooru/xmas/playlist.xml"
localdir = "C:\\Xmas_Music"
webdir = xml_url[::-1][xml_url[::-1].find('/'):][::-1]
try:
    os.chdir(localdir)
    print "Downloading to", localdir
except:
    os.mkdir(localdir)
    print "Creating download directory", localdir
try:
    xml_page = urllib2.urlopen(xml_url)
except:
    print "Error opening playlist URL."
    raw_input()
    quit()
print "Parsing XML"
xml = xml_page.read().replace("\t","").replace("\n","")
tracks = xml.split('<track>')[1:]
track_dict = dict()
def get_elem(xml,tag):
    start_tag = "<" + tag + ">"
    end_tag = "</" + tag + ">"
    return xml[(xml.find(start_tag)+len(start_tag)):xml.find(end_tag)]
down_count = 0
for track in tracks:
    track_id = get_elem(track,"location")
    track_dict[track_id] = dict()
    print "%s:" %track_id
    track_dict[track_id]['Artist'] = get_elem(track,"creator").replace("&#039;","'").replace("&amp;","&")
    print "\t Artist: %s" %track_dict[track_id]['Artist']
    track_dict[track_id]['Title'] = get_elem(track,"title").replace("&#039;","'").replace("&amp;","&")
    print "\t Title: %s" %track_dict[track_id]['Title']
    track_dict[track_id]['URL'] = webdir + track_id
    if not track_id in os.listdir(os.getcwd()):
        print "\t File not found in directory, downloading now."
        try:
            urllib.urlretrieve(track_dict[track_id]['URL'],filename=track_id)
            print "\t Download complete, editing metadata."
            down_count += 1
        except:
            print "\t Could not download %s, moving on to next file." % track_dict[track_id]['URL']
            break
        try:
            id3info = ID3.ID3(track_id)
            id3info['TITLE'] = track_dict[track_id]['Title']
            id3info['ARTIST'] = track_dict[track_id]['Artist']
            print "\t Done editing metadata: %s" %id3info
        except:
            print "\t There was an error editing metadata."
    else:
        print "\t File already in directory."
print "Downloaded %s files." %down_count
print "%s files in %s." %(len(os.listdir(os.getcwd())),os.getcwd())
print "Press Enter to exit."
raw_input()
