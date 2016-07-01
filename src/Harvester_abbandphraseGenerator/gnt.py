class doiandtitlegenratorclass:
    # It takes a text file and then, it puts each line into an item on the output list.
    def readtoarr2(self,str='Harvester_abbandphraseGenerator/text_list_of_tile_1.txt'):
        with open(str, "r", encoding="utf-8") as f:
             mylist = list(f)
        fl=[]
        for item in mylist:
            fl.append(item.rstrip('\n'))
        return  fl

    # It creates two files from harvested information from dara (these two files are doi and titles).
    def doiandtitlegenrator(self):
        ls=self.readtoarr2()
        for idx, item in enumerate(ls):
            if item.find('                ')==0:
                ls[idx-1]=ls[idx-1]+" "+ls[idx]
                ls[idx-1]=ls[idx-1].replace('                 ',' ')
                del ls[idx]
        titles=[]
        doi=[]
        ls=list(set(ls))
        for item in ls:
            a=item.split(" #this is BEN_DOI# ")
            titles.append(a[0])
            doi.append(a[1])

        f = open("lists_files/title1.txt",'wb')
        endidx=len(titles)-1
        for idx,item in enumerate(titles):
            if idx!=endidx:
                item=item+u"\n"
            else:
                item=item
            f.write(item.encode('UTF-8'))
        f.close()

        f = open("lists_files/doi.txt",'wb')
        endidx=len(doi)-1
        for idx,item in enumerate(doi):
            if idx!=endidx:
                item=item+u"\n"
            else:
                item=item
            f.write(item.encode('UTF-8'))
        f.close()