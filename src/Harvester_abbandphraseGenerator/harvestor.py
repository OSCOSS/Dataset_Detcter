import urllib.request
import xml.etree.ElementTree as ET
import sys
import timeit
import Harvester_abbandphraseGenerator.gnt as gntinstance
gnt=gntinstance.doiandtitlegenratorclass()

class harvestorclass:
    def harvestor(self):
        starttimerun = timeit.default_timer()
        url = 'http://www.da-ra.de/oaip/oai?verb=ListRecords&metadataPrefix=oai_dc'
        ls=[]
        file = urllib.request.urlopen(url)
        tree = ET.parse(file)
        root = tree.getroot()
        root = root.find('{http://www.openarchives.org/OAI/2.0/}ListRecords')
        token=root.find('{http://www.openarchives.org/OAI/2.0/}resumptionToken')
        comsiz= token.attrib['completeListSize']
        cursor=token.attrib['cursor']
        token=token.text
        lstoken=(token.split(','))
        index=0
        url=lstoken[0]+','+lstoken[1]+','+lstoken[2]+','+str(index)+','+lstoken[4]+','+lstoken[5]
        url='http://www.da-ra.de/oaip/oai?verb=ListRecords&resumptionToken='+url
        #url='http://www.da-ra.de/oaip/oai?verb=ListRecords'
        while index<int(comsiz):
            try:
                print('current:'+url)
                file = urllib.request.urlopen(url)
                tree = ET.parse(file)
                root = tree.getroot()
                root = root.find('{http://www.openarchives.org/OAI/2.0/}ListRecords')
                #newline/oneline
                #token=root.find('{http://www.openarchives.org/OAI/2.0/}resumptionToken')
                root = root.findall('{http://www.openarchives.org/OAI/2.0/}record')
                for child in root:
                    for child1 in child.find('{http://www.openarchives.org/OAI/2.0/}metadata'):
                          type=child1.findall('{http://purl.org/dc/elements/1.1/}type')
                          title=child1.findall('{http://purl.org/dc/elements/1.1/}title')
                          DOI=child1.findall('{http://purl.org/dc/elements/1.1/}identifier')
                          if (type[0].text=='Dataset' or type[0].text=='Datensatz'):
                              for titleitem in title:
                                  if (titleitem.text !='Archival Version'):
                                        teitem=titleitem.text.split()
                                        if (teitem[0]!='Version' and len(teitem)!=2):
                                            txtttle=titleitem.text+' #this is BEN_DOI# '+DOI[0].text
                                            ls.append(txtttle)

            except:
                print(index)
                e = sys.exc_info()[0]
                print( "<p>Error: %s</p>" % e )
            index=index+50
            url='http://www.da-ra.de/oaip/oai?verb=ListRecords&resumptionToken='+lstoken[0]+','+lstoken[1]+','+lstoken[2]+','+str(index)+','+lstoken[4]+','+lstoken[5]
            print('lenght'+str(len(ls)))


        ls=list(set(ls))
        f = open("text_list_of_tile_1.txt",'wb')
        for item in ls:
            item=item+u"\n"
            f.write(item.encode('UTF-8'))
        f.close()
        stopruntime = timeit.default_timer()

        print ('time='+str(stopruntime-starttimerun))
    def collection(self):
        # It harvests information of datasets in dara (doi_titles)
        self.harvestor()

        # It creates two files from harvested information from dara (these two files are doi and titles).
        gnt.doiandtitlegenrator()

    def doititlecaller(self):
        print('pass')
        gnt.doiandtitlegenrator()

