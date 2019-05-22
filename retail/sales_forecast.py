import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
from fbprophet import Prophet
from datetime import datetime
from dateutil import relativedelta
import time
import calendar
import os
import warnings
import pickle


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
    #daily_sales['month_year'] = daily_sales['date'].dt.to_period('M').astype('datetime64[ns]')
    daily_sales['year'] = daily_sales.date.dt.year.astype(np.int16)
    
    return daily_sales 


def make_forecast(df, preiods=180):
    
    pkl_path = PATH + 'propeht_model.plk'
    #for prophet requirement date column name ds and data column name y
    daily_ts = df[['date', 'nnettotal']].rename(columns={'date':'ds', 'nnettotal':'y'})
    #print(daily_ts.head(4))
    
    m = Prophet(daily_seasonality=False)
    m.add_country_holidays(country_name='US')
    m.fit(daily_ts)
    future = m.make_future_dataframe(periods=180)
    
    forecast = m.predict(future)
    forecast.to_csv(PATH + 'forecast.csv', index=False)
    
    with open(pkl_path, "wb") as f:    
        pickle.dump(m, f)
    
def load_propet_forecast_data_n_model():
    pkl_path = PATH + 'propeht_model.plk'
    
    df = pd.read_csv(PATH + 'forecast.csv', parse_dates=['ds'])
    
    with open(pkl_path, 'rb') as f:
        model = pickle.load(f)

    return df, model

def get_hist_and_pred_data(fcast, m):
    """
    Input: fcast, dataframe from fbprophet forecast
    Output: json [{
                'history': [{'ds': '18-03-2019', 'y': 4180.79},
                              {'ds': '19-03-2019', 'y': 4398.41},..],                   
                'prediction':[{'ds': '07-05-2019','yhat': 4073.61,'yhat_lower': 1310.38,'yhat_upper': 7023.90},
                                {'ds': '08-05-2019','yhat': 4636.79,'yhat_lower': 1716.99,'yhat_upper': 7369.18},.]
                  }] 
    """
    
    last_date = m.history['ds'].values[-1].astype(str)[:10]
    fcast = fcast[fcast['ds'] > last_date][['ds', 'yhat', 'yhat_lower', 'yhat_upper']]   
        
    hist = m.history[m.history['ds'] > '2017-12-31'][['ds', 'y']]    
    fcast['ds'] = fcast['ds'].map(lambda x: x.strftime('%d-%m-%Y'))
    hist['ds'] = hist['ds'].map(lambda x: x.strftime('%d-%m-%Y'))
    
    fcast, hist = fcast.round(2), hist.round(2)
    #return fcast, hist
    return [{"prediction": fcast.to_dict(orient='records') , 
             "history": hist.to_dict(orient='records')}]

def get_next_sevedays_pred_data(fcast):
    """
    Input: fcast => dataframe from fbprophet forecast
    
    Output: seven days daily data in json
                [{'ds': '10-05-2019', 'prediction': 9208.75,  'lower': 6446.99,  'upper': 11969.76},
    """
    
    cur_dt = datetime.today().strftime('%Y-%m-%d')
    df = fcast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    df = df[df['ds'] > cur_dt].head(7)
    df['ds'] = df['ds'].map(lambda x: x.strftime('%d-%m-%Y'))
    df = df.rename(columns={'yhat_lower':'lower', 'yhat':'prediction', 'yhat_upper':'upper'})
    df = df.round()
    return df.to_dict(orient='record')

def get_current_next_month_pred_data(fcast):
    """
    Input: fcast => dataframe from fbprophet forecast
    
    Output: seven days daily data in json
            [{'lower': 5062.49, 'month_year': 'June-2019',  'prediction': 7922.49,  'upper': 10846.83},..]
    
    """    
    
    curr_date = datetime.today()
    curr_month = curr_date.strftime('%B-%Y')
    next_month = (curr_date + relativedelta.relativedelta(months=1)).strftime('%B-%Y')
    #print(curr_month, next_month)
    df = fcast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
    
    df['month_year'] = df['ds'].apply(lambda x : x.strftime('%B-%Y'))
    df = df[df['month_year'].isin([curr_month, next_month])].copy()
    
    df = df.groupby('month_year', as_index=False). \
            agg({'yhat':np.average, 'yhat_lower':np.average, 'yhat_upper':np.average})
    df = df.rename(columns={'yhat_lower':'lower', 'yhat':'prediction', 'yhat_upper':'upper'})
    df = df.round()
    return df.to_dict(orient='record')



if __name__=='__main__':
   
    STORE='u100062'
    
    #daily_sales = get_daily_sales_data(STORE)
    #make_forecast(daily_sales)
    forecast, m = load_propet_forecast_data_n_model()#load model
    
    res = get_hist_and_pred_data(forecast, m) #api
    print(res[0]["history"][:2])
    print('\n')
    print(res[0]["prediction"][:2])
    print('\n')
    print(get_next_sevedays_pred_data(forecast)[:2])#api
    print('\n')
    print(get_current_next_month_pred_data(forecast))#api
    
     

