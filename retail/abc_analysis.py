import numpy as np
import pandas as pd
import os
import warnings

#PATH = 'data/'
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/')

def load_n_process_salesdetail_data(store='u100062'):
    
    sales_details = pd.read_csv(PATH+'{}_trn_salesdetail.csv'.format(store), 
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

def get_saleswise_abc_data(sales_details, code2name):
    
    itemwise_sales = sales_details.groupby(['vitemcode'], as_index=False). \
                        agg({'nunitprice':np.average, 'ndebitqty': np.sum})
    itemwise_sales['totalsales'] = itemwise_sales['nunitprice'] * itemwise_sales['ndebitqty']
    itemwise_sales = itemwise_sales.sort_values(by='totalsales', ascending=False)
    itemwise_sales['cumulativesales'] = itemwise_sales['totalsales'].cumsum()
    itemwise_sales['%sales'] = (itemwise_sales['cumulativesales']/itemwise_sales['totalsales'].sum())
    
    itemwise_sales['ABC_category'] = itemwise_sales['%sales']. \
                                     apply(lambda x: 'A' if x < 0.71 
                                          else 'B' if (x >= 0.71 and x < 0.91)
                                          else 'C')
        
    itemwise_sales.insert(1, 'vitemname', itemwise_sales['vitemcode'].apply(lambda x : code2name[x]))

    return itemwise_sales

def get_abc_cat_data(df):
    
    temp = df['ABC_category'].value_counts().reset_index(). \
           rename(columns={'index':'cat', 'ABC_category':'counts'})    
        
    return dataframe_to_json(temp)   


def get_sales_abc_cat_data(sales_abc):
    """
    input: df => pandas dataframe
    output: [{'cat': 'C', 'counts': 3756},....]
    """
    
    return get_abc_cat_data(sales_abc)


def get_profitwise_abc_data(sales_details, code2name):
    
    itemwise_profit = sales_details.groupby(['vitemcode'], as_index=False). \
                        agg({'nunitprice':np.average, 'ncostprice':np.average, 'ndebitqty': np.sum})
    itemwise_profit['profit'] = ((itemwise_profit['nunitprice'] - itemwise_profit['ncostprice'])
                             * itemwise_profit['ndebitqty'])
    itemwise_profit = itemwise_profit.sort_values(by='profit', ascending=False)
    itemwise_profit['cumulative_profit'] = itemwise_profit['profit'].cumsum()
    total_profit = itemwise_profit['profit'].sum()
    itemwise_profit['%profit'] = (itemwise_profit['cumulative_profit'] / total_profit)
    itemwise_profit['ABC_category'] = itemwise_profit['%profit'].apply(lambda x: 'A' if x < 0.71 
                                                                 else 'B' if (x >= 0.71 and x < 0.91)
                                                                 else 'C')
    itemwise_profit.insert(1, 'vitemname', itemwise_profit['vitemcode'].apply(lambda x : code2name[x]))
    
    return itemwise_profit
    


def get_profit_abc_cat_data(profit_abc):
    
    """
    input: df => pandas dataframe
    output: [{'cat': 'C', 'counts': 3756},....]
    """
    
    return get_abc_cat_data(profit_abc)

def dataframe_to_json(df):
    
    return df.to_dict(orient='records')

    
    
def get_abc_a_cat_table(sales_abc, profit_abc, code2name):
    
    """
    input: sales_abc:dataframe profit_abc:dataframe, code2name:dict
    output: json [{'ABC_category_profit': 'C',  'ABC_category_sales': 'A',  'profit': 0.0,
    'profit_sales_ratio': 0.0,  'totalsales': 952.7199999999999,  'vitemcode': '087236100612',
    'vitemname': 'MACALLAN 12 1.75LT'},......]
    """
    
    join_abc = pd.merge(sales_abc[['vitemcode', 'totalsales', 'ABC_category']],
         profit_abc[['vitemcode', 'profit', 'ABC_category']],
        on = 'vitemcode', how='left')
    join_abc.insert(1, 'vitemname', join_abc['vitemcode'].apply(lambda x : code2name[x]))
    
    temp = join_abc[join_abc['ABC_category_x'] == 'A'].copy()
    temp = temp.rename(columns={'ABC_category_x':'ABC_category_sales', 'ABC_category_y':'ABC_category_profit'})
    temp['totalsales'] = round(temp['totalsales'], 2)
    temp['profit'] = round(temp['profit'],1)
    temp['profit_sales_ratio'] = round((temp['profit']/temp['totalsales'])*100)
    
    temp = temp.sort_values(by='profit_sales_ratio')    
   
    return dataframe_to_json(temp)



if __name__=='__main__':
    
    STORE='u100062'
    sales_details, code2name = load_n_process_salesdetail_data(STORE)    
    sales_abc = get_saleswise_abc_data(sales_details, code2name)
    profit_abc = get_profitwise_abc_data(sales_details, code2name)
    
    
    print(get_sales_abc_cat_data(sales_abc))
    print(get_profit_abc_cat_data(profit_abc))
    print(get_abc_a_cat_table(sales_abc, profit_abc, code2name)[:2])
    










