#!/usr/bin/env python
# coding: utf-8

# In[97]:


import PyPDF2
import csv
import json
import pandas as pd
import matplotlib.pyplot as plt
import camelot
import tabula
import re
import requests
import os


# In[106]:


def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = requests.get(url)
        # write to file
        file.write(response.content)
#Load list of urls to extract pdfs from
df = pd.read_csv('Cities.csv')
#iterate over df and access links, download pdfs, convert tables to csv
for row in df[:14].values:
    for i in row:
        if '.pdf' in str(i):
            if '200' in str(requests.get(str(i))):
                download(str(i), str(row[1])+'.pdf')
                tables = tabula.convert_into(str(row[1])+'.pdf', str(row[1])+'.csv',output_format='csv',
                                             multiple_tables=True, pages='all')
                os.remove(str(row[1])+'.pdf')

