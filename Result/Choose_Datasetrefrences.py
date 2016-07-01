# a user selects correct suggested candidates made by our approach

import os
from PyQt4.QtGui import *
from Result import UI_SelectDatasets

class Maindailog(QMainWindow, UI_SelectDatasets.Ui_Dialog):
    def __init__(self,parent):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.pa=parent
        self.assigncombobox()

    # It put the names of all papers which are analyzed by our approach previously.
    def assigncombobox(self):
        lsnamedir=[x[0].replace('lists_files/SSuggested_Candidate/','') for x in os.walk("lists_files/SSuggested_Candidate/")]
        self.combo.addItems(lsnamedir)



