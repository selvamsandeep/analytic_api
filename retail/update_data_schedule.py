import schedule
import time
import os
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

from retail.grab_data_sqldb_save import create_db_connection,download_and_save_data
from retail.sales_forecast import get_daily_sales_data, make_forecast
from retail.market_basket_analysis import create_cooccurance_matirx

STORE_DB = 'u100062'
#PATH = 'data/'
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/')

def download_data():    
    
    db_connection = create_db_connection(store_db=STORE_DB)  
    download_and_save_data(db_connection, store_db=STORE_DB, table='trn_sales')
    download_and_save_data(db_connection, store_db=STORE_DB, table='trn_salesdetail')
    download_and_save_data(db_connection, store_db=STORE_DB, table='mst_item')    
    db_connection.close()
    
def create_cooccurance_matirx():
    cc_matrix= PATH + 'cc_matrix.npy'
    try:
        os.remove(cc_matrix)
    except:
        pass
    _, _, _, _ = create_cooccurance_matirx(cc_matrix, STORE_DB)
   
    
def run_prophet_model():
    daily_sales = get_daily_sales_data(STORE_DB)
    make_forecast(daily_sales)
    
def run_main():
    schedule.every().day.at("07:00").do(download_data)  
    schedule.every().day.at("07:15").do(create_cooccurance_matirx) 
    schedule.every().day.at("07:18").do(run_prophet_model)  
    while True:
        schedule.run_pending()
        time.sleep(1)
    
if __name__=='__main__':
        
    run_main()