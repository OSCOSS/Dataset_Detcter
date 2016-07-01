import re
import nltk
from lists_files import lsarray1
from similarity_cos_tf_idf import cosine_tf as cosine_tf_instance
cosine_tf=cosine_tf_instance.cosine_tf_class()
from similarity_cos_tf_idf import aux_functions as aux_fun
auxfun=aux_fun.auxfunclass

class tf_final_class:
    def sepfinder(self,abb,ls):
        punc= lsarray1.Punctuation + lsarray1.Punctuation1 + lsarray1.Punctuation2 + ["I"] + [" "]
        list1=[]
        list2=[]
        for item1 in abb:
            for item in ls:
                if item1 in item:
                    index=item.find(item1)
                    lent=len(item1)
                    if item[index+lent:index+lent+1] in punc or item[index+lent:index+lent+1].isdigit():
                        if item.find(item1)==0:
                            list1.append(item)
                            list2.append(item1)
                        elif item[index-1:index] in punc:
                            list1.append(item)
                            list2.append(item1)
                    elif index+lent==len(item):
                        if item.find(item1)==0:
                            list1.append(item)
                            list2.append(item1)
                        elif item[index-1:index] in punc:
                            list1.append(item)
                            list2.append(item1)
        return list1,list2

    def titleindara_abb(self,abb):
                lsttemp1=[]
                for item in abb:
                    lsttemp1.append(item)
                    lsttemp1.append(item.upper())
                abb=list(set(lsttemp1))
                titles= auxfun.readtoarr2(auxfun,'lists_files/title1.txt')
                list1=[]
                list2=[]
                punc= lsarray1.Punctuation + lsarray1.Punctuation1 + lsarray1.Punctuation2 + ["I"] + [" "]

                for item1 in abb:
                    for item in titles:
                        if item1 in item:
                                index=item.find(item1)
                                lent=len(item1)
                                if item[index+lent:index+lent+1] in punc or item[index+lent:index+lent+1].isdigit():
                                    if item.find(item1)==0:
                                        list1.append(item)
                                        list2.append(item1)
                                    elif item[index-1:index] in punc:
                                        list1.append(item)
                                        list2.append(item1)
                                elif index+lent==len(item):
                                    if item.find(item1)==0:
                                        list1.append(item)
                                        list2.append(item1)
                                    elif item[index-1:index] in punc:
                                        list1.append(item)
                                        list2.append(item1)
                return list1,list2

    def sentencize(self,ctxt):
        st=""
        for item in ctxt:
            st=st+" "+str(item)
        ls=self.token(st)
        return ls

    def token(self,txt):
        sent_detector =nltk.data.load('tokenizers/punkt/english.pickle')
        ls=sent_detector.tokenize(txt.strip())
        return ls

    def removerlist(self,item,list):
        for it in list:
            item=item.replace(it," ")
        return item

    def tf_ec(self,query,lssentence,abb_refrence,filename):
        abbinTlist1=[]
        abbinTlist1.append(abb_refrence)
        lts1,lst2=self.titleindara_abb(abbinTlist1)
        puli= lsarray1.Punctuation2 + lsarray1.Punctuation1 + lsarray1.Punctuation
        puli=list(set(puli))
        inputsenteces=[]
        inputsenteces=inputsenteces+lssentence
        listsentb=self.sentencize(inputsenteces)
        listsentbi=[]
        for itemsen in listsentb:
            listsentbi.append(self.removerlist(itemsen,puli))
        timeloc= cosine_tf.maintask(listsentbi, self.removerlist(query, puli), filename, abb_refrence, lts1)
        return timeloc

    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False


    def querysplitter(self,query,abb_refrence):
        lssplits=[]
        if query.count(abb_refrence)>1:
                listofindexs=[m.start() for m in re.finditer(abb_refrence, query)]
                tlsmp=nltk.word_tokenize(query)
                lentofindex=len(listofindexs)
                for i in range(lentofindex):
                    if i+1<=lentofindex-1:
                        start=listofindexs[i]
                        end=listofindexs[i+1]
                        substr=query[start:end]
                        risf=substr.rfind('.')
                        if risf==-1:
                                lssplits.append(query)
                        else:
                            endofsubstr=start+risf+1
                            str1=query[:endofsubstr]
                            str2=query[endofsubstr+1:]
                            lssplits.append(str1)
                            lssplits.append(str2)
        else:
                lssplits.append(query)
        return lssplits




