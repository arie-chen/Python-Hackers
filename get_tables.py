from PyPDF2 import PdfFileWriter, PdfFileReader
import csv
import json
import pandas as pd
import matplotlib.pyplot as plt
import tabula
from requests import get
import os
import re
from tika import parser


## https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)


def clean_phrase(phrase):
    return phrase.replace(" ", "_").lower()

#iterate over df and access links, download pdfs, convert tables to csv
def get_tables(df, start=0, end=-1, col=15):
    tables = []

    for row, element in enumerate(df.iloc[start:end, col], start):
        if is_valid_pdf(element):
            doc_name = clean_phrase(df.columns[col] + "_" + df.iloc[row, 1])
            pdf_name = doc_name + ".pdf"
            download(element, pdf_name)
            temp = get_tables_from_pdf(df, pdf_name, row)
            if not temp:
                pass
            tables += temp
            os.remove(pdf_name)
    return tables

def lookup_table(pdf_doc):
    string = r'\n[T|t]{1}able\s(?:ES[^\s]*|[\d+\w+])[:|\.|\s]\n*(.+)\n'
    doc = PdfFileReader(open(pdf_doc, 'rb'))
    pages = []
    names = []
    for i in range(doc.getNumPages()):
        writer = PdfFileWriter()
        writer.addPage(doc.getPage(i))
        with open('temp.pdf', 'wb') as outfile:
            writer.write(outfile)
        page = doc.getPage(i)
        text = parser.from_file('temp.pdf')
        if text["content"] and re.search(string, text["content"]):
            pages.append(i + 1)
            names += re.findall(string, text["content"])
    return pages, names

def get_tables_from_pdf(df, pdf_name, row):
    pages, names = lookup_table(pdf_name)
    tables = tabula.read_pdf(pdf_name, multiple_tables=True, pages=pages)
    x = 1
    for t in tables:
        t['jurisdiction'] = df.iloc[row, 1]
        t['location_type'] = df.iloc[row, 2]
        t['table_number'] = x
        x += 1
    print("hello")
    return tables
    
def is_valid_pdf(link):
    if type(link) is not str:
        return False
    if '200' in str(get(link)) and 'application/pdf' in str(get(link).headers['Content-Type']):
        return True
    return False
