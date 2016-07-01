# The file is for editing an HTML document.
# Its user interface is "Htmleditorui.py"
from PyQt4.QtGui import *
from html_and_doc_handler import Htmleditorui


class Maindailog(QMainWindow, Htmleditorui.Ui_MainWindow):
    def __init__(self,parent,content=""):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.close)
        self.plainTextEdit.setPlainText(content)
        self.pushButton_3.clicked.connect(self.apply)
        self.pa=parent
        self.pushButton.clicked.connect(self.search)
        self.indexsearch=0

    # It applies changes into webwiev of the main form.
    def apply(self):
        self.pa.webView.setHtml(self.plainTextEdit.toPlainText())
        self.close()

    # It searches a query (piece of code) in the HTML code.
    def search(self):
        text=self.plainTextEdit.toPlainText().lower()
        query=self.lineEdit.text().lower()
        if(text.find(query,self.indexsearch)==-1):
            self.indexsearch=0
        index=self.indexsearch
        index=text.find(query,index)
        if (index!=-1):
            lenght=len(query)
            end=index+lenght
            cursor = self.plainTextEdit.textCursor()
            cursor.setPosition(index)
            cursor.setPosition(end,QTextCursor.KeepAnchor)
            self.plainTextEdit.setTextCursor(cursor)
            self.plainTextEdit.setStyleSheet("selection-background-color: yellow")
            self.plainTextEdit.textCursor().selectedText()
            self.indexsearch=index+1
        else:
            self.indexsearch=0



