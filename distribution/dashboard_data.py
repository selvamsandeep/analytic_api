import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

import os
#DATA_DIR = 'data/'
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'distri_data/')

def create_dataframe():
    sales_df = pd.read_excel(DATA_DIR + 'Sales.xls', parse_dates=['Date'])
    sales_df['month'] = sales_df.Date.dt.month    
    sales_df['dayofyear'] = sales_df.Date.dt.dayofyear
    sales_df['month_year'] = sales_df.Date.apply(lambda x:x.strftime('%B-%Y'))
    sales_df['quater'] = sales_df.Date.dt.quarter.apply(lambda q : 4 if q == 1 else q-1)
    required_cols = ['Date', 'month',  'month_year', 'quater',
                     'Party Name', 'Item Name', 'Billed Quantity', 'Rate', 'Amount']    
    df = sales_df[required_cols].copy()
    
    return df


def partywise_aggregated_sales(data_frame, k=10):
    """
     input => data frame 
     output: [{'k': 'Kavi Protein And Feed Pvt Ltd', 'v': 31164474.440000005}, ....]
    """
    partywise_sales_amt = data_frame.groupby(['Party Name'], as_index=False)['Amount'].sum(). \
    sort_values(by='Amount', ascending=False)
    df = partywise_sales_amt.head(k)
    lst = []
    for p, a in zip(df['Party Name'].tolist(), df['Amount'].tolist()):      
        lst.append({'key':p, 'value':a})
    return lst


def itemwise_aggregated_salse_in_amt(data_frame, k=10):
    """
     input => data frame 
     output: [{'key': 'D L Methionine 99% - 1 Kg', 'value': 51347221.699999996}, ....]
    """
    itemwise_sales_amt = data_frame.groupby(['Item Name'], as_index=False)['Amount'].sum(). \
    sort_values(by='Amount', ascending=False)
    df = itemwise_sales_amt.head(k)
    lst = []
    for item, amt in zip(df['Item Name'].tolist(), df['Amount'].tolist()):
        lst.append({'key':item, 'value':amt})
        
    return lst


def montly_sales(data_frame):
    """
    input => data frame 
    output=> [{'key': 'April-2018', 'value': 56975192.91000037}, ....]
    """
    df = data_frame.groupby(['month_year'], as_index=False).agg({'Amount':sum})
    
    lst = []
    for month, amount in zip(df['month_year'].tolist(), df['Amount'].tolist()):
        lst.append({'key':month, 'value':amount})
        
    return lst


def quaterly_sales(data_frame):
    """
    input => data frame 
    output=> [{'key': 'quater-1', 'value': 158720365.68999895}, ....]
    """
    df = data_frame.groupby(['quater'], as_index=False).agg({'Amount':sum})
    
    lst = []
    for quater, amount in zip(df['quater'].tolist(), df['Amount'].tolist()):
        lst.append({'key':'quater-'+str(quater), 'value':amount})
        
    return lst

def get_item_monthly_sales(item, dataframe):
    """
    input => item_name, data frame 
    output=> [{'key': 'January-2019', 'value': 4138092.75}, ....]
    """
    #curr_year = '2019'
    #dataframe['year'] = dataframe['month_year'].apply(lambda x: x[-4:])
    #df = dataframe[(data_frame['Item Name'] == item) & (dataframe['year'] == curr_year)]
    df = dataframe[dataframe['Item Name'] == item]
    df = df.groupby('month_year', as_index=False).agg({'Amount':np.sum})
    lst = []
    for month, amount in zip(df['month_year'].tolist(), df['Amount'].tolist()):
            lst.append({'key':month, 'value':amount})
    return lst

def get_party_monthly_sales(party, dataframe):
    """     
    input => party_name, dataframe 
    output=> [{'key': 'January-2019', 'value': 4138092.75}, ....]
    
    """
    #curr_year = '2019'
    #dataframe['year'] = dataframe['month_year'].apply(lambda x: x[-4:])
    #df = dataframe[(data_frame['Party Name'] == party) & (dataframe['year'] == curr_year)]
    df = dataframe[dataframe['Party Name'] == party]
    df = df.groupby('month_year', as_index=False).agg({'Amount':np.sum})
    lst = []
    for month, amount in zip(df['month_year'].tolist(), df['Amount'].tolist()):
            lst.append({'key':month, 'value':amount})
    return lst

def item_qty_sold_to_party(item, party_list, dataframe):
    """
    input: 
    item => Item_name
    party_list=> list of party [{'name': 'Megha Poultry Farm'},..,]
    dataframe
    output: [{'name': 'Megha Poultry Farm', 'qty': 2300},...]
    """
    df = dataframe[dataframe['Item Name'] == item]
    lst = []
    for i, p in enumerate(party_list):
        if i > 10: break
        party = p['name']
        qty = df[df['Party Name'] == party]['Billed Quantity'].sum()
        lst.append({'name':str(party), 'qty':int(qty)})        
   
    return lst

def party_puchased_items_qty(party, item_list, dataframe):
    """
    input: 
    item => Item_name
    party_list=> list of party [{'name': 'Megha Poultry Farm'},..,]
    dataframe
    output: [{'name': 'Megha Poultry Farm', 'quatntity': 2300},...]
    """
    df = dataframe[dataframe['Party Name'] == party]
    lst = []
    for i, p in enumerate(item_list):
        item = p['name']
        qty = df[df['Item Name'] == item]['Billed Quantity'].sum()
        lst.append({'name':str(item), 'qty':int(qty)})
        if i > 10: break
   
    return lst

if __name__=='__main__':
    data_frame = create_dataframe()
    print(partywise_aggregated_sales(data_frame))
    print('\n')
    print(itemwise_aggregated_salse_in_amt(data_frame))
    print('\n')
    print(montly_sales(data_frame))
    print('\n')
    print(quaterly_sales(data_frame))
    print('\n')
    
