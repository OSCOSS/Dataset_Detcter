# -*- coding: utf-8 -*-

import operator
import os
import sys
import timeit
import time
from os import listdir
from os.path import isfile, join
from PyQt4.QtCore import *
from PyQt4.QtGui import *


import Harvester_abbandphraseGenerator.abbrivationgenrator as  abbgenharinstance
abbgenhar=abbgenharinstance.abb_extractor_class()
import Harvester_abbandphraseGenerator.harvestor as harvestorinstance
harvestor=harvestorinstance.harvestorclass()
import Harvester_abbandphraseGenerator.phrasemader as phraseharvestorinstance
phraseharvestor=phraseharvestorinstance.phrasegenrator_class()
from Result import itembyitem, Choose_Datasetrefrences
from MainPackage import Main_Windows_form_ui
from html_and_doc_handler import Htmledit
from html_and_doc_handler import  importdoc as importdco_instance
importdoc=importdco_instance.importdoc_class()
from similarity_cos_tf_idf import combinedapproach as combinedapproach_instance
combinedapproach=combinedapproach_instance.combinedapproach_class()
from similarity_cos_tf_idf import aux_functions as auxfunctions
auxfun=auxfunctions.auxfunclass

class MainClass(QMainWindow, Main_Windows_form_ui.Ui_MainWindow1):

    #  It is a constructor and is automatically called.
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

    #  The interface is connected to related functions.
        self.actionExit.triggered.connect(self.close)
        self.actionImport_a_word_file.triggered.connect(self.opendoc)
        self.actionImport_HTMl_file.triggered.connect(self.importhtml)
        self.actionConvert_all_files_in_directory.triggered.connect(self.convertdirectoryhtml)
        self.actionsaveHtmlfile.triggered.connect(self.Savehtmlf)
        self.webView.mouseDoubleClickEvent=self.editwebweiw
        self.actionhtmledit.triggered.connect(self.editHtmlshow)
        self.actionHarvestor.triggered.connect(self.harvestdata)
        self.Search_t_final.triggered.connect(self.combinedapp)
        self.actionAbb_Phrase.triggered.connect(self.specialfeaturs)
        self.checkitbit.triggered.connect(self.imbyim)
        self.EXportRDFGRaph.triggered.connect(self.choosedatasetref)

    # It recovers the destination directory.
        dirt= importdoc.recoverdestinationdir()
        self.dircheck(dirt,1)

    # The initial text in webview element in the main form.
        self.webView.setHtml("<html><p style=\"padding-top: 2cm;\">Main functionalities:</p><ul style=\"padding-top: 0,5cm;\"><li>File Menu: <ul><li>Import a Paper.</li></ul></li><li>Run Menu: <ul><li>Harvest Datasets' Titles from da|ra</li><li>Extract Special Features from Harvested Titles</li><li>Detect Datasets' References in the Imported Paper</li></ul></li><li>Result Menu:<ul><li>Check Detected References in the Imported Paper (One by One)</li><li>Create a JSON File for an Analyzed Paper</li></ul></li></ul></html>")

    # It takes a text file and then, it puts each line into an item on the output list.
    def readtoarr2(self,str):
        with open(str, "r", encoding="utf-8") as f:
            mylist = list(f)
        fl=[]
        for item in mylist:
            item=item.rstrip('\n')
            fl.append(item)
        return  fl

    # It show datasets refrences in the imported paper to the user ( imbyim= item by item ).
    # It provides the name of the imported paper and the HTML document of the file.
    # It calls the related form and feeds the provided information to the form.
    def imbyim(self):
        text1 = self.labelcurrent.text()
        text1 = text1.replace('File Name:','')
        str1 = self.webView.page().mainFrame().toHtml()
        self.main = itembyitem.Maindailog(self, str(str1), text1)
        self.main.show()

    # It extracts special features from titles.
    def specialfeaturs(self):
        start_time = time.time()
        os.system('cls')
        print('[#############Harvesting of titles in dara is started!##################]10%')

        # It creates two files from harvested information from dara (these two files are doi and titles).
        harvestor.doititlecaller()
        print('[#############Harvesting of titles in dara is done!!####################]60%')
        print('[####Extracting abbreviations from the harvested titles is started!!####]61%')

        # It extracts abbreviations from the harvested titles.
        abbgenhar.main()
        print('[#####Extracting abbreviations from the harvested titles is done!! #####]90%')
        print('[###Extracting special phrases from the harvested titles is started!!###]91%')

        # It extracts special phrases from the harvested titles.
        phraseharvestor.phrasemain()
        print('[############################it is done#################################]60%')
        print("--- %s seconds ---" % (time.time() - start_time))

    # It provides information for per-special_feature work flow.
    # It puts all refrences information of a paper into an array.
    # This information is about the 5 most similar titles to each refrences.
    # It helps Genratesugestion() function.
    # It returns two lists ( 1. a list of special features, 2. a list of titles and their similarity score.)
    def voting_first(self,itemofdir):
        text1=itemofdir
        text1=text1.replace('File Name:','')
        text1=text1.replace('.html','')
        nameoffile=[]
        tf=[]
        for file in os.listdir("lists_files/Testlog2/"+text1+"/"):
          if file!='time.txt':
            if file.endswith(".txt"):
                indexx=file.index('_')
                nameoffile.append(file[0:indexx])
                ls= auxfun.readtoarr2(auxfun,'lists_files/Testlog2/' + text1 + '/' + file)
                endindex=len(ls)/3
                if endindex>6:
                    endindex=6

                tempobj=[]
                tempobj.append(file[0:indexx])
                tempobj.append('0')
                tf.append(tempobj)

                for i in range (0,int(endindex)):
                    tempobj=[]

        # The first three rows of each file are related to information of a refrence (They are skipped).
                    if i==0:
                        pass
                    else:
                        i=i*3
                        tempobj.append(ls[i+2].replace('TExT:',''))
                        tempobj.append(ls[i+1].replace('value:',''))
                        tf.append(tempobj)
        listsetnamefile=list(set(nameoffile))
        return listsetnamefile,tf

    # It sorts titles based on the number of occurrences of titles in firstly.
    # It sorts titles based on the similarity score secondly.
    # It helps Genratesugestion() function.
    def splitofvoted(self,ls1,xf,ls3):
        ls2=[]
        for abb in ls1:
            ls=[]
            for title in xf:
                if abb.lower() in title[1].lower():
                    ls.append(title)
            ls=self.newlistplusmaxsimilarityscore(ls,ls3)
            ls=sorted(ls,key=operator.itemgetter(0, 2), reverse=True)
            ls2.append(ls)
        return ls1,ls2

    # It returns a list of titles which contains the number of occurrences of each
    # and the maximum similarity score of each.
    def newlistplusmaxsimilarityscore(self,ls_count_title,ls2_title_index):
        newlist=[]
        for titlearr in ls_count_title:
            temp=[]
            newlisttemp=[]
            title=titlearr[1]
            for indexarr in ls2_title_index:
                if title==indexarr[0]:
                    auxitem=indexarr[1]
                    temp.append(float(auxitem))
            value=max(temp)
            newlisttemp.append(titlearr[0])
            newlisttemp.append(titlearr[1])
            newlisttemp.append(value)
            newlist.append(newlisttemp)
        return newlist

    # It generates information for per-Special_features work flow.
    def Genratesugestion(self):
        directory='.\lists_files\Testlog2'
        lsnameofdir=[x[0] for x in os.walk(directory)]
        lsnameofdir1=[]
        for item in lsnameofdir:
            lsnameofdir1.append(item.replace('.\\lists_files\\Testlog2\\',''))
        lsnameofdir1.pop(0)
        text1=lsnameofdir1[0]
        for itemofdir in lsnameofdir1:
            ls1,ls2=self.voting_first(itemofdir)
            tf=[]
            temp=''
            for item in ls2:
                if item[0] in ls1:
                    if temp=='' or temp!=item[0]:
                        tf.append(item[0])
                        temp=item[0]
                else:
                    tf.append(item[0])

            withoutduplicate=list(set(tf))
            countedlist=[]
            for item in withoutduplicate:
                df=[]
                number=tf.count(item)
                df.append(number)
                df.append(item)
                countedlist.append(df)
            xf=[]

            for item in ls1:
                for item1 in countedlist:
                    if item.lower() in item1[1].lower():
                        xf.append(item1)

            ls1,xf=self.splitofvoted(ls1,xf,ls2)

            for item in xf:
                txt11=[]
                fileofanalysis=item[-1]
                nameoffileofanalysis=fileofanalysis[1]
                if not os.path.exists('.\lists_files\SSuggested_Candidate\\'+itemofdir):
                        os.makedirs('.\lists_files\SSuggested_Candidate\\'+itemofdir)
                f = open('.\lists_files\SSuggested_Candidate\\'+itemofdir+'\\'+nameoffileofanalysis+'.txt','wb')
                for item1 in item:
                        txt11.append(str(item1[0])+'__behnam__'+item1[1]+'__behnam__'+str(item1[2]))

                txt11=list(set(txt11))
                txt111=[]
                for ix in txt11:
                   tempauxitem=[]
                   splitix=ix.split('__behnam__')
                   tempauxitem.append(int(splitix[0]))
                   tempauxitem.append(splitix[1])
                   tempauxitem.append(float(splitix[2]))
                   txt111.append(tempauxitem)
                txt212=''
                txt11=sorted(txt111,key=operator.itemgetter(0, 2), reverse=True)
                for izt in txt11:
                    txt212+=str(izt[0])+'____'+izt[1]+'____'+str(izt[2])+u"\n"
                f.write(txt212.encode('UTF-8'))
                f.close()

    # Combination of Cosine similarity and Tf-Idf. ( "combinedapp" = combination approach)
    def combinedapp(self):
        start = timeit.default_timer()
        content1=self.webView.page().mainFrame().toHtml()
        FiLeNaMe=self.labelcurrent.text()
        combinedapproach.final_approach(content1, FiLeNaMe)
        stop = timeit.default_timer()
        os.system('cls')
        time.sleep(2)
        self.Genratesugestion()
        print('TOTAL TIME:'+str(stop-start))

    # It imports a ".doc" File into application.
    def opendoc(self):
        start_time = time.time()
        dirdes= importdoc.directorydestination()
        docfile=QFileDialog.getOpenFileName(self, caption="Import Word File", directory=dirdes , filter="Text files (*.doc*)")
        self.browseropendestination1(docfile[:docfile.rfind('/')].replace("/","\\"))
        if(docfile!=''):
            self.progressbar.setVisible(True)
            self.progressbar.setValue(50)
            filedir= importdoc.subopendoc(docfile, dirdes)
            if (filedir!="0"):
                self.webView.setUrl(QUrl(filedir))
                namehtmlfile=filedir.split('/')
                fhn=namehtmlfile[len(namehtmlfile)-1]
                self.labelcurrent.setText('File Name:'+fhn)
            else:
                self.webView.setHtml("<P align=\"center\"><Font color=\"red\"> File was not loaded properly!<br> Please try again.</Font></P>")
            self.progressbar.setVisible(False)
        print("--- %s seconds ---" % (time.time() - start_time))

    #   It checks the destination directory (e.g. for saving HTML files).
    def dircheck(self,dirt,mode):
         if (dirt!="0"):
             self.lineEdit.setText(dirt)
         else:
            if(mode==1):
               self.lineEdit.setText("The path is not selected yet. We'll use the directory of project.")
            elif(mode==2):
               self.lineEdit.setText("You have not selected any correct directory. We'll use the directory of project. ")

    # It sets the definition directory.
    def browseropendestination1(self,dir):
        importdoc.destinationfiletxt(dir)
        dirt= importdoc.recoverdestinationdir()
        self.dircheck(dirt,2)

    # It imports an HTML file.
    def importhtml(self):
        start_time = time.time()
        url= importdoc.importhtmlfile(self)
        self.browseropendestination1(url[url.find('file:///')+8:url.rfind('/')].replace("/","\\"))
        print(url[url.find('file:///')+8:url.rfind('/')].replace("/","\\"))
        if (url!=''):
            self.progressbar.setVisible(True)
            self.progressbar.setValue(50)
            self.labelfile.setText(url)
            if(url!="0"):
                self.webView.setUrl(QUrl(url))
                namehtmlfile=url.split('/')
                fhn=namehtmlfile[len(namehtmlfile)-1]
                self.labelcurrent.setText('File Name:'+fhn)
            else:
                self.webView.setHtml("<P align=\"center\"><Font color=\"red\"> File was not loaded properly!<br> Please try again.</Font></P>")
            self.progressbar.setVisible(False)
        print("--- %s seconds ---" % (time.time() - start_time))

    # It converts all ".doc" files in a directory.
    def convertdirectoryhtml(self):
        start_time = time.time()
        dirdes= importdoc.directorydestination()
        dir = str(QFileDialog.getExistingDirectory(self, caption="Select Directory",directory=dirdes))
        print('this is:'+dir+'\n')
        self.browseropendestination1(dir)
        if(dir!=''):
            onlyfiles = [ f for f in listdir(dir) if (isfile(join(dir,f)) and f.endswith(".docx")) or (isfile(join(dir,f)) and f.endswith(".doc")) ]
            dirdes= importdoc.recoverdestinationdir()
            print(dirdes)
            i=0
            lenght=len(onlyfiles)
            if(lenght!=0):
                portion=100/lenght
                self.progressbar.setVisible(True)
                self.labelfile.setVisible(True)
                for file in onlyfiles:
                   i=i+1
                   val=i*portion
                   self.progressbar.setValue(val)
                   self.labelfile.setText(file)
                   eachfiledir=dir+r"/"+file
                   importdoc.subopendoc(eachfiledir, dirdes)
                self.progressbar.setVisible(False)
                self.labelfile.setVisible(False)
        print("--- %s seconds ---" % (time.time() - start_time))

    # It saves The HTML document in the webview element in the main form.
    # (It may user edit the HTML document and want to save it.)
    def Savehtmlf(self):
        start_time = time.time()
        dirdes= importdoc.directorydestination()
        filename=QFileDialog.getSaveFileName(self, caption="Save as HTML", directory=dirdes , filter="Text files (*.html)")
        dir=filename
        content=self.webView.page().mainFrame().toHtml()
        if (dir!=''):
            importdoc.SfileHTML(dir, content)
        print("--- %s seconds ---" % (time.time() - start_time))

    # It lets user edit the HTML code in webview of the main form by a double click.
    # A user can disable the edit mode.
    def editwebweiw(self,event):
        if (self.webView.page().isContentEditable()):
            self.webView.page().setContentEditable(False)
        else:
            self.webView.page().setContentEditable(True)

    # It calls the related form for editing the imported HTML code.
    def editHtmlshow(self):
        content=self.webView.page().mainFrame().toHtml()
        self.main = Htmledit.Maindailog(self, str(content))
        self.main.show()

    # It helps a user to export a JSON-LD file.
    def choosedatasetref(self):
        self.main = Choose_Datasetrefrences.Maindailog(self)
        self.main.show()

    # It harvests information of datasets in dara (doi_titles)
    def harvestdata(self):
        harvestor.collection()


app= QApplication(sys.argv)
dialog= MainClass()
dialog.show()
app.exec_()