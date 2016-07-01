# -*- coding: utf-8 -*-
# The user interface of the form which shows datasets refrences to a user item by item.
# It handles per-dataset_refrence flow

from PyQt4 import QtCore, QtGui
from PyQt4 import QtWebKit

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

indexsearch='unchange'

class Ui_Dialog1(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1057, 544)
        self.webView = QtWebKit.QWebView(Dialog)
        self.webView.setGeometry(QtCore.QRect(20, 80, 531, 441))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.plainTextEdit = QtGui.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(570, 80, 471, 441))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.labelfile=QtGui.QLabel(Dialog)
        self.labelfile.setObjectName(_fromUtf8("lablefile"))
        self.labelfile.setText("")
        self.labelfile.setGeometry(QtCore.QRect(20, 520, 471, 18))
        self.labellist=QtGui.QLabel(Dialog)
        self.labellist.setObjectName(_fromUtf8("labellist"))
        self.labellist.setText("List of Special Features in the Paper:")
        self.labellist.setGeometry(QtCore.QRect(20, 0, 350, 20))
        self.combo = QtGui.QComboBox(Dialog)
        self.combo.setObjectName(_fromUtf8("COMBOBOX1"))
        self.combo.setGeometry(QtCore.QRect(20, 20, 350, 20))
        QtCore.QObject.connect(self.combo,QtCore.SIGNAL("currentIndexChanged(int)"), self.Tabmaker)
        self.Overviewofpaper=QtGui.QLabel(Dialog)
        self.Overviewofpaper.setObjectName(_fromUtf8("Overviewofpaper"))
        self.Overviewofpaper.setText("The Imported Paper (Highlighted Part: Refrence to Dataset):")
        self.Overviewofpaper.setGeometry(QtCore.QRect(20, 55, 350, 20))
        self.Rankedlist=QtGui.QLabel(Dialog)
        self.Rankedlist.setObjectName(_fromUtf8("Rankedlist"))
        self.Rankedlist.setText("The Ranked list of Dataset Titles:")
        self.Rankedlist.setGeometry(QtCore.QRect(570, 55, 350, 20))
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(380, 15, 200, 35))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Check Detected Refrences in the Imported Paper (Item by Item)", None))
        self.pushButton_2.setText(_translate("Dialog", "Next Dataset Refrence in the Paper>>\n(Based on the Selected Features)", None))

    # index of datasets refrences (related to a special feature) in a paper.
    def Tabmaker(self):
        indexsearch='change'


