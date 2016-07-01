import re
from lists_files import lsarray1 as lsarray
import nltk
import enchant
from nltk.corpus import wordnet

class abb_extractor_class:
    # It removes punctuation marks
    def rmovepu(self,item):
        puli=lsarray.Punctuation2+lsarray.Punctuation1+lsarray.Punctuation
        puli=list(set(puli))
        puli.remove(')')
        if item[-1] in puli:
            return item[:-1]
        return item

    # It takes a text file and then, it puts each line into an item on the output list.
    # It removes punctuation marks as well.
    def readtoarr2(self,str='lists_files/title1.txt'):
        with open(str, "r", encoding="utf-8") as f:
             mylist = list(f)
        fl=[]
        for item in mylist:
            item=item.rstrip('\n')
            if str=='title.txt':
                item=self.rmovepu(item)
            fl.append(item.rstrip())
        return  fl

    # It takes a text file and then, it puts each line into an item on the output list.
    def readtoarr21(self,str='title.txt'):
        with open(str, "r", encoding="utf-8") as f:
             mylist = list(f)
        fl=[]
        for item in mylist:
            item=item.rstrip('\n')
            if str=='title.txt':
                item=self.rmovepu(item)
            item=item.lower()
            fl.append(item.rstrip())
        return  fl

    # It apples a pre-processing on titles
    def Preproccess(self,titleraw):
        ls=[]
        for item in titleraw:
            listitem=item.split(':')
            ls.append(listitem[0].rstrip())
        return ls

    # is a value float?
    def isfloat(self,var):
        try:
              return float(var)
        except:
                return False

    def restofabb(self,txt):
        txt1=''.join(e for e in txt if e.isalnum())
        txt2= ''.join([i for i in txt1 if not i.isdigit()])
        if len(txt1)>2:
            if len(txt2)>0:
                if not txt2[1:].islower() and not self.isfloat(txt1) and not self.isfloat(txt1[0]):
                    return txt
                else:
                    return 'false'
            else:
                return 'false'
        else:
            return 'false'

    # Items in parentheses
    def btwparenthese(self,s):
        puli=lsarray.Punctuation2+lsarray.Punctuation1+lsarray.Punctuation
        labb=[]
        ls=(re.findall('\(.*?\)',s))
        for item in ls:
            item=item.replace('(',' ')
            item=item.replace(')',' ')
            count=0
            mp=''
            wordsp=nltk.word_tokenize(item)
            try:
                if wordsp[-1] in puli:
                    del wordsp[-1]
                if wordsp[0] in puli:
                     del wordsp[0]
            except:
                pass
            for item1 in wordsp:
                count=count+1
                mp=item1
            if count==1:
                labb.append(mp)
        return labb


    def isnumbertester(self,item):
        txt1=''.join(e for e in item if e.isalnum())
        if self.isfloat(txt1)!=False:
            return True
        else:
            return False


    def abbgenrator2(self,ls):
        ls0=[]
        for itts in ls:
            for item in self.btwparenthese(itts):
                if not self.isnumbertester(item):
                    ls0.append(item.rstrip())
        ls0=list(set(ls0))
        return ls0

    def tokensfilter(self,ls):
        ls1=[]
        ls2=[]
        for item in ls:
            for item1 in nltk.word_tokenize(item):
                if self.restofabb(item1)!='false':
                    ls1.append(item1.rstrip())
            leftpr=item.split('(')
            dashlist=item.split('-')
            if len(leftpr)>1 and len(nltk.word_tokenize(leftpr[0]))==1:
                ls2.append(leftpr[0].rstrip())
            if len(dashlist)>1 and len(nltk.word_tokenize(dashlist[0]))==1:
                ls2.append(dashlist[0].rstrip())
        return ls2,ls1

    def filterdirtyelm(self,ls):
        list1=[]
        for item in ls:
            if self.isfloat(item[0]):
                pass
            else:
                list1.append(item.rstrip())
        return list1

    def cleanlist(self,listofabbd):

        puli=lsarray.Punctuation2+lsarray.Punctuation1+lsarray.Punctuation

        for idx,item in enumerate(listofabbd):
            if item[-1] in puli:
                listofabbd[idx]=item[:-1]
            if item[0] in puli:
                listofabbd[idx]=item[1:]

            matchpatern = re.search(r"^((\/|X|I|V|-)+$|^(\/|x|i|v|-)+)$", item)
            if matchpatern:
                matchsubstring=matchpatern.group()
            else:
                matchsubstring=''

            if matchsubstring and len(item)==len(matchsubstring):
                    listofabbd.remove(item)
        listofabbd=list(set(listofabbd))

        return listofabbd

    def newspliteritem(self,ls):
        ls1=[]
        for item in ls:
            ditem=item.split('-')
            Ulitem=item.split('_')
            slitem=item.split('/')
            doitem=item.split('.')
            for item1 in ditem:
                if self.restofabb(item1)!='false':
                    ls1.append(item1.rstrip())
            for item1 in Ulitem:
                if self.restofabb(item1)!='false':
                    ls1.append(item1.rstrip())
            for item1 in slitem:
                if self.restofabb(item1)!='false':
                    ls1.append(item1.rstrip())
            if self.restofabb(doitem[0].rstrip())!='false':
                ls1.append(doitem[0].rstrip())
            ls1.append(item.rstrip())
        ls1=list(set(ls1))
        return ls1

    def filterpunt(self,ls):
        puli=puli=lsarray.Punctuation2+lsarray.Punctuation1+lsarray.Punctuation+['’']
        puli=list(set(puli))
        puli=list(set(puli)-set([".","-","/","*","&",":"]))
        ls1=[]
        for item in ls:
             if len(list(set(puli).intersection(set(item))))>0:
                pass
             else:
                    ls1.append(item.rstrip())
        return ls1

    def checklowercase_exceptfirst(self,ls):
        ls1=[]
        for item in ls:
            if not (item[1:].islower()):
                ls1.append(item.rstrip())
        return ls1

    def dashslashlowerpart(self,ls):
        ls1=[]
        for item in ls:
            flag=0
            if '-' in item:
                dashlist=item.split('-')
                for item1 in dashlist:
                    if item1[1:].islower() or self.isfloat(item1):
                        flag=1
            if '/' in item:
                dashlist=item.split('/')
                for item1 in dashlist:
                    if item1[1:].islower() or self.isfloat(item1):
                        flag=1


            if flag==0:
                 ls1.append(item.rstrip())
        return list(set(ls1))

    # It checks if an item has a definition or not (En and De).
    def dicpr(self,item,dicen,gls,dicge):
        member2=item.lower()
        definition=wordnet.synsets(member2)
        if not definition and not (dicen.check(member2)) and not (dicge.check(member2)) and not(member2 in gls):
            return True
        else:
            return False

    def restofabbapplier(self,newlst,dicen,gls,dicge):
        cleannonabb=[]
        for item in newlst:
            item=item.rstrip()
            if self.restofabb(item)!='false':
                cleannonabb.append(item)
            else:
                if self.dicpr(item,dicen,gls,dicge):
                    cleannonabb.append(item)
        return cleannonabb

    # It removes names of countries.
    def countremover(self,encount,decount,cleannonabb):
        countries=list(set(encount+decount))
        for idx,item in enumerate(cleannonabb):
            item=item.rstrip()
            for item1 in countries:
                item1=item1.rstrip()
                if item1.lower()==item.lower():
                    del cleannonabb[idx]
        return cleannonabb

    # It write items on a list into the rows of a file.
    def filewriter(self,ls2,fn):
        f = open(fn,'wb')
        endidx=len(ls2)-1
        for idx,item in enumerate(ls2):
            if idx!=endidx:
                item=item+u"\n"
            else:
                item=item
            f.write(item.encode('UTF-8'))
        f.close()

    # If it is all in capital, then It will be converted into lowercase.
    def makelowerifcapital(self,ls):
        ls1=[]
        for txt in ls:
            txt1=''.join(e for e in txt if e.isalnum())
            txt2= ''.join([i for i in txt1 if not i.isdigit()])
            if txt2.isupper():
                ls1.append(txt.lower())
            else:
                ls1.append(txt)
        return ls1

    def main(self):
        listoftitle=self.readtoarr2()
        listoftitle=self.makelowerifcapital(listoftitle)
        listoftitle=self.Preproccess(listoftitle)
        fwitemlist,Notlowecaselist=self.tokensfilter(listoftitle)
        abb_level1=list(set(Notlowecaselist))
        abb_level1=self.filterdirtyelm(abb_level1)
        abb_level1=list(set(abb_level1+fwitemlist))
        abb_level1=self.filterpunt(abb_level1)
        abb_level1=self.dashslashlowerpart(abb_level1)
        dicen=enchant.Dict("en_US")
        gls=self.readtoarr21('Harvester_abbandphraseGenerator/german.dic')
        dicge = enchant.Dict('de_DE')
        encount=self.readtoarr21('Harvester_abbandphraseGenerator/germancount.txt')
        decount=self.readtoarr21('Harvester_abbandphraseGenerator/Country-List.txt')
        abb_level1=self.countremover(encount,decount,abb_level1)
        abb_level1=self.restofabbapplier(abb_level1,dicen,gls,dicge)
        abb_level1=self.cleanlist(abb_level1)
        extaddition=list(set(self.readtoarr2('Harvester_abbandphraseGenerator/ExtraAbbMan.txt')))
        Finallist1=abb_level1
        Finallist=list(set(Finallist1+extaddition))
        FPList=self.readtoarr2('Harvester_abbandphraseGenerator/False_abb_Phrase.txt')
        Finallist=list(set(Finallist)-set(FPList))
        self.filewriter(Finallist,'lists_files/listofabb.txt')



