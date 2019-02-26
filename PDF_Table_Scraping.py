#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PyPDF2
import csv
import json
import pandas as pd
#import matplotlib.pyplot as plt
#import camelot
import tabula
import re


# In[7]:


#Extracting all tables from pages containing term table with Camelot
#table = camelot.read_pdf('Richmond_emissions.PDF', pages='all')


# In[9]:


#Result: List of Camelot TableList objects containing DataFrames
#len(table)


# In[6]:


#Extracting all tables from pages containing term table with Tabula
a = tabula.read_pdf('Richmond_emissions.PDF', multiple_tables=True, pages='all')
i = 0
for x in a :
    x['Table Number'] = i;
    i+=1
print(a)
#reader = PyPDF.PdfFileReader(open("Richmond_emissions.PDF", mode='rb' ))
#n = reader.getNumPages()
#print(n)

#df = []
#for page in [str(i+1) for i in range(n)]:
#    if page == "1":
#            df.append(tabula.read_pdf("Richmond_emissions.PDF", multiple_tables=True, pages=page))
#            print(df)
#            break;

#    else:
#            df.append(tabula.read_pdf(r"Richmond_emissions.PDF", pages=page))






#tabula.convert_into("Richmond_emissions.PDF", "output.csv", output_format="csv",multiple_tables=True, pages='all')
