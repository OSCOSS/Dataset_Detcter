# The file contains just some auxiliary functions.
# The old name of the file was -> "darapruner.py"
# The name was changed since a lot of functions were removed from the files.

class auxfunclass:
    def __init__(self):
        pass

    def readtoarr(self):
        with open('daraafterprune.txt', "r", encoding="utf-8") as f:
             mylist = list(f)
        fl=[]
        for item in mylist:
            fl.append(item.rstrip('\n'))
        return  fl

    def readtoarr2(self,str):
        with open(str, "r", encoding="utf-8") as f:
             mylist = list(f)
        fl=[]
        for item in mylist:
            fl.append(item.rstrip('\n'))
        return  fl

    def removerlist(self,item,list):
        for it in list:
            item=item.replace(it," ")
        return item