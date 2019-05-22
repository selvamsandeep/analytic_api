import numpy as np
import pandas as pd
import os,sys
import datetime
import pickle


#DATA_DIR = 'data/'
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'distri_data/')
#DATA_DIR = 'data_dump/'
#DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_dump/')
#print(os.path.dirname(os.path.abspath(__file__)))
#print(DATA_DIR)
#print(os.listdir(DATA_DIR))

def creat_itemiwse_dataframe():
    sales_df = pd.read_excel(DATA_DIR + 'Sales.xls', parse_dates=['Date'])
    sales_df['dayofyear'] = sales_df.Date.dt.dayofyear
    sales_df['week'] = sales_df.Date.dt.week
    
    itemwise_df = sales_df[['Date', 'dayofyear', 'week', 'Item Name', 'Party Name', 'Billed Quantity']].copy()
    
    item_list = list(set(itemwise_df['Item Name']))
    party_list = list(set(itemwise_df['Party Name']))
    
    return itemwise_df, item_list, party_list


def create_item_index_dic(item_list):
    item2idx = {}
    idx2item = {}
    for i, item in enumerate(item_list):
        item2idx[item] = i
        idx2item[i] = item 
        #if i < 5: print(i, item)
        
    return item2idx, idx2item

def create_party_index_dic(party_list):
    party2idx = {}
    idx2party = {}
    for i, party in enumerate(party_list):
        party2idx[party] = i
        idx2party[i] = party 
        #if i < 5: print(i, party)
        
    return party2idx, idx2party 


def create_item_party_qty_matrix():
    
    cc_matrix = DATA_DIR + 'cc_matrix.npy'
    
    if not os.path.exists(cc_matrix):  
        itemwise_df, item_list, party_list = creat_itemiwse_dataframe()
        num_items = len(item_list)
        num_party = len(party_list)
        item2idx, idx2item = create_item_index_dic(item_list)
        party2idx, idx2party = create_party_index_dic(party_list)
        
        X = np.zeros((num_items, num_party, 367), dtype=np.int16)
        for i, row in itemwise_df.iterrows():
            #if i < 5: print(row['dayofyear'], row['Party Name'], row['Item Name'], row['Billed Quantity'])
            X[item2idx[row['Item Name']]][party2idx[row['Party Name']]][row['dayofyear']] += row['Billed Quantity']
            
        np.save(cc_matrix, X)
        with open(DATA_DIR + 'item2idx.pkl', 'wb') as handle:
             pickle.dump(item2idx, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(DATA_DIR + 'idx2item.pkl', 'wb') as handle:
             pickle.dump(idx2item, handle, protocol=pickle.HIGHEST_PROTOCOL)  
        with open(DATA_DIR + 'party2idx.pkl', 'wb') as handle:
             pickle.dump(party2idx, handle, protocol=pickle.HIGHEST_PROTOCOL)     
        with open(DATA_DIR + 'idx2party.pkl', 'wb') as handle:
             pickle.dump(idx2party, handle, protocol=pickle.HIGHEST_PROTOCOL)        
    
    else:
        X = np.load(cc_matrix)
        with open(DATA_DIR + 'item2idx.pkl', 'rb') as handle:
            item2idx = pickle.load(handle)
        with open(DATA_DIR + 'idx2item.pkl', 'rb') as handle:
            idx2item = pickle.load(handle) 
        with open(DATA_DIR + 'party2idx.pkl', 'rb') as handle:
            party2idx = pickle.load(handle)
        with open(DATA_DIR + 'idx2party.pkl', 'rb') as handle:
            idx2party = pickle.load(handle)     
    
    return X, item2idx, idx2item, party2idx, idx2party

def customers_going_to_buy(item, X, item2idx, idx2party):
    """
    input=> item name and date_str in yyyy-mm-dd formate
    output=> list of customers 
    """
    today = datetime.datetime.now()
    dayofyear = (today - datetime.datetime(today.year, 1, 1)).days + 1
    arr = np.nonzero(X[item2idx[item]][:, dayofyear:dayofyear+7])
    
    cust_list =  list(set([idx2party[c] for c in arr[0]]))
    #return cust_lsit
    lst =[]
    for cust in cust_list:
        lst.append({"name":cust})
    
    return lst

def items_to_be_purchased(party, X, idx2item, party2idx):
    """
    input=> item name and date_str in yyyy-mm-dd formate
    output=> list of customers 
    """
    today = datetime.datetime.now()
    dayofyear = (today - datetime.datetime(today.year, 1, 1)).days + 1
    arr = np.nonzero(X[:, party2idx[party],dayofyear:dayofyear+7])
    
    items_list =  list(set([idx2item[i] for i in arr[0]]))
    #return cust_lsit
    lst =[]
    for item in items_list:
        lst.append({"name":item})
    
    return lst

if __name__=='__main__':
    #itemwise_df, item_list, party_list = creat_itemiwse_dataframe()
    #item2idx, idx2item = create_item_index_dic(item_list)
    #party2idx, idx2party = create_party_index_dic(party_list)
    X, item2idx, idx2item, party2idx, idx2party = create_item_party_qty_matrix()
    top10_item = {1:'D L Methionine 99% - 1 Kg', 
                  2:'LIV 52 PROTECH LIQ 5 LTR',
                  3:'G-PROMIN VET 5 LTR',
                  4:'VIMERAL 500 ML',
                  5:'NEODOX FORTE 50 GM',
                  6:'POULTRY FEED DCP 50 KG',
                  7:'L - Lysine 99% - 1 Kg',
                  8:'BROTONE 5 LTR', 
                  9:'IBD PLUS VEB 1000 DS',
                  10:'HEPATO CARE 5 LTR'}

    
    item = top10_item[1]    
    cust_list = customers_going_to_buy(item, X, item2idx, idx2party)
    print(cust_list)
    parties = {
                1:'KSM Poultry Farm',
                2:'Kavi Protein and Feed Pvt Ltd-Krishnagiri',
                3:'Sujatha Poultry Farm',
                4:'D.K Poultry',
                5:'D.K.Poultry (Feed)',
                6:'Nimble Growh Consultancy Services Pvt',
                7:'Chakravarthi Vet Medical & Agencey',
                8:'Manasa Poultry Farm [Dvg]',
                9:'S.L.N. Poultry Farm Cnp',
                10:'Sri Ragavendra Hatcheries Poultry Feeds',
                11:'Kavi Protein And Feed Pvt Ltd'}
    
    party = parties[1]
    item_list = items_to_be_purchased(party, X, idx2item, party2idx)
    print(item_list)
    
    
    
    
    
    
    




