import numpy as np
import pandas as pd
import mysql.connector as sql
import time
import logging
import os

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

#STORE_DB = 'u100068'
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/')

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        logging.info('{0} Store DB: {1}, Table: {2} Time taken: {3:.2f} sec'. \
                     format(method.__name__,  kw['store_db'], kw['table'],te-ts))    
        return result

    return timed

def create_db_connection(store_db):
    db_connection = sql.connect(
        host='devalberta.cfixtkqw8bai.us-east-2.rds.amazonaws.com', 
        database=store_db, 
        user='alberta', 
        password='Jalaram123$')
    return db_connection    
#db_connection = create_db_connection(STORE_DB)

@timeit
def download_and_save_data(con, store_db, table):    
    
    try:
        df = pd.read_sql('SELECT * FROM ' + table, con=con)
    except Exception as e:
        print(e)
        con.close()
    #romve constant column
    temp = df.nunique().reset_index().rename(columns={'index':'column_name', 0:'values'})
    cols = temp[temp['values'] > 1]['column_name'].tolist()
    df = df[cols]
    df.to_csv(PATH+'{0}_{1}.csv'.format(STORE_DB, table), index=False)
    #return df
    
    
if __name__=='__main__':
    
    #STORE_DB = 'u100068'
    #db_connection = create_db_connection(store_db=STORE_DB) 
    #download_and_save_data(store_db=STORE_DB, table='trn_sales')
    #download_and_save_data(store_db=STORE_DB, table='trn_salesdetail')
    #download_and_save_data(store_db=STORE_DB, table='mst_item')   
    #db_connection.close()
    
    STORE_DB = 'u100062'
    db_connection = create_db_connection(store_db=STORE_DB)  
    download_and_save_data(db_connection, store_db=STORE_DB, table='trn_sales')
    download_and_save_data(db_connection, store_db=STORE_DB, table='trn_salesdetail')
    download_and_save_data(db_connection, store_db=STORE_DB, table='mst_item')    
    db_connection.close()




