import enchant
from nltk.corpus import wordnet
from lists_files import lsarray1
from html_and_doc_handler import htmlparserb
from similarity_cos_tf_idf import tf_final as tf_final_instance
tf_final=tf_final_instance.tf_final_class()
from similarity_cos_tf_idf import cosine_tf as cosine_tf_instance
cosine_tf=cosine_tf_instance.cosine_tf_class()
from similarity_cos_tf_idf import  aux_functions as aux_fun
auxfun=aux_fun.auxfunclass

class combinedapproach_class:
    # It checks that a token has a definition or not.
    def is_not_ditionaryDe_En(self,txt):
        definition=wordnet.synsets(txt)
        if not definition:
            dicge = enchant.Dict('de_DE')
            if not (dicge.check(txt)):
                return True
            else:
                return False
        else:
            return False

    # This function checks if a special feature exists in a context.
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

    # It is the main approach of our application ( the combination of cosine similarity and Tf-idf).
    def final_approach(self,content1,FiLeNaMe):
            ls= htmlparserb.content(content1)
            context=''
            for item in ls:
                context=context+' '+item
            abb1= auxfun.readtoarr2(auxfun,'lists_files/listofabb.txt')
            abb2= auxfun.readtoarr2(auxfun,'lists_files/listofPhrase.txt')
            candidate=[]
            for item in abb1:
                if self.sep_checK(item,context):
                    candidate.append(item)
            for item in abb2:
                if self.sep_checK(item,context):
                    candidate.append(item)
            textlist,abbinTlist= tf_final.sepfinder(candidate, ls)
            abbinTlist1=list(set(abbinTlist))
            textlist1=list(set(textlist))
            FiLeNaMe=FiLeNaMe.replace('File Name:','')
            FiLeNaMe=FiLeNaMe.replace('.html','')
            FiLeNaMe=FiLeNaMe.strip(' ')
            lsallsplit=[]
            for itemabb_q in abbinTlist1:
               for itemsenasquery in textlist1:
                    if self.sep_checK(itemabb_q,itemsenasquery):
                        neulistofquery= tf_final.querysplitter(itemsenasquery, itemabb_q)
                        if len(neulistofquery)>1:
                            neulistofquery.pop(0)
                        lsallsplit=lsallsplit+neulistofquery
            textlist1=list(set(lsallsplit))

            nodigitlist=self.removedigitlist(ls)
            for itemabb_q in abbinTlist1:
                for itemsenasquery in textlist1:
                    if self.sep_checK(itemabb_q,itemsenasquery):

                            itemsenasquery=self.improvequery(itemsenasquery,itemabb_q)
                            loctim= tf_final.tf_ec(itemsenasquery, nodigitlist, itemabb_q, FiLeNaMe)
                            cosine_tf.DAra_No(FiLeNaMe, itemabb_q, loctim)

    # It makes cases like "allbus2010" into "allbus 2010"
    def improvequery(self,query,abb_q):
        index=query.find(abb_q)
        lent=len(abb_q)
        if index+lent<len(query) and query[index+lent:index+lent+1].isdigit():
                       return query[:index+lent]+' '+query[index+lent:]
        else:
            return query

    def removedigitlist(self,listwithdigit):
        lenghtlist=len(listwithdigit)
        for x in range(0, lenghtlist):
                    resultwioutd = ''.join([i for i in listwithdigit[x] if not i.isdigit()])
                    listwithdigit[x]=resultwioutd
        return listwithdigit