# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import csv
import os



os.chdir('html/html')

FileNames=os.listdir(os.getcwd()) 
ontologyDictName = {u'表型特征':'ontology_phenotype', u'分子功能':'ontology_function', u'生物进程':'ontology_bioprocess', u'形态构造':'ontology_structure'}
data = []
for file in FileNames:
    if file[-3:] == 'htm':
        print file
        with open(file) as fin:
            html = fin.read()
        
        soup = BeautifulSoup(html,"html5lib")
        
        tables = soup.findAll('table',{'class':'data-table'})
        tbody = tables[0]
        try:
            trs = tbody.findAll('tr')
        except:
            pass
        gname = ''
        gsymbol = ''
        chrom = ''
        material = ''
        contentps = ''
        try:
            gname = trs[1].find('td').contents[0] + "/" + trs[1].find('td').find('i').text
        except:
            pass
        try:
            gsymbol = trs[2].find('td').find('em').text
        except:
            pass
        try:
            chrom = trs[3].find('td').text
        except:
            pass
        try:
            material = trs[4].find('td').text.replace('\n',' ').replace('\r', '') 
        except:
            pass
        try:
            contentps = trs[5].find('td').findAll('p')
        except:
            contentps = []
        des = ''
        for p in contentps:
            des += p.text.replace('\n',' ').replace('\r', '')
        try: 
            locstb = trs[5].find('table').findAll('tr')[3].findAll('td')[1]
            locs = locstb.contents[0][:-1] + "/" + locstb.contents[6][:-1] 
        except:
            locs = "NA"
            
        ontologyDict = {u'表型特征':'', u'分子功能':'', u'生物进程':'', u'形态构造':''}
        try:
            ontologytr = tables[1].findAll('tr')
            for i in range(1,len(ontologytr)):
                ontologyDict[ontologytr[i].find('th').text] = ontologytr[i].find('td').text.replace('\n',' ').replace('\r', '')
        except:
            pass
        ref = ''
        try:
            reftable = tables[2]
            trs = reftable.findAll('tr')
            for i in range(1,len(trs)):
                ref += trs[i].find('td').text.replace('\n',' ').replace('\r', '') + ";"
        except:
            pass
        temp = {'filename':file,'genename':gname.encode('utf-8'),"genesymbol":gsymbol.encode('utf-8'),'chrom':chrom.encode('utf-8'),'material':material.encode('utf-8'),'des':des.encode('utf-8'),'ref':ref.encode('utf-8')}
        
        for key in ontologyDictName:
            if key in ontologyDict:
                temp[ontologyDictName[key]] = ontologyDict[key].encode('utf-8')
            else:
                temp[ontologyDictName[key]] = "NA"
        data.append(temp)

os.chdir('../../')

with open('ricedata.csv', 'wb') as csvfile:
    fieldnames = ['filename','genename', 'genesymbol','chrom','material','des','ontology_phenotype','ontology_function','ontology_bioprocess','ontology_structure','ref']
    writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)


    writer.writerow(fieldnames)
    
    for eachline in data:
        temp = []
        for f in fieldnames:
            temp.append(eachline[f])
        writer.writerow(temp)

