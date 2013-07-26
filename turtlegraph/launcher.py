from urllib import *
from tkMessageBox import *
import Tkinter
from os import remove, rename
root = Tkinter.Tk()
root.withdraw()
try:
    local_lastupdated_io = open('lastupdated.txt','r')
    local_lastupdated = local_lastupdated_io.read()
    local_lastupdated_io.close()
except:
    local_lastupdated_io = open('lastupdated.txt','w')
    local_lastupdated_io.close()
    local_lastupdated = None
try:
    remote_lastupdated_location = urlopen('http://www.chasestevens.com/turtlegraph/lastupdated.txt')
    temp_lastupdated = open('lastupdated.temp.txt','w')
    while True:
        datastream =  remote_lastupdated_location.read(8192)
        if not datastream:
            break
        temp_lastupdated.write(datastream)
    temp_lastupdated.close()
except:
    import turtlegraph
    quit()
remote_lastupdated_io = open('lastupdated.temp.txt','r')
remote_lastupdated = remote_lastupdated_io.read()
remote_lastupdated_io.close()
if remote_lastupdated != local_lastupdated:
    changelog_location = urlopen('http://www.chasestevens.com/turtlegraph/changelog.txt')
    changelog = ''
    while True:
        datastream = changelog_location.read(8192)
        if not datastream:
            break
        changelog += datastream
    proceed = askyesno('Update Available','An update has been found for TurtleGraph. Would you like to update now?\n\n' + str(changelog))
    if proceed:
        try:
            remote_helpfile_location = urlopen('http://www.chasestevens.com/turtlegraph/helpfile.txt')
            helpfile_io = open('helpfile.txt','w')
            help_text = ''
            while True:
                datastream = remote_helpfile_location.read(8192)
                if not datastream:
                    break
                help_text += datastream
            helpfile_io.write(help_text)
            helpfile_io.close()
            remote_turtlegraph_location = urlopen('http://www.chasestevens.com/turtlegraph/turtlegraph.py')
            turtlegraph_io = open('turtlegraph.temp.py','w')
            turtlegraph_text = ''
            while True:
                datastream = remote_turtlegraph_location.read(8192)
                if not datastream:
                    break
                turtlegraph_text += datastream
            turtlegraph_io.write(turtlegraph_text)
            turtlegraph_io.close()
            try:
                remove('turtlegraph.py')
                remove('turtlegraph.pyc')
            except:
                pass
            rename('turtlegraph.temp.py','turtlegraph.py')
            remove('lastupdated.txt')
            rename('lastupdated.temp.txt','lastupdated.txt')
            showinfo('Update Successful','TurtleGraph was successfully updated.')
        except:
            showerror('Update Unsuccessful','Turtlegraph was not successfully updated. Some files may be corrupt or missing. Update will run again next time TurtleGraph is launched.')
            remove('lastupdated.temp.txt')
            remove('lastupdated.txt')
    else:
        remove('lastupdated.temp.txt')
else:
    remove('lastupdated.temp.txt')
import turtlegraph
quit()
