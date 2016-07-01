# -*- coding: utf-8 -*-
from win32com.client import constants
from PyQt4.QtGui import *
import win32com.client as win32
import os
import sys

class importdoc_class:
    def directorydestination(self):
        dirdes=self.recoverdestinationdir()
        dirdes=dirdes.replace( "/","\\")
        if (dirdes=="0"):
            dirdes="."
        return dirdes

    # It opens and converts a ".doc" file into an HTML file
    def subopendoc(self,docfile,dirdes):
        if (os.path.exists(docfile)):
          try:
                dirfile=docfile
                newdirfile=dirfile.replace( "/","\\")
                word = win32.gencache.EnsureDispatch('Word.Application')
                word.Visible = False
                doc = word.Documents.Open(newdirfile)
                orginalfilename=os.path.splitext(os.path.split(newdirfile)[1])[0]
                neudir=dirdes+r"\ ".strip() +orginalfilename+r".html"
                neudir=neudir.replace( "/","\ ".strip())
                print(neudir+"\n")
                doc.SaveAs(str(neudir),constants.wdFormatHTML)
                doc.Close()
                word.Quit()
                ndurl=neudir.replace( "\\","/")
                ndurl=r"file:///"+ndurl
          except:
              ndurl="0"
              os.system('cls')
              print ("Importdoc_Unexpected error:", sys.exc_info()[0])
        else:
            ndurl="0"
        return ndurl

    def destinationfiletxt(self,dir):
        file = open("lists_files/destinationdir.txt", "w")
        file.write(dir)
        file.close()

    def  SfileHTML(self,dir,context):
        file = open(dir, 'wb')
        file.write(context.encode('utf8'))
        file.close()

    def recoverdestinationdir(self):
        try:
            file = open('lists_files/destinationdir.txt', 'r')
            str=file.read()
            if(not(os.path.isdir(str))):
                str="0"
            file.close()
        except:
            str="0"
        return str

    def importhtmlfile(self,self1):
        dirdes=self.recoverdestinationdir()
        HTMLfile=QFileDialog.getOpenFileName(self1, caption="Import HTML File", directory=dirdes , filter="Text files (*.htm*)")
        if (HTMLfile!=''):
            if (os.path.exists(HTMLfile)):
                HTMLfile=r"file:///"+HTMLfile
            else:
                HTMLfile="0"
        else:
            HTMLfile=''
        return HTMLfile
