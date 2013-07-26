import fnmatch
import os
import Tkinter
import tkFileDialog
import ID3
from tkMessageBox import showinfo

root = Tkinter.Tk()
root.withdraw()
folder = tkFileDialog.askdirectory(title="Please select a music directory.")

matches = []
file_types = ['mp3','aiff']
for root, dirnames, filenames in os.walk(folder):
    for filename in reduce((lambda x,y: x + y), [fnmatch.filter(filenames, ('*.' + filetype)) for filetype in file_types]):
        matches.append(os.path.join(root, filename))

output = 'Title,Artist,Album,Track,Year,File Location (Do Not Alter)\n'
for song in matches:
    line = ''
    id3info = ID3.ID3(song)
    columns = [id3info.title,id3info.artist,id3info.album,id3info.track,id3info.year,song]
    for column in columns:
        line += '"' + str(column) + '",'
    line = line[:-1] + '\n'
    output += line

filename = tkFileDialog.asksaveasfilename(defaultextension='.csv',filetypes=[('All Files','.*'),('Comma Separated Values File','.csv')])
f = open(filename,'w')
f.write(output)
f.close()

showinfo("File Created","Your CSV file has been created and is ready for you to edit. After you have done so and saved, please click 'OK'.")

f = open(filename,'r')
f.readline() #Removing column titles
for line in f.readlines():
    line.replace('"','')
    columns = line.split(',')#0:title,1:artist,2:album,3:track,4:year,5:location
    id3info = ID3.ID3(columns[5])
    id3info['TITLE'] = columns[0]
    id3info['ARTIST'] = columns[1]
    id3info['ALBUM'] = columns[2]
    id3info['TRACKNUMBER'] = columns[3]
    id3info['YEAR'] = columns[4]
f.close()

showinfo("Success","Song metadata has been successfully updated.")
