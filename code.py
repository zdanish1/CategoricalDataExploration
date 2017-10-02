import pandas as pd
import numpy as np

######################################################
###################### PART 1 ########################
######################################################

# - Fill Rate
# - True-Valued Fill Rate
# - Cardinality

#reads in data from a json file
data = pd.read_json('data_analysis.json')

#the following dictionary records expected lengths for certain fields to use for validation
len_dict = {'category_code': 8, 'phone': 10, 'state': 2, 'zip': 5}

#fill rate
def fill(df, colname): 
    return sum(df[colname].notnull())

#true-valued fill rate
def tvfill(df, colname):
    df = df[~df[colname].isin(['',' ','0',0,None,'none','null'])]
    if colname in len_dict.keys():
        return len(df[df[colname].map(len) == len_dict[colname]])
    return len(df)

#cardinality
def cardinality(df, colname):
    df = df[~df[colname].isin(['',' ','0',0,None,'none','null'])]
    if colname in len_dict.keys():
        return df[df[colname].map(len) == len_dict[colname]][colname].nunique()
    return df[colname].nunique()

#catch-all function
def compute(fun,*args):
    return fun(*args)

#dictionary to record the the fill rate, true-valued fill rate and cardinality
summary_dict = {'Columns': list(data.columns),\
                'Fill Rate': [compute(fill,data,c) for c in list(data.columns)],\
               'True Value Fill Rate' : [compute(tvfill,data,c) for c in list(data.columns)],\
               'Cardinality' : [compute(cardinality,data,c) for c in list(data.columns)]}

#converting to dataframe
fig1 = pd.DataFrame(summary_dict)[['Columns','Fill Rate', 'True Value Fill Rate', 'Cardinality']]
print fig1

