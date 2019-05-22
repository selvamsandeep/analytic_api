import numpy as np
import pandas as pd
import datetime
import calendar
import os
import warnings

#STORE='u100062'
#PATH = 'data/'
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/')

def get_daily_sales_data(store='u100062'):
    
    sales = pd.read_csv(PATH+'{}_trn_sales.csv'.format(store), 
                    parse_dates=['dtrandate'], 
                    low_memory=False)    
    sales['date'] = sales.dtrandate.dt.date.astype('datetime64[ns]')
    daily_sales = sales.groupby('date', as_index=False).agg({'nnettotal':np.sum})
    daily_sales['month']= daily_sales.date.dt.month.astype(np.int8)
    #daily_sales['month'] = daily_sales['month'].apply(lambda x: calendar.month_abbr[x])
    daily_sales['year'] = daily_sales.date.dt.year.astype(np.int16)
    
    return daily_sales


def load_n_process_salesdetail_data(store='u100062'):
    
    sales_details = pd.read_csv(PATH + '{}_trn_salesdetail.csv'.format(store), 
                    parse_dates=['LastUpdate'], 
                    low_memory=False)
    
    sales_details['vitem_len'] = sales_details['vitemcode'].apply(lambda x : len(x))
    sales_details = sales_details[sales_details['vitem_len'] > 2].copy()
    
    itemcode2name = {}
    #itemname2code = {}
    for code, name in zip(sales_details.vitemcode, sales_details.vitemname):
        itemcode2name[code] = name
        #itemname2code[name] = code
        
    return sales_details, itemcode2name


# grouped bar chart 
def get_monthly_sales_yearwise_data(df):
    """
    input: daily_sales data dataframe
    output: [{'2018_sales': 150720.0, '2019_sales': 168919.0, 'month': 1.0},
             {'2018_sales': 161158.0, '2019_sales': 0.0, 'month': 2.0}, ...]
    """
    
    ar = np.zeros((12, 3))
    
    now = datetime.datetime.now()
    year = now.year    
    monthly_sales = df.groupby(['year', 'month'], as_index=False).agg({'nnettotal':np.sum})    
    df = monthly_sales[monthly_sales['year'] >= year-1].copy()
    df['nnettotal'] = round(df['nnettotal'])    
    
    ar[:, 0] = np.arange(1, 13)
    ar[:, 1] = df[df['year'] == year-1]['nnettotal'].values
    mm = df[df['year'] == year]['nnettotal'].values
    ar[:len(mm), 2] = mm
    
    temp = pd.DataFrame(ar, columns=['month', str(year-1)+'_sales', str(year)+'_sales'])
    
    #print(df)
    return  temp.to_dict(orient='records')

# monthly sales trend line chart 
def get_monthly_sales_data(df):
    """
    input: daily_sales data dataframe
    output: [{'mm-yyyy': 'Jan-2018', 'monthly_sales': 150720.0},
             {'mm-yyyy': 'Feb-2018', 'monthly_sales': 161158.0},, ...]
    """
    
    ar = np.zeros((12, 3))
    
    now = datetime.datetime.now()
    year = now.year    
    monthly_sales = df.groupby(['year', 'month'], as_index=False).agg({'nnettotal':np.sum})    
    df = monthly_sales[monthly_sales['year'] >= year-1].copy()
    df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])
     
    df['mm-yyyy']  = df['month'] + '-' +df['year'].astype(str)
    df['monthly_sales'] = round(df['nnettotal'])
    df = df.drop(['year', 'month', 'nnettotal'], axis=1)
    
    #print(df)
    return  df.to_dict(orient='records')

#bar chart
def top10_items_based_on_sales(df, itemcode2name):
    """
    input: sales details dataframe, itemcode2name dict
    output: json [{'totalsales': 34396.74, 'vitemname': 'TITO S HANDMADE REGSTORE VODKA 1.75LT'},
                 {'totalsales': 31957.07, 'vitemname': 'MOET  CHANDON IMP 750ML'}, ....]
    """
    
    itemwise_sales = df.groupby(['vitemcode'], as_index=False). \
                                   agg({'nunitprice':np.average, 'ndebitqty': np.sum})
    
    itemwise_sales['totalsales'] = round(itemwise_sales['nunitprice'] * itemwise_sales['ndebitqty'], 2)
    itemwise_sales = itemwise_sales.sort_values(by='totalsales', ascending=False).head(10)
    itemwise_sales.insert(1, 'vitemname', itemwise_sales['vitemcode'].apply(lambda x: itemcode2name[x]))
    
    return itemwise_sales[['vitemname', 'totalsales']].to_dict(orient='records')

#bar chart
def top10_items_based_on_profit(df, itemcode2name):
    """
    input: sales details dataframe, itemcode2name dict
    output: json [{'profit': 4969.89, 'vitemname': 'SUPERME ZEN 3500MG'},
                  {'profit': 4089.0, 'vitemname': 'LVOV REG 1.75LT'}, ....]
    """
    
    itemwise_profit = df.groupby(['vitemcode'], as_index=False). \
                                    agg({'nunitprice':np.average, 'ncostprice':np.average, 'ndebitqty': np.sum})

    itemwise_profit['profit'] = round(((itemwise_profit['nunitprice'] - itemwise_profit['ncostprice'])
                             * itemwise_profit['ndebitqty']), 2)
    itemwise_profit = itemwise_profit.sort_values(by='profit', ascending=False).head(10)
    itemwise_profit.insert(1, 'vitemname', itemwise_profit['vitemcode'].apply(lambda x: itemcode2name[x]))
    
    return itemwise_profit[['vitemname', 'profit']].to_dict(orient='records')








if __name__=='__main__':
    
    STORE='u100062'                                  
    daily_sales = get_daily_sales_data(STORE)
    sales_details, itemcode2name = load_n_process_salesdetail_data(STORE)
    
    print('grouped bar chart') 
    print(get_monthly_sales_yearwise_data(daily_sales))
    print('monthly sales trend line chart' )
    print(get_monthly_sales_data(daily_sales))
    print('bar chart')
    print(top10_items_based_on_sales(sales_details, itemcode2name))
    print('bar chart')
    print(top10_items_based_on_profit(sales_details, itemcode2name))







