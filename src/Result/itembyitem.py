import os

import nltk
from PyQt4.QtGui import *

from Result import UI_demostrate_itembyitem
from html_and_doc_handler import htmlparserb
from similarity_cos_tf_idf import combinedapproach as combinedapproach_instance
combinedapproach=combinedapproach_instance.combinedapproach_class()
from similarity_cos_tf_idf import  tf_final as tf_final_instance
tf_final=tf_final_instance.tf_final_class()

class Maindailog(QMainWindow, UI_demostrate_itembyitem.Ui_Dialog1):
    def __init__(self,parent,wbwtext,txtlable):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.pa=parent
        self.wbw(wbwtext,txtlable)
        self.assigncombobox(txtlable)
        self.indexsearch=0
        self.textparentwebveiw=wbwtext
        self.labelll=txtlable
        self.pushButton_2.clicked.connect(self.nextquery)
        self.Mainfun()

    # find the next dataset refrence.
    def nextquery(self):
        if UI_demostrate_itembyitem.indexsearch== 'change':
            self.indexsearch=0
            UI_demostrate_itembyitem.indexsearch= 'unchange'
        txtlable= self.labelll.replace('.html','')
        filelisttxtinnewdir = [ f for f in os.listdir('.\lists_files\Testlog2\\'+txtlable) if f.endswith(".txt") ]
        listoffile=[]
        for item in filelisttxtinnewdir:
            if self.combo.currentText() in item:
                listoffile.append(item)
        if self.indexsearch<len(listoffile)-1:
            self.indexsearch+=1
        else:
            self.indexsearch=0
        self.Mainfun()

    def wbw(self,str1,txtlable):
           self.webView.setHtml(str1)
           txtlable=txtlable.replace('.html','')
           self.labelfile.setText("File Name: "+txtlable)

    # list of special features detected in a paper
    def assigncombobox(self,txtlable):
        txtlable=txtlable.replace('.html','')
        filelisttxtinnewdir = [ f for f in os.listdir('.\lists_files\Testlog2\\'+txtlable) if f.endswith(".txt") ]
        lsofabb=[]
        for item in filelisttxtinnewdir:
            item1=item.split('_')
            lsofabb.append(item1[0])
        lsofabb=list(set(lsofabb))
        self.combo.addItems(lsofabb)

    # It makes the current dataset refrence highlighted.
    def search(self):
        text=self.textparentwebveiw
        query=self.combo.currentText()
        self.webView.setStyleSheet("selection-background-color: GreenYellow")
        self.webView.findText(query)
        txt=self.webView.selectedText()
        os.system('cls')
        print('Selected Text: '+str(txt))

    def readtoarr2(self,str):
        with open(str, "r", encoding="utf-8") as f:
            mylist = list(f)
        fl=[]
        for item in mylist:
            item=item.rstrip('\n')
            fl.append(item)
        return  fl

    def Mainfun(self):
        self.webView.findText('')
        self.webView.selectedText()
        txtlable=self.labelll.replace('.html','')
        filelisttxtinnewdir = [ f for f in os.listdir('.\lists_files\Testlog2\\'+txtlable) if f.endswith(".txt") ]
        lsofnewuabb=[]
        content=self.webView.page().mainFrame().toHtml()
        parser = htmlparserb.MyHTMLParser()
        parser.ls=[]
        parser.reset()
        parser.feed(content)
        tls=[]
        for item in parser.ls:
            tls.append(item)


        for itmem in filelisttxtinnewdir:
            tmitem=itmem.split('_')
            if tmitem[0]==self.combo.currentText():
                lsofnewuabb.append(tmitem[1])



        content1=self.webView.page().mainFrame().toHtml()
        ls= htmlparserb.content(content1)
        ls1=self.readtoarr2("lists_files/Testlog2/"+txtlable+"/"+self.combo.currentText()+"_"+lsofnewuabb[self.indexsearch])
        item1=ls1[2].replace('TExT:','')
        tokens=nltk.word_tokenize(item1)
        contextwithalldetail=''
        for itms in ls:
            flag=0
            for itokens in tokens:
                if not (combinedapproach.sep_checK(itokens, itms.lower())):
                    flag=1
                    break

            if flag==0:
                contextwithalldetail=itms
                break
        queryl=[]
        lscontextwithalldetail= tf_final.token(contextwithalldetail)
        fllscontextwithalldetail=[]
        for item in lscontextwithalldetail:
            if self.combo.currentText() in item:
                fllscontextwithalldetail.append(item)
        try:
            lscontextwithalldetail=max(fllscontextwithalldetail, key=len)
        except:
            pass

        for item in tls:
            if self.combo.currentText() in item and item in contextwithalldetail:
                queryl.append(item)

        try:
            query=max(queryl, key=len)
        except:
            query=self.combo.currentText()
        self.webView.setStyleSheet("selection-background-color: GreenYellow")
        query=self.sentancespliter(self.combo.currentText(),query)
        self.webView.findText(query.rstrip())
        txt=self.webView.selectedText()

        txt=''
        idxcounterb=0
        for idx,item in enumerate(ls1):
            if 2<idx and idx<18:
                if idx%3!=0:

                    if idx%3==1:
                        item=item.replace("value:","Consine Similarity Score: ")
                        txt+=item+"\n"
                    else:
                        item=item.replace("TExT:","Title: ")
                        txt+=item+"\n\n"
                else:
                    idxcounterb+=1
                    txt+=str(idxcounterb)+".\n"
        txt+="\n\n\n\n\n\n\n\n The Selected Sentences Without Punctuation Marks:\n"+ls1[2]
        self.plainTextEdit.setPlainText(txt)



    def sentancespliter(self,spf,query):
        ls=query.split('. ')
        lstemp=[]
        for item in ls:
            ls1=item.split(';')
            for item1 in ls1:
                lstemp.append(item1)

        for item in lstemp:
            if spf in item:
                return item





