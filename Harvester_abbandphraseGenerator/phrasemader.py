import re
import os
import enchant
import nltk
from nltk.corpus import wordnet
import lists_files.lsarray as lsarray

class phrasegenrator_class:
    # It removes punctuation marks
    def rmovepu(self,item):
        puli= lsarray.Punctuation2 + lsarray.Punctuation1 + lsarray.Punctuation
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
            if str=='lists_files/title1.txt':
                item=self.rmovepu(item)
            fl.append(item)
        return  fl

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

    # For the first type of special phrase (e.g. "studie" in "Lebensverlaufsstudie")
    def pharseispartof(self,item,listpd):
        listoftoken=nltk.word_tokenize(item)
        nl=[i for e in listpd for i in listoftoken if e.lower() in i.lower()]
        return nl

    # It removes items which are exactly same as items in the dictionary of phrases.
    #  (.\Harvester_abbandphraseGenerator\dicphrase.txt)
    def deleteflistbycon(self,listofpharse,item):
        item=item[0].upper()+item[1:]
        item1=item+'s'
        item2=item+'es'
        item3=item+'ing'
        item4=item+'en'
        if item in listofpharse:
               listofpharse.remove(item)
        if item.lower() in listofpharse:
               listofpharse.remove(item.lower())
        if item.title() in listofpharse:
               listofpharse.remove(item.title())

        if item1 in listofpharse:
               listofpharse.remove(item1)
        if item1.lower() in listofpharse:
               listofpharse.remove(item1.lower())
        if item1.title() in listofpharse:
               listofpharse.remove(item1.title())

        if item2 in listofpharse:
               listofpharse.remove(item2)
        if item2.lower() in listofpharse:
               listofpharse.remove(item2.lower())
        if item2.title() in listofpharse:
               listofpharse.remove(item2.title())

        if item3 in listofpharse:
               listofpharse.remove(item3)
        if item3.lower() in listofpharse:
               listofpharse.remove(item3.lower())
        if item3.title() in listofpharse:
               listofpharse.remove(item3.title())

        if item4 in listofpharse:
               listofpharse.remove(item4)
        if item4.lower() in listofpharse:
               listofpharse.remove(item4.lower())
        if item4.title() in listofpharse:
               listofpharse.remove(item4.title())

        return listofpharse

    # It removes punctuation marks from the first and last of strings.
    def cleanitems(self,item):
        puli= lsarray.Punctuation2 + lsarray.Punctuation1 + lsarray.Punctuation
        puli=list(set(puli))
        if item[-1] in puli:
            item=item[:-1]
        if item[0] in puli:
            item=item[1:]
        return item

    def isextrachecker(self,item):
        puli= lsarray.Punctuation2 + lsarray.Punctuation1 + lsarray.Punctuation
        puli=list(set(puli))
        newstring = ''.join(ch for ch in item if ch not in puli)
        if len(newstring)<2:
            return True
        else:
            newstring=newstring.lower()
            newstring1=newstring.replace('th','')
            if self.isdigit1(newstring1):
                return True
        return False

    # It is for the second type of special phrases (e.g. "Poll in ""Accident Poll")
    def secondphrasegenrator(self,listofdic,item,dicen,gls,dicge):
        stpwww= lsarray.stopwdde + lsarray.stopwd + lsarray.stopwd0 + lsarray.stopwd1 + lsarray.stopwd2 + lsarray.stopwd3 + lsarray.stopwd4 + lsarray.stopwd5 + lsarray.stopwd6
        stpwww=list(set(stpwww))
        listoftoken=nltk.word_tokenize(item)
        puli= lsarray.Punctuation2 + lsarray.Punctuation1 + lsarray.Punctuation
        puli=list(set(puli))
        for item1 in listoftoken:
           for item2 in listofdic:
            if item1.lower()==item2.lower():
                lisind=listoftoken.index(item1)
                if lisind!=0:
                    if not (listoftoken[lisind-1] in puli) and not (listoftoken[lisind-1].lower() in stpwww) and not (listoftoken[lisind-1].lower() in lsarray.orderlist) and not (self.isdigit1(listoftoken[lisind-1])) and not (self.isextrachecker(listoftoken[lisind-1])) and not (listoftoken[lisind-1].lower() in lsarray.extraword1):
                        if self.dicpr(listoftoken[lisind-1],dicen,gls,dicge):
                            txt=listoftoken[lisind-1]+' '+listoftoken[lisind].lower()
                            return True,txt
                        else:
                            txt=listoftoken[lisind-1].lower()+' '+listoftoken[lisind].lower()
                            return True,txt
        return False,''

    def isdigit1(self,firstrest):
        try:
            float(firstrest)
            return True
        except ValueError:
            return False

    # It is for the third type of special phrases (e.g. "Survey Of Eyewitness")
    def thirdphrasegenerator(self,item):
        nitem=''
        stpwww= lsarray.stopwd + lsarray.stopwd0 + lsarray.stopwd1 + lsarray.stopwd2 + lsarray.stopwd3 + lsarray.stopwd4 + lsarray.stopwd5 + lsarray.stopwd6
        stpwww=list(set(stpwww))
        try:
            if 'Survey of' in item:
                listoftoken1=nltk.word_tokenize(item)
                item1=item.lower()
                id=item1.index('survey of')+len('survey of')
                idx=item1.index('survey of')
                rest=item[id:]
                reslist=nltk.word_tokenize(rest)
                firstrest=reslist[0]
                nitem=item[idx:idx+len('survey of')]+' '+firstrest
                if firstrest.lower() in stpwww or firstrest.lower() in lsarray.extraword1:
                    return False,''
                elif self.isdigit1(firstrest):
                    return False,''
                else:
                    return True,nitem

            elif 'Study of' in item:
                listoftoken1=nltk.word_tokenize(item)
                item1=item.lower()
                id=item1.index('study of')+len('study of')
                idx=item1.index('study of')
                rest=item[id:]
                reslist=nltk.word_tokenize(rest)
                firstrest=reslist[0]
                nitem=item[idx:idx+len('study of')]+' '+firstrest
                if firstrest.lower() in stpwww or firstrest.lower() in lsarray.extraword1:
                    return False,''
                elif self.isdigit1(firstrest):
                    return False,''
                else:
                    return True,nitem
        except:
            pass
        return False,''

    # It checks if a token has a definition or not.
    def dicpr(self,item,dicen,gls,dicge):
        member2=item.lower()
        definition=wordnet.synsets(member2)
        if not definition and not (dicen.check(member2)) and not (dicge.check(member2)) and not(member2 in gls):
            return True
        else:
            return False

    def lastcleaner1(self,lst,phrasedic):
        lst1=[]
        for item in lst:
            flag=0
            matchpatern = re.search('[0-9][a|b]$',item)
            if matchpatern:
                matchsubstring=matchpatern.group()
            else:
                matchsubstring=''
            if matchsubstring!='':
                flag=1
            for item2 in phrasedic:
                item1_0=item2.lower()+'n'
                item1_1=item2.lower()+'s'
                item1_2=item2.lower()+'es'
                item1_3=item2.lower()+'ing'
                item1_4=item2.lower()+'en'
                item1_5=item2.lower()+'e'
                item1_6=item2.lower()
                if item.lower()==item1_0 or item.lower()==item1_1 or item.lower()==item1_2 or item.lower()==item1_3 or item.lower()==item1_4 or item.lower()==item1_5 or item.lower()==item1_6:
                    flag=1
                #if item2.lower()=='poll' and item2.lower() in item:
                #    if not (item.endswith(item2)):
                #       flag=1
                renp=item.replace(item2,'')
                if self.isdigit1(renp):
                     flag=1
                if renp.lower() in lsarray.extraword1:
                    flag=1
            if flag==0:
                lst1.append(item)
        return lst1

    # It updates Special phrases list by removing items on false positive list.
    def updatepharselist(self):
        listofpharse=self.readtoarr2('lists_files/listofPhrase.txt')
        FPList=self.readtoarr2('Harvester_abbandphraseGenerator/False_abb_Phrase.txt')
        listofpharse=list(set(listofpharse)-set(FPList))
        self.filewriter(listofpharse,'lists_files/listofPhrase.txt')

    def Make_first_letter_upper(self,lst):
        lst1=[]
        for item in lst:
            item1=item.title()
            lst1.append(item1)

        return lst1

    # last check to avoid any mistake.
    def prunephrasefromlist_checkbytitle(self,lstofphrase):
        titleraw=self.readtoarr2()
        lsnewitem=[]

        for item1 in lstofphrase:
            flag=0
            for item in titleraw:
                if item1.lower() in item.lower():
                    flag=1
                    break
            if flag==1:
                lsnewitem.append(item1)
        return lsnewitem

    def phrasemain(self):
        os.system('cls')
        titleraw=self.readtoarr2()
        phrasedic=self.readtoarr2('Harvester_abbandphraseGenerator/dicphrase.txt')
        print('[#####Phrase generating######]10%')
        listofpharse=[]
        listofpharse0=[]
        listofpharse01=[]
        dicen=enchant.Dict("en_US")
        gls=self.readtoarr2('Harvester_abbandphraseGenerator/german.dic')
        dicge = enchant.Dict('de_DE')
        print('[#####Phrase generating######]20%')
        for item in titleraw:
            lpn=self.pharseispartof(item,phrasedic)
            flag,candidate=self.secondphrasegenrator(phrasedic,item,dicen,gls,dicge)
            flag1,candidate1=self.thirdphrasegenerator(item)
            if flag1:
                listofpharse01.append(candidate1)
            if flag:
                listofpharse0.append(candidate)
            for item1 in lpn:
                listofpharse.append(item1)
        print('[#####Phrase generating######]40%')
        listofpharse0=list(set(listofpharse0))
        listofpharse01=list(set(listofpharse01))
        listofpharse=list(set(listofpharse+listofpharse0+listofpharse01))

        listofpharse1=[]
        for item in listofpharse:
            item=self.cleanitems(item)
            listofpharse1.append(item)
        print('[#####Phrase generating######]50%')
        listofpharse1=list(set(listofpharse1))
        listofpharse=listofpharse1

        for item in phrasedic:
            listofpharse=self.deleteflistbycon(listofpharse,item)
        print('[#####Phrase generating######]60%')
        listofpharse=self.lastcleaner1(listofpharse,phrasedic)

        FPList=self.readtoarr2('Harvester_abbandphraseGenerator/False_abb_Phrase.txt')
        listofpharse=list(set(listofpharse)-set(FPList))
        print('[#####Phrase generating######]65%')
        listofpharse=self.Make_first_letter_upper(listofpharse)
        print('[#####Phrase generating######]85%')
        listofpharse=self.prunephrasefromlist_checkbytitle(listofpharse)
        self.filewriter(listofpharse,'lists_files/listofPhrase.txt')
        print('[#####Phrase generating######]100%')
