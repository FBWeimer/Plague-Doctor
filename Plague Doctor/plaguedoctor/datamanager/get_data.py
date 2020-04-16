import gspread
import pandas as pd
from plaguedoctor.datamanager import access


def date_scope(initial_month,last_month):


    month = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'aulho', 'sgosto', 'setembro', 'outubro',
             'novembro', 'dezembro']

    index_initial_month = month.index(initial_month)
    index_last_month = month.index(last_month)

    return index_initial_month, index_last_month

def data_concatenate(initial_month,last_month,state_sheet,client):
    df = []
    index_initial_month, index_last_month = date_scope(initial_month,last_month)

    if last_month > initial_month:
        for months in range(index_initial_month,index_last_month+1): #or in range(0,12), to get all months of the year
            month = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'aulho', 'sgosto', 'setembro',
                     'outubro', 'novembro', 'dezembro']
            month = month[months].upper()
            book = client.open_by_url(state_sheet)
            sheet = book.worksheet(month)
            data = pd.DataFrame(sheet.get_all_records())
            df.append(data)
            try:
                data = pd.concat([df[0],df[1]])
            except:
                continue
    else:
        month = initial_month.upper()
        book = client.open_by_url(state_sheet)
        sheet = book.worksheet(month)
        data = pd.DataFrame(sheet.get_all_records())

    return data

