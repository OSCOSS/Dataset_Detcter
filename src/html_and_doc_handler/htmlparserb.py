# The file is for parsing and extracting context from an HTML document.
from html.parser import HTMLParser
from lists_files import lsarray1

class MyHTMLParser(HTMLParser):
    ls=[]
    def handle_data(self, data):
        checknull=data.strip()
        cmdidx=data.find("<!--")
        datawolinebreak=data.replace("\n", " ")
        if (checknull!="" and cmdidx==-1 ):
            self.ls.append(datawolinebreak)


def content(content):
    parser = MyHTMLParser()
    parser.ls=[]
    parser.reset()
    parser.feed(content)
    dashandunderlinechecker(parser.ls)
    dotchecker(parser.ls)
    parentheseshandler(parser.ls)
    lowerc=""
    while lowerc=="":
        lowerc=startwithlc(parser.ls)
    startwithlc(parser.ls)
    endwithstopword(parser.ls)
    startwithlowrcasestop(parser.ls)
    return (parser.ls)

def startwithlowrcasestop(lst):
    stopwords= lsarray1.stopwd
    for idx, item in enumerate(lst):
        item=item.lstrip()
        txt=item.partition(' ')[0]
        if (txt in stopwords and idx!=0 and txt.islower()):
           lst[idx-1]=lst[idx-1]+" "+lst[idx]
           del lst[idx]

def endwithstopword(lst):
    stopwords= lsarray1.stopwd
    lenght=len(lst)-1
    for idx, item in enumerate(lst):
       item=item.rstrip()
       txt=item.rsplit(None, 1)[-1]
       if (txt.lower() in stopwords and idx!=lenght):
           lst[idx]=lst[idx]+" "+lst[idx+1]
           del lst[idx+1]

def dashandunderlinechecker(lst):
    for idx, item in enumerate(lst):
       item=item.rstrip()
       if ( item.endswith('-') or item.endswith('_') or item.endswith(',')):
           lst[idx]=lst[idx]+" "+lst[idx+1]
           del lst[idx+1]
       elif( item.endswith('and') or item.endswith('or')):
           lst[idx]=lst[idx]+" "+lst[idx+1]
           del lst[idx+1]

def startwithlc(lst):
    lowrc="1"
    for idx, item in enumerate(lst):
        item=item.lstrip()
        if (item[0].islower() and idx!=0):
                lowrc=""
                lst[idx-1]=lst[idx-1]+" "+lst[idx]
                del lst[idx]
    return lowrc

def dotchecker(lst):
    for idx, item in enumerate(lst):
        item=item.rstrip().lstrip()
        if (item[0]=="."  and idx!=0) or (item[0]==":" and idx!=0)or (item[0]=="," and idx!=0):
            lst[idx-1]=lst[idx-1]+" "+lst[idx]
            del lst[idx]

def parentheseshandler(lst):
    for idx, item in enumerate(lst):
        lenght=len(lst)-1
        item=item.rstrip().lstrip()
        if (item[0]=="("  and idx!=0) or (item[0]=="<"  and idx!=0) or (item[0]=="["  and idx!=0) or (item[0]=="{"  and idx!=0) or (item[0]==")"  and idx!=0) or (item[0]=="]"  and idx!=0) or (item[0]=="}"  and idx!=0) or (item[0]==">"  and idx!=0):
            lst[idx-1]=lst[idx-1]+" "+lst[idx]
            del lst[idx]
        elif (item[-1]=="(") or (item[-1]=="<") or (item[-1]=="[") or (item[-1]=="{") or (item[-1]==")") or (item[-1]=="]") or (item[-1]=="}") or (item[-1]==">"):
            if (idx!=lenght):
                lst[idx]=lst[idx]+" "+lst[idx+1]
                del lst[idx+1]



