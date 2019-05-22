import numpy as np
import pandas as pd
import os
import pickle
import operator

#PATH = 'data/'
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'retail_data/')

def create_itemcodes_list(store='u100062'):
    
    trn_sales_details =pd.read_csv(PATH+'{}_trn_salesdetail.csv'.format(STORE), low_memory=False)

    trn_sales_details['vitem_len'] = trn_sales_details['vitemcode'].apply(lambda x : len(x))

    sales_details = trn_sales_details[trn_sales_details['vitem_len'] > 2]
    

    items_groups = sales_details[['isalesid', 'vitemcode', 'vitemname']].groupby(['isalesid'], as_index=False). \
                    agg(lambda x : ','.join(x))


    items_groups['vitemcode'] = items_groups['vitemcode'].apply(lambda x : x.split(','))
    items_groups['vitemname'] = items_groups['vitemname'].apply(lambda x : x.split(','))

    items_groups['vitemcode'] = items_groups['vitemcode'].apply(lambda x: list(set(x)))
    items_groups['vitemname'] = items_groups['vitemname'].apply(lambda x: list(set(x)))

    items_groups['num_items'] = items_groups['vitemcode'].apply(lambda x : len(x))

    vitemcodes_list = items_groups.vitemcode.tolist()
    
    
    mst_item = pd.read_csv(PATH+'{}_mst_item.csv'.format(STORE), low_memory=False)
    
    code2name = {}
    for i in range(mst_item.shape[0]):
        #print(mst_item.vitemcode[i], mst_item.vitemname[i])
        code, name = mst_item.vitemcode[i], mst_item.vitemname[i]
        code2name[code] = name
        
    #itemcodes = list(set(sales__trn_salesdetail.csvdetails.vitemcode.tolist()))
    #add items not in mst_item table and in trn_sales_details tables
    for code, name in zip(sales_details.vitemcode, sales_details.vitemname):
        if code not in code2name:        
            code2name[code] = name
    
    #itemcodes = list(set(sales_details.vitemcode.tolist()))
    itemcodes = [*code2name]
    
    return itemcodes, code2name, vitemcodes_list

def create_dic_item_idx(itemcodes):
    
    item2idx = {}
    idx2item = {}
    for i, item in enumerate(itemcodes):
        item2idx[item] = i
        idx2item[i] = item
        
    return item2idx, idx2item


def create_cooccurance_matirx(cc_matrix=None, store='u100062'):
   
    if not os.path.exists(cc_matrix):
        itemcodes, code2name, vitemcodes_list = create_itemcodes_list(store)
        item2idx, idx2item = create_dic_item_idx(itemcodes)
        mat_sz = len(itemcodes)
        X = np.zeros((mat_sz, mat_sz), dtype=np.int16)
        #x.shape

        for vitems in vitemcodes_list:
            n = len(vitems)
            if n == 1: continue
            for i in range(n):        
                vi = vitems[i]
                for j in range(i+1, n):
                    vj = vitems[j]
                    #print(item2idx[vi], item2idx[vj])
                    X[item2idx[vi], item2idx[vj]] += 1
                    X[item2idx[vj], item2idx[vi]] += 1

        np.save(cc_matrix, X)
        with open(PATH+'item2idx.pkl', 'wb') as handle:
             pickle.dump(item2idx, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(PATH+'idx2item.pkl', 'wb') as handle:
             pickle.dump(idx2item, handle, protocol=pickle.HIGHEST_PROTOCOL)  
        with open(PATH+'code2name.pkl', 'wb') as handle:
             pickle.dump(code2name, handle, protocol=pickle.HIGHEST_PROTOCOL)        
                
    else:
        X = np.load(cc_matrix)
        with open(PATH+'item2idx.pkl', 'rb') as handle:
            item2idx = pickle.load(handle)
        with open(PATH+'idx2item.pkl', 'rb') as handle:
            idx2item = pickle.load(handle)
        with open(PATH+'code2name.pkl', 'rb') as handle:
            code2name = pickle.load(handle)    

   
    return X, item2idx, idx2item, code2name


def get_top20_items(X, code2name, idx2item, freq=100):    
    """
    for GET request 
    Input: X:numpy 2d array, code2name:dict, idx2item:dict,
    Output: {1: 'FRANZISKANER WEISSBIER 16.9OZ BOT',
             2: 'FIREBALL CINNAMON WHISKY 50ML',
             ..................................,
             20: 'COPENHAGEN SNUFF'}
    """
    items = []
    dic = {}
    for i in range(X.shape[1]):
        if X[:, i].max() > freq:
            #print(idx2item[i])
            items.append((code2name[idx2item[i]], X[:, i].max()))
    items.sort(key=operator.itemgetter(1), reverse=True)        
    
    for i, item in enumerate(items):
        #print(i+1, item)
        dic[i+1] = item[0]
        if i+1 >= 20: break
        
    return dic


def  get_items_purchased_along(item, X, code2name, item2idx, idx2item):
    """
    for POST request 
    Input: X:numpy 2d array, code2name:dict, idx2item:dict,
    Output: [{'item': 'FIREBALL CINNAMON WHISKY 50ML', 'qty': 369},
     {'item': 'FIREBALL CINNAMON WHISKY 200ML', 'qty': 98},
    """
    items = []
    res = []
    name2code = {v : k for k, v in code2name.items()}    
    arr = np.nonzero(X[:, item2idx[name2code[item]]] > 1)
    for i in arr[0]:
        #print(code2name[idx2item[i]], X[i, item2idx[name2code[item]]])
        items.append((code2name[idx2item[i]], X[i, item2idx[name2code[item]]]))
    items.sort(key=operator.itemgetter(1), reverse=True) 
    for it in items:
        res.append({'item':it[0], 'qty':float(it[1])})
        
    return res


if __name__=='__main__':
    
    STORE = 'u100062'
    cc_matrix= PATH + 'cc_matrix.npy'
    X, item2idx, idx2item, code2name = create_cooccurance_matirx(cc_matrix, STORE)
    
    top20_items = get_top20_items(X, code2name, idx2item)
    print(top20_items)
    item = top20_items[2]
    print(get_items_purchased_along(item, X, code2name, item2idx, idx2item))





