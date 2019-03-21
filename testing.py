import PyPDF2
import csv
import json
import pandas as pd
#import matplotlib.pyplot as plt
#import camelot
import tabula
import requests
import os
import re

def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = requests.get(url)
        # write to file
        file.write(response.content)
#iterate over df and access links, download pdfs, convert tables to csv
def get_tables(df,start=0, end=-1):
    tables = []
    for row in df[start:end].values:
        for i in row:
            if '.pdf' in str(i):
                if '200' in str(requests.get(str(i))):
                    download(str(i), str(row[1])+'.pdf')
                    pages, names = lookup_table(str(row[1])+'.pdf')
                    print(pages,names)
                    tables += tabula.read_pdf(str(row[1])+'.pdf',multiple_tables=True, pages=pages)
                    x,y=1,0
                        # open("foo.csv", "w")
                        #bobbert = tables[1]
                    for t in tables:
                        t.columns = t.iloc[0]
                        t.drop(t.index[0], inplace=True)
                        t['jurisdiction'] = str(row[1])
                        t['location_type'] = str(row[2])
                        t['table_number'] = x
                        #t['table_name'] = names[y]
                        x += 1
                        y += 1
                        with open('foo.csv', 'a') as f:
                            t.to_csv(f, header=False)
#t.to_csv(str(row[1]) + " " + x + ".csv")

#bobbert.to_csv ("gobears.csv", index = None, header=True)

                                               #with open(nam,'a') as fd:
                        #	fd.write(t)


					
                    #tables = tabula.convert_into(str(row[1])+'.pdf', str(row[1])+'.csv',output_format='csv',
                                              #multiple_tables=True, pages='all')
                    #os.remove(str(row[1])+'.pdf')



def lookup_table(pdf_doc):
    string = r'([T|t]{1}able\s[\w+\d+].+)\n'
    
    doc = PyPDF2.PdfFileReader(open(pdf_doc, 'rb'))
    pages = []
    names = []
    for i in range(doc.getNumPages()):
        page = doc.getPage(i)
        text = page.extractText()
        if re.search(string, text):
            pages.append(i)
            names += re.findall(r'[T|t]{1}able\s[\d+\w+][:|\.|\n](.+)\n', text)
    return pages, names

df = pd.read_csv('Counties.csv')
a = get_tables(df,1,69)

#pd.DataFrame(a).to_csv("file.csv", header=None, index=None)
 #Don't forget to add '.csv' at the end of the path





