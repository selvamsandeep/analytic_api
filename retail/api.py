from flask.views import MethodView
from flask import jsonify, request, abort, render_template
import os

from user.decorators import user_required

#import for sales insight page
from retail.sales_visualization import get_daily_sales_data, load_n_process_salesdetail_data
from retail.sales_visualization import get_monthly_sales_yearwise_data, get_monthly_sales_data #api
from retail.sales_visualization import top10_items_based_on_sales, top10_items_based_on_profit #api

#inport for abc analusis page
#from retail.abc_analysis  import load_n_process_salesdetail_data
from retail.abc_analysis import get_saleswise_abc_data, get_profitwise_abc_data
from retail.abc_analysis import get_sales_abc_cat_data, get_profit_abc_cat_data #api
from retail.abc_analysis import get_abc_a_cat_table #api

# import for market basket analysis
from retail.market_basket_analysis import create_cooccurance_matirx
from retail.market_basket_analysis import get_top20_items, get_items_purchased_along

#import for sales forecast page 
from retail.sales_forecast import load_propet_forecast_data_n_model
from retail.sales_forecast import get_hist_and_pred_data
from retail.sales_forecast import get_next_sevedays_pred_data, get_current_next_month_pred_data

#update data 
#from retail.update_data_schedule import run_main
#run_main()

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/')
STORE='u100062'

#salees visualize page data 
daily_sales = get_daily_sales_data(STORE)
sales_details, code2name = load_n_process_salesdetail_data(STORE)
#print()

#abc analysis
#sales_details, code2name = load_n_process_salesdetail_data(STORE)    
sales_abc = get_saleswise_abc_data(sales_details, code2name)
profit_abc = get_profitwise_abc_data(sales_details, code2name)

#market basket analysis
cc_matrix= PATH + 'cc_matrix.npy'
X, item2idx, idx2item, code2name = create_cooccurance_matirx(cc_matrix, STORE)

#sales forcast page
forecast, m = load_propet_forecast_data_n_model()#

"""-------------api for sales insight visual page with 4 plots------------- """
class TopSalesItemsAPI(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)    
    
    def get(self, name):
        try:
            result = top10_items_based_on_sales(sales_details, code2name)
        except Exception as e:
            #print (str(e))
            result=None
            error = str(e)

        if not result:
            return jsonify({"error": error}), 404

        return jsonify({"top10_items_based_on_sales": result}), 201 

    def post(self, name):
        pass

class TopProfitItemsAPI(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)
        
    def get(self, name):
        #print('in top10 item profit api')        
        try:
            #print(sales_details_df.shape) 
            result = top10_items_based_on_profit(sales_details, code2name)
        except Exception as e:
            #print (str(e))
            result=None
            error = str(e)

        if not result:
            return jsonify({"error": error}), 404

        return jsonify({"top10_items_based_on_profit": result}), 201 

    def post(self, name):
        pass

class YearlySalesAPI(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)
        
    def get(self, name):
        try:
            result = get_monthly_sales_yearwise_data(daily_sales)
        except Exception as e:
            #print (str(e))
            result=None
            error = str(e)
        if not result:
            return jsonify({"error": error}), 404

        return jsonify({"monthly_sales_yearwise": result}), 201 

    def post(self, name):
        pass

        
class MonthlySalesAPI(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)
    
    
    def get(self, name):
        try:
            result = get_monthly_sales_data(daily_sales)
        except Exception as e:
            #print (str(e))
            result=None
            error = str(e)
        if not result:
            return jsonify({"error": error}), 404

        return jsonify({"monthly_sales": result}), 201

    def post(self, name):
        pass

"""-------------api for abc analysis visual page with 2 plots and 1 table------------- """
#for pie chart
class AbcOnsalesAPI(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)    
    
    def get(self, name):
        try:
            result = get_sales_abc_cat_data(sales_abc)
        except Exception as e:
            #print (str(e))
            result=None
            error = str(e)
        if not result:
            return jsonify({"error": error}), 404

        return jsonify({"customerise aggregated sales": result}), 201 

    def post(self, name):
        pass

#for pie chart
class AbcOnProfitAPI(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)
        
    def get(self, name):
        try:
            result = get_profit_abc_cat_data(profit_abc)
        except Exception as e:
            #print (str(e))
            result=None
            error = str(e)
        if not result:
            return jsonify({"error": error}), 404

        return jsonify({"item wise aggregated sales": result}), 201 

    def post(self, name):
        pass


# table for comparting ABC categories on sales and profit
class ABCcatTableAPI(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)
        
    def get(self, name):
        try:
            result = get_abc_a_cat_table(sales_abc, profit_abc, code2name)
        except Exception as e:
            #print (str(e))
            result=None
            error = str(e)

        if not result:
            return jsonify({"error": error}), 404

        return jsonify({"monthly sales": result}), 201

    def post(self, name):
        pass


""" ---------------Market basket analysis bobble chrage for items purhased along---------"""

class MarketBasketAPI(MethodView):

    decorators = [user_required]

    def __init__(self): 

        self.top20_items = get_top20_items(X, code2name, idx2item)      
        if (request.method != 'GET') and not request.json:          
            abort(400)

    def get(self, name): 
        try: 
            result = self.top20_items
        except Exception as e:
            error = str(e)
            result=None
        if not result:
            return jsonify({"error": error}), 404

        return jsonify({"top20items":result}), 201

    
    def post(self, name):

        # item = top10_item[9]
        if not "item_id" in request.json:
            error = {
                "code": "MISSING_ITEM_ID_"
            }
            return jsonify({'error': error}), 400

        data= request.get_json() #force=True silent=True. can be used 
        #print (data['f_date'])
        #print (data)
        try:
            print ('in')  
            print(data["item_id"])          
            #item = self.top20_items[1]
            item = self.top20_items[int(data["item_id"])]
            print(item)            
            #item = self.top20_items[int(data["item_id"])]           
            result = get_items_purchased_along(item, X, code2name, item2idx, idx2item)           
        except Exception as e:
            error = str(e)
            result=None
            #print (str(e))
        print(result[0])
        if not result:
            return jsonify({"error":error}), 404

        return jsonify({"Items_purchaed_along ":result}), 201 



"""-------------api sales forecase next days table, current & next month and data trend plot------------- """
#for table next seven days sales preodictions
class PredNextSevenDaysAPI(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)    
    
    def get(self, name):
        try:
            result = get_next_sevedays_pred_data(forecast)
        except Exception as e:
            print (str(e))
            error = str(e)
        if not result:
            return jsonify({"error": error}), 404

        return jsonify({"next_seven_day_forecast": result}), 201 

    def post(self, name):
        pass

#for table for current and next month preditons
class PredTwoMonthsAPI(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)
        
    def get(self, name):
        try:
            result = get_current_next_month_pred_data(forecast)
        except Exception as e:
            print (str(e))
            error = str(e)
        if not result:
            return jsonify({"error": error}), 404

        return jsonify({"current_and_next_month_sales": result}), 201 

    def post(self, name):
        pass


# plot for histroric and predciton data
class HistNPredAPI(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)
        
    def get(self, name):
        try:
            result = get_hist_and_pred_data(forecast, m)
        except Exception as e:
            print (str(e))
            error = str(e)
            result=None

        if not result:
            return jsonify({"error": error}), 404

        return jsonify({"monthly sales": result}), 201

    def post(self, name):
        pass


        