import datetime
import math
import os
import re
from collections import defaultdict
from datetime import date
from operator import itemgetter
import nltk
from gensim import corpora, models, similarities
from lists_files import lsarray1
from similarity_cos_tf_idf import aux_functions as aux_fun
auxfun=aux_fun.auxfunclass

class cosine_tf_class:
    def maintask(self,ctx,queryval,nameidx,abb_refrence,listq):
        list1=ctx
        list2=[]
        for item in list1:
            list2.append(item.lower())
        puli= lsarray1.Punctuation2 + lsarray1.Punctuation1 + lsarray1.Punctuation
        for item in listq:
            item= auxfun.removerlist(auxfun,item, puli)
            list2.append(item.lower())
        query=[]
        qt=queryval
        qt=qt.lower()
        query.append(qt)
        lq=nltk.word_tokenize(qt)
        sq=set(lq)
        list0=[]
        print("tokenize")
        for item in list2:
            sd=set(nltk.word_tokenize(item))
            srf=sq.intersection(sd)
            srf=list(srf)
            if len(srf)!=0:
               list0.append(item)
        list0.append(qt)
        print("start sim calculation")
        timeloc=self.tf_idf_cosine_sim(query,list0,nameidx,abb_refrence,len(listq))
        return timeloc

    def tf_idf_cosine_sim(self,query,list0,nameidx,abb_refrence,lenq):
        documents = list0
        texts = [[word for word in document.lower().split() if word not in lsarray1.stopwdde and word not in lsarray1.stopwd]
                 for document in documents]
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        texts = [[token for token in text if frequency[token] > 1]
                for text in texts]
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        lenofcorp=len(texts)-1
        tfidf = models.TfidfModel(corpus)
        index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.items()))
        new_vec=corpus[lenofcorp]
        sims = index[tfidf[new_vec]]
        finalsimmeasure=[]
        for item in sims:
            finalsimmeasure.append(item)
        strfile=''
        for idx in range(len(finalsimmeasure)):
                strfile=strfile+"index:"+str(idx) + "\nvalue:"+str(finalsimmeasure[idx])+"\nTExT:"+list0[idx]+"\n"
                strfile=strfile
        localtime=datetime.datetime.now().time()
        localtime=str(localtime)
        localtime=localtime.replace(':','').replace('.','')
        directory='lists_files/Testlog2/'+nameidx
        nds='lists_files/Testlog2/'+nameidx+'/'+abb_refrence+'_'+str(localtime)+'.txt'
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open(nds, 'wb')
        f.write(strfile.encode('utf-8'))
        f.close()
        return localtime

    def DAra_No(self,nameidx,abb_refrence,localtime):
            ls= auxfun.readtoarr2(auxfun,'lists_files/Testlog2/' + nameidx + '/' + abb_refrence + '_' + localtime + '.txt')
            endindex=len(ls)/3
            tf=[]
            for i in range (0,int(endindex)):
                df=[]
                i=i*3
                df.append(ls[i].replace('index:',''))
                df.append(ls[i+1].replace('value:',''))
                df.append(ls[i+2].replace('TExT:',''))
                tf.append(df)
            lstitledara= auxfun.readtoarr2(auxfun,'lists_files/title1.txt')
            lstitledara=[x.lower() for x in lstitledara if abb_refrence in x]
            neulist=[]
            puli= lsarray1.Punctuation2 + lsarray1.Punctuation1 + lsarray1.Punctuation
            for item in tf[:-1]:
                for item1 in lstitledara:
                    ctqtitle= auxfun.removerlist(auxfun,item1, puli)
                    if ctqtitle.lower()==item[2].lower():
                        item[2]=item1
                        neulist.append(item)
            neulist.append(tf[-1])
            neulist.sort(key=lambda x: float(x[1]))
            neulist=list(reversed(neulist))
            strfile=''
            if (self.yearcheck(neulist,abb_refrence)!=['Null']):
                neulist=self.yearcheck(neulist,abb_refrence)

            for item in neulist:
                strfile=strfile+"index:"+item[0] + "\nvalue:"+item[1]+"\nTExT:"+item[2]+"\n"
                strfile=strfile
            directory='lists_files/Testlog2/'+nameidx
            nds='lists_files/Testlog2/'+nameidx+'/'+abb_refrence+'_'+localtime+'.txt'
            if not os.path.exists(directory):
                os.makedirs(directory)
            f = open(nds, 'wb')
            f.write(strfile.encode('utf-8'))
            f.close()

    def yearnoticer(self,list1,abb_refrence):
             query=list1[0]
             sentence=query[2]
             ss=sentence.split()
             lks=[s for s in ss if s.isdigit()]
             lks=list(set(lks))
             abb_index=[m.start() for m in re.finditer(abb_refrence.lower(), sentence)]
             allnumlist=[]
             for item in lks:
                 allnumlist.append([item]+[m.start() for m in re.finditer(item, sentence)])
             distanceofnum=[]
             for item1 in abb_index:
                for item in allnumlist:
                  if int(item[0])==2008:
                    listinside=[]
                    listinside.append(item[0])
                    item.pop(0)
                    for item2 in item:
                        listinside.append(math.fabs(item1-item2))
                    distanceofnum.append(listinside)

    def sep_checK(self,abb,cont):
            punc= lsarray1.Punctuation + lsarray1.Punctuation1 + lsarray1.Punctuation2 + [' '] + ['s']
            while abb in cont:
                    index=cont.find(abb)
                    lent=len(abb)
                    if cont[index+lent:index+lent+1] in punc or cont[index+lent:index+lent+1].isdigit():
                        if cont.find(abb)==0:
                            return True
                        elif cont[index-1:index] in punc or cont[index-1:index]==' ':
                            return True
                    elif index+lent==len(cont):
                        if cont.find(abb)==0:
                            return True
                        elif cont[index-1:index] in punc:
                            return True

                    try:
                        cont=cont[index+1:]
                    except:
                        return False
            return False


    def yearcheck(self,neulist,abb):
        closestyear=self.closest_yeart(neulist,abb)
        neulist1=neulist[1:]
        lsfinal=[]
        if closestyear!='null':
            for item in neulist1:
                if self.sep_checK(closestyear, item[2]):
                        lsfinal=[]
                        neulist1.remove(item)
                        lsfinal=lsfinal+[neulist[0]]+[item]+neulist1
                        break
                else:
                        lsfinal=['Null']
        else:
            lsfinal=['Null']
        return lsfinal




    def year_extractor(self,text):
        ls=re.findall('\d+', text)
        y = [xc for xc in ls if len(xc) == 4 and 1900<int(xc) and int(xc)<=date.today().year]
        return y

    def closest_yeart(self,neulist,abb):
        itemq=neulist[0]
        itemqtext=itemq[2]
        lsabbq=[m.start() for m in re.finditer(abb.lower(), itemqtext)]
        lsyearind=[]
        lsyear=self.year_extractor(itemqtext)
        if(lsyear!=[]):
            for item in lsyear:
                indyear=[m.start() for m in re.finditer(str(item), itemqtext)]
                lsyearind=lsyearind+indyear
            if (lsyearind!=[] and lsabbq!=[]):
                pairdistance=[]
                for item in lsabbq:
                    for item1 in lsyearind:
                        pairdistance.append([item,item1])
                puredistance=[]
                for item in pairdistance:
                    puredistance.append(math.fabs(item[1]-item[0]))
                indexmin=min(enumerate(puredistance), key=itemgetter(1))[0]
                itemyearindex=pairdistance[indexmin][1]
                finalresultyear=itemqtext[itemyearindex:itemyearindex+4]
            else:
               finalresultyear='null'
        else:
            finalresultyear='null'
        return finalresultyear






