import json
from datetime import datetime

import numpy as np
import pandas as pd

DATA_CSV = './data/468104.csv'

def get_df_from_csv():
    nan_values = ['-9999','9999']
    df = pd.read_csv(DATA_CSV, na_values = nan_values, parse_dates=True)
    return df

def faren(cel):
    # temperatures stored in tenths of degrees C (hence /50 instead of /5 below)
    if pd.isnull(cel):
        return cel
    else:
        return int(cel)*9/50+32
    
def day_of_year(dt):
    return int(datetime.strftime(dt,'%j'))

def make_dates_dates(df):
    df.DATE = pd.to_datetime(df.DATE.map(lambda x:str(x)),format="%Y%m%d")
    return df

def convert_to_farenheit(df):
    
    df['TMAX'] = df.TMAX.map(faren)
    df['TMIN'] = df.TMIN.map(faren)
    return df
    
def add_date_cols(df):    
    df['year'] = df['DATE'].map(lambda x:x.year)
    df['month'] = df['DATE'].map(lambda x:x.month)
    df['day'] = df['DATE'].map(day_of_year)

    return df

def clean_dataframe(df,columns):

     return add_date_cols(convert_to_farenheit(make_dates_dates(df[columns])))
    

def create_column_defs():
    '''
    creates a dictionary of weather column names and descriptions and dumps
    them to JSON.
    '''

    # Column descriptions are processed in 2 chunks for the following reason: 
    # Most columns are defined according to their name in full. However, 
    # there is a large list of weather type columns of the pattern 
    # "WT*" (i.e. "WT02") that are described in the pdf by their number only. 

    # copy-pasted pdf text to 2 text files to ingest here.

    # the first text file and code block take care of the WT pattern cols, and the 
    # second file and code block do the rest. 
    WT_RAW = 'data/wtypes.txt'
    COLUMNS_RAW = 'data/codez.txt'

    column_key = {}

    # I copied these from a pdf, and some of the linebreaks did not survive. 
    # "double lines" are handled in the except block
    with open(WT_RAW,'r') as infile:
        for line in infile:
            try:
                num,description = line.split(' = ')
                column_key['WT'+num] = description.strip()
            except:
                parts = line.split(' = ')
                column_key['WT'+parts[0]] = parts[1][:-3]
                column_key['WT'+parts[1][-2:]] = parts [2].strip()

    # for this set I just fixed the unbroken lines in emacs before running this,
    # so there should not be any "double lines"
    with open (COLUMNS_RAW,'r') as infile:
        for line in infile:
            try:
                code,description = line.split(' = ')
                column_key[code] = description.strip()
            except:
                print '*****',line

    #pprint(column_key)

    with open('data/column_descriptions.json','w') as outfile:
        json.dump(column_key,outfile)

    return column_key
