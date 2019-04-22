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

    for counter, element in enumerate(df.iloc[start:end, col], start):
        if type(element) is str and ".pdf" in element:
            doc_name = clean_phrase(df.columns[col] + "_" + df.iloc[counter, 1])
            pdf_name = doc_name + ".pdf"
            csv_name = doc_name + ".csv"
            download(element, pdf_name)
            try :
                mypdf = PdfFileReader(open( pdf_name, 'rb'))
                #tabula.convert_into(pdf_name, csv_name, multiple_tables=True, pages='all')
            except:
                print(pdf_name,' is invalid pdf')
                break
            pages, names = lookup_table(pdf_name)
            print(pages, names)
            temp = tabula.read_pdf(pdf_name, multiple_tables=True, pages=pages)
            x,y=1,0
            for t in temp:
                #t.columns = t.iloc[0]
                #t.drop(t.index[0], inplace=True)
                #t['jurisdiction'] = "hello"#df.iloc[counter, 1]
                #t['location_type'] = df.iloc[counter, 2]
                #t['table_number'] = x
                #t['table_name'] = names[y]
                x += 1
                y += 1
            #return tables
            tables += temp

            #os.remove(pdf_name)
    return tables

def lookup_table(pdf_doc):
    string = r'\n[T|t]{1}able\s[\d+\w+][:|\.|\s]\n*(.+)\n'
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
