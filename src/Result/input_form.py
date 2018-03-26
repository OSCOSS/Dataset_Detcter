from PyQt4.QtGui import *
from Result import input_form_ui
import metadata_parser
import json

class Maindailog(QMainWindow, input_form_ui.Ui_Dialog):
    def __init__(self,parent,textfile,lisofentity):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.mainfun)
        self.filename=textfile
        self.lsoftitile=lisofentity

    def mainfun(self):
        SSOAR_ID=self.lineEdit.text()
        if SSOAR_ID!='':
            doc=json_makerr(self.lsoftitile,SSOAR_ID)
            with open('lists_files/Json/'+SSOAR_ID+'.json', 'w') as outfile:
                    #json_data = json.dumps(doc, sort_keys=True , indent=1,)
                    json.dump(doc, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
                    #json.dump(json_data, outfile, ensure_ascii=False)
            self.close()

# some metadata and a parser for extracting information from SSOAR
def Metadata(url):
        page = metadata_parser.MetadataParser(url)
        metadata_fields = {
         "description" :page.metadata.get('meta').get('DC.description'),
        "titlealt" : page.metadata.get('meta').get('DCTERMS.alternative'),
        "titlede" :page.metadata.get('meta').get('DC.title'),
        "type" : page.metadata.get('meta').get('DC.type'),
        "author" : page.metadata.get('meta').get('DC.creator'),
        "subject" : page.metadata.get('meta').get('DC.subject'),
        "issued" : page.metadata.get('meta').get('DCTERMS.issued'),
        "language" : page.metadata.get('meta').get('DC.language'),
        "identifier" : page.metadata.get('meta').get('DC.identifier'),
        "publisher" : page.metadata.get('meta').get('DC.publisher')
             }
        return metadata_fields

# The structure of output JSON file
def json_makerr(lsoftitile,docid):
    docurl = "http://www.ssoar.info/ssoar/handle/document/"+docid
    metadata = Metadata(docurl)
    list_of_datasets=listdatacreator(lsoftitile)

    doc = { "@context": "http://schema.org",
            "@type": "ScholarlyArticle",
            "description": metadata["description"],
            "headline": metadata["titlede"],
            "alternativeHeadline": metadata["titlealt"],
            "author": metadata["author"],
            "inLanguage": metadata["language"],
            "datePublished": metadata["issued"],
            "publisher": metadata["publisher"],
            "sameAs": "http://nbn-resolving.de/"+metadata["identifier"],
            "citation": list_of_datasets
        }

    return doc

# list of dataset selected by a user.
def listdatacreator(lsoftitile):
    flist=[]
    for item in lsoftitile:
        temp={}
        templist=[]
        temp["@type"]="Dataset"
        for idx,item1 in enumerate(item):
            if idx==0:
                temp["headline"]=item1
            else:
                templist.append("https://doi.org/"+item1)
        temp["sameAs"]=templist
        flist.append(temp)
    return flist
