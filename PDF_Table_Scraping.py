#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PyPDF2
import csv
import json
import pandas as pd
import camelot
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
a = tabula.convert_into('Richmond_emissions.PDF', "richmond_emissions.csv", multiple_tables=True, pages='all')

