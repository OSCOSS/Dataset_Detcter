# -*- coding: utf-8 -*-
# The user interface of the form which help a user to extrat result as a JSON file
# It handles per-characteristic_feature flow

from PyQt4 import QtCore, QtGui
import os
from Result import input_form

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(602, 418)
        self.buttonBox = QtGui.QPushButton(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(375, 372, 100, 22))
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.buttonBox.setText('Export JSON file')
        self.Labell = QtGui.QLabel(Dialog)
        self.Labell.setObjectName(_fromUtf8("Labell"))
        self.Labell.setGeometry(QtCore.QRect(20, 350, 350, 25))
        self.Labell.setText("Please select an analyzed paper:")
        self.combo = QtGui.QComboBox(Dialog)
        self.combo.setObjectName(_fromUtf8("COMBOBOX1"))
        self.combo.setGeometry(QtCore.QRect(20, 372, 350, 25))
        QtCore.QObject.connect(self.combo,QtCore.SIGNAL("currentIndexChanged(int)"), self.Tabmaker)
        self.Labell = QtGui.QLabel(Dialog)
        self.Labell.setObjectName(_fromUtf8("Labell"))
        self.Labell.setGeometry(QtCore.QRect(10, 0, 350, 25))
        self.Labell.setText("Tabs' titles represent detected features in the selected paper.")
        self.Labell = QtGui.QLabel(Dialog)
        self.Labell.setObjectName(_fromUtf8("Labell"))
        self.Labell.setGeometry(QtCore.QRect(10, 15, 600, 25))
        self.Labell.setText("Each tab contains a list of suggested datasets' titles in the paper.(Related to a special features) ")
        self.tabs= QtGui.QTabWidget(Dialog)
        self.tabs.setObjectName(_fromUtf8("tabs"))
        self.tabs.setGeometry(QtCore.QRect(0, 40, 600, 310))
        self.tabs.show()
        self.buttonBox.clicked.connect(self.exportJSONfile)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def exportJSONfile(self):
        lsoftitile=[]
        tabsnumber=self.tabs.count()
        icountxx=0
        while icountxx<tabsnumber:
            try:
                childern=self.tabs.widget(icountxx).children()
                for item in childern:
                    if item.isChecked():
                        lsoftitile.append(item.text())
            except:
                pass
            icountxx+=1
        os.system('cls')
        lsoftitile=self.add_doi(self.readtoarr("lists_files/title1.txt"),lsoftitile)
        if len(lsoftitile)!=0:
                self.main = input_form.Maindailog(self,self.combo.currentText(),lsoftitile)
                self.main.show()

    # It gets a text file and puts each row into an item on a list.
    def readtoarr(self,add):
        with open(add, "r", encoding="utf-8") as f:
             mylist = list(f)
        fl=[]
        for item in mylist:
            fl.append(item.rstrip('\n'))
        return  fl

    # It recovers the doi of each title.
    def add_doi(self,lsoftitle,querys):
        flist=[]
        for iteminquerys in querys:
            temlist=[]
            temlist.append(iteminquerys)
            indices = [i for i, x in enumerate(lsoftitle) if x.lower() == iteminquerys]
            doislist=self.readtoarr("lists_files/doi.txt")
            for item in indices:
                temlist.append(doislist[item])
            flist.append(temlist)
        return flist

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Select Datasets' References", None))

    # It gets a text file and puts each row into an item on a list.
    # An exmple of each row -> 3____detroit area study, 1989: political participation in the detroit area____0.176687
    # Three data are separated by '____'. (i.e. 1. The number of occurrences of each title,
    #  2. The title, 3. The similarity score of the title)
    # It extracts the second part (i.e. title)
    def readtoarr2(self,str):
        with open(str, "r", encoding="utf-8") as f:
            mylist = list(f)
        fl=[]
        for item in mylist:
            item=item.rstrip('\n')
            item1=item.split('____')
            fl.append(item1[1])
        return  fl

    # It dynamically adds tabs regarding detected special features.
    def Tabmaker(self):
        textdir=str(self.combo.currentText())
        self.tabs.clear()

        filelisttxtinnewdir = [ f for f in os.listdir('.\lists_files\SSuggested_Candidate\\'+textdir) if f.endswith(".txt") ]
        for idx,item in enumerate(filelisttxtinnewdir):
            itemname=item.replace('.txt','')
            tab1= QtGui.QWidget()
            listitemdataset=self.readtoarr2("lists_files\SSuggested_Candidate\\"+textdir+'\\'+item)
            listitemdataset=listitemdataset[:-1]
            for idx,itemlinetitledatarefrences in enumerate(listitemdataset):
                if idx<10:
                    checkboxt = QtGui.QCheckBox(tab1)
                    checkboxt.setChecked(True)
                    checkboxt.setText(itemlinetitledatarefrences)
                    y=idx*30
                    checkboxt.setGeometry(QtCore.QRect(10, y, 550, 30))
                else:
                    break

            self.tabs.addTab(tab1,itemname)


