import pandas as pd
from requests import get  # to make GET request
import os
import tabula
import camelot
from PyPDF2 import PdfFileReader 

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

def get_csvs(source, row, col):
    df = pd.read_csv(source)

    for counter, element in enumerate(df.iloc[:row, col]):
        if type(element) is str and ".pdf" in element:
            doc_name = clean_phrase(df.columns[col] + "_" + df.iloc[counter, 1])
            pdf_name = doc_name + ".pdf"
            csv_name = doc_name + ".csv"
            csv_name2 = doc_name + '2' + ".csv"
            
            download(element, pdf_name)
            try :
                mypdf = PdfFileReader(open( pdf_name, 'rb'))
                tables = camelot.read_pdf(pdf_name, pages='all')
                tables.export(csv_name2, f='csv')
                #tabula.convert_into(pdf_name, csv_name, multiple_tables=True, pages='all')
            except:
                print(pdf_name,' is invalid pdf')
            
            os.remove(pdf_name)
