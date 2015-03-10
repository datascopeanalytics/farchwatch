#!/usr/local/bin/python
import os
import sys
import json
from datetime import datetime
from collections import defaultdict

import numpy as np
import pandas as pd

DATA_CSV = '../data/468104.csv'

COLUMNS = [
    'STATION_NAME',
    'DATE', 
    'PRCP', 
    'SNOW', 
    'TMAX', 
    'TMIN', 
    'AWND', 
    'WT01', 
    'WT13', 
    'WT16', 
    'WT08',
]


def get_df_from_csv():
    nan_values = ['-9999','9999']
    df = pd.read_csv(DATA_CSV, na_values = nan_values, parse_dates=True,low_memory=False)
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
    awful_thing = df['DATE'].astype(str)
    df.loc[:,'DATE'] = pd.to_datetime(awful_thing,format="%Y%m%d")
    return df

def convert_to_farenheit(df):
    
    df.loc[:,'TMAX'] = df.loc[:,'TMAX'].map(faren)
    df.loc[:,'TMIN'] = df.loc[:,'TMIN'].map(faren)
    return df
    
def add_date_cols(df):    
    df.loc[:,'year'] = df.loc[:,'DATE'].map(lambda x:x.year)
    df.loc[:,'month'] = df.loc[:,'DATE'].map(lambda x:x.month)
    df.loc[:,'day'] = df.loc[:,'DATE'].map(day_of_year)

    return df

def midway_readings_only(df):
    stations = df.STATION_NAME.unique()
    return df[df.loc[:,'STATION_NAME'] == stations[0]]

def remove_botanical_garden(df):
    stations = df.STATION_NAME.unique()
    return df[df.loc[:,'STATION_NAME'] != stations[2]]

def make_cols_human_readable(df):
    df.rename(columns = {
        'WT01': 'FOG',
        'WT13':'MIST',
        'WT16':'RAIN',
        'WT08':'HAZE'
    }, inplace=True)
    return df

def nans_to_zeroes(df):
    '''
    specific to these columns, 
    replacing NaNs with zeroes 
    for the purpose of making averages quickly and lazily 
    legitimacy of doing this: Medium-Meh to Meh.
    '''
    for col in ['SNOW','FOG','MIST','RAIN','HAZE']:
        df.loc[:,col]=df.loc[:,col].replace(np.NaN,0)

    return df

def clean_dataframe(df,columns):
    df = make_dates_dates(df.loc[:,columns])
    df = convert_to_farenheit(df)
    df = add_date_cols(df)
    df = remove_botanical_garden(df)
    df = make_cols_human_readable(df)
    df = nans_to_zeroes(df)

    return df
    

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

def nans_to_nulls(df):
    '''
    to entire dataframe, 
    changing one convention of saying 'nothing' to another,
    for the purpose of creating valid JSON
    legitimacy: V. Legit.
    '''
    df.loc[:,:] = df.where(pd.notnull(df),None)
    return df

def create_df_by_date():
    df = clean_dataframe(get_df_from_csv(),COLUMNS)
    return df.groupby(['DATE']).mean()

def dict_me(df):
    return nans_to_nulls(df).reset_index().to_dict('records')

def create_yearly_dict_from_df(df1):
    df = df1.copy()
    stupid_data_dict = dict_me(df)

    data_dict = {}
    for record in stupid_data_dict: 
        date = str(record['DATE']).split()[0]
        record['DATE'] = date
        data_dict[date]=record
    
    # dby: data_by_year
    dby = defaultdict(list)
    for record in data_dict.itervalues():
        y = record['year']
        dby[y].append(record)

    # sort days within each year
    for key,val in dby.iteritems():
        val.sort(key=lambda x: x['DATE'])    
        
    return dby


def when_is_it_over(yearly_dict,tolerance):
    # figuring out when it is over each year
    over_dict=defaultdict(dict)

    for year, stuff in yearly_dict.items():

        number_bummers = 0
        over_date = None
        for day in reversed(stuff):
            if number_bummers <= tolerance:
                if day['not_over']:
                    over_dict[year][number_bummers] = over_date
                    number_bummers += 1
                if day['is_nice']:
                    over_date = day['DATE']

            else:
                break

    return dict(over_dict)

    
def add_nice_and_over(df,nice,not_over,tol):

    df.loc[:,'is_nice'] = (df.loc[:,'TMAX'] > nice) & (df.loc[:,'PRCP'] < 10)
    df.loc[:,'not_over'] = df.loc[:,'TMAX'] < not_over

    return df

if __name__ == '__main__':

    # make a dirrrrrr for the da-duh
    dirname = 'data_out_'+datetime.strftime(datetime.now(),'%Y%m%d_%I%M') 
    os.mkdir(dirname)

    df_by_date = create_df_by_date()

    #### SET RULES FOR "OVER" 
    # once a daily high hits [NICE] degrees with no PRCP, "it is over" if, 
    # after that day, the high is below [NOT_OVER] degrees 
    # [TOLERANCE >= 0] times or fewer.
    NICE = 60 
    NOT_OVER = 50
    TOLERANCE = 1
    ##
    df_with_nice_and_over = add_nice_and_over(df_by_date,NICE,NOT_OVER,TOLERANCE)

    # data json 1: data_by_year.json
    yearly_dict = create_yearly_dict_from_df(df_with_nice_and_over)
    with open(dirname+'/data_by_year.json','w') as outfile1:
        json.dump(yearly_dict,outfile1)

    # data json 2: when_it_be_over.json
    over_dict = when_is_it_over(yearly_dict,TOLERANCE)
    over_dict['metadata']={
        'NICE':NICE,
        'NOT_OVER':NOT_OVER,
        'TOLERANCE':TOLERANCE,
    }
    with open(dirname+'/when_it_be_over.json','w') as outfile2:
        json.dump(over_dict,outfile2)
    
    # data json 3: daily_averages.json


    daily_averages_df = df_with_nice_and_over.groupby('day').mean()
    daily_averages = dict_me(daily_averages_df)
    with open (dirname+'/daily_averages.json','w') as outfile3:
        json.dump(daily_averages,outfile3)



   

