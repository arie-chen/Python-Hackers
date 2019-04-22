#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PyPDF2
import csv
import json
import pandas as pd
import matplotlib.pyplot as plt
import camelot
import tabula
import requests
import os
import re


# In[25]:


def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = requests.get(url)
        # write to file
        file.write(response.content)
#iterate over df and access links, download pdfs, convert tables to csv
def get_tables(csv,start=0, end=-1):
    df = pd.read_csv(csv)
    tables = []
    file_name = []
    links = []
    for row in df[start:end].values:
        for i in row:
            if 'http' in str(i):
                if '200' in str(requests.get(str(i))):
                    if 'application/pdf' in str(requests.get(str(i)).headers['Content-Type']) and str(i) not in links:
                        links.append(str(i))
                        download(str(i), str(row[1])+'.pdf')
                        pages, names = lookup_table(str(row[1])+'.pdf')
                        result = pd.DataFrame([])
                        tables += tabula.read_pdf(str(row[1])+'.pdf',multiple_tables=True, pages=pages)
                        if str(row[1])+'.pdf' not in file_name:
                            file_name.append(str(row[1])+'.pdf')
                        x,y=1,0
                        for t in tables:
                            try:
#                                 t.columns = t.iloc[0]
#                                 t.drop(t.index[0], inplace=True)
                                t['jurisdiction'] = str(row[1])
                                t['location_type'] = str(row[2])
                                t['table_number'] = x
#                                 t['table_name'] = names[y]
#                                 tables.append(t)
                                x += 1
                                y += 1
                                with open('extract_cities.csv', 'a') as f:
                                    t.to_csv(f)
                            except:
                                continue
    for file in file_name:
#         print(file)
        os.remove(file)
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
            names += re.findall(r'[T|t]{1}able\s[\d*\w*][:|\.|\n|-](.+)\n', text)
    return pages, names


# In[26]:


#Load list of urls to extract pdfs from

get_tables('Cities.csv', 11, 15)

