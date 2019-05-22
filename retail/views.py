from flask import Blueprint
#sales Insight page
from retail.api import TopSalesItemsAPI, TopProfitItemsAPI
from retail.api import YearlySalesAPI, MonthlySalesAPI
from retail.api import AbcOnsalesAPI, AbcOnProfitAPI, ABCcatTableAPI
from retail.api import MarketBasketAPI
from retail.api import PredNextSevenDaysAPI, PredTwoMonthsAPI, HistNPredAPI



retail_app = Blueprint('retail_app', __name__)

# route for sales  Insige page 4 plots
top_sales_item_view = TopSalesItemsAPI.as_view('top_sales_item_api')
retail_app.add_url_rule('/top10_items_on_sales/<name>', view_func=top_sales_item_view, methods=['GET',])
top_profit_item_view = TopProfitItemsAPI.as_view('top_profit_item_api')
retail_app.add_url_rule('/top10_items_on_profit/<name>', view_func=top_profit_item_view, methods=['GET',])
yearly_sales_view  = YearlySalesAPI.as_view('yearly_sales_api')
retail_app.add_url_rule('/get_monthly_sales_yearwise/<name>', view_func=yearly_sales_view, methods=['GET',])
monthly_sales_view = MonthlySalesAPI.as_view('montly_sales_api')
retail_app.add_url_rule('/get_monthly_sales/<name>', view_func=monthly_sales_view, methods=['GET', ])

#route for abc analysis 2 pie chart and one table
abc_on_sales_view = AbcOnsalesAPI.as_view('acb_on_sales_api')
retail_app.add_url_rule('/get_sales_abc_cat/<name>', view_func=abc_on_sales_view, methods=['GET',])
abc_on_profit_view = AbcOnProfitAPI.as_view('abc_on_profit_api')
retail_app.add_url_rule('/get_profit_abc_cat/<name>', view_func=abc_on_profit_view, methods=['GET',])
abc_cat_table_view = ABCcatTableAPI.as_view('abc_cat_table_view')
retail_app.add_url_rule('/get_abc_a_cat_table/<name>', view_func=abc_cat_table_view, methods=['GET',])

# market basket analysis page GET top items and POST items purchased alongs
market_basket_view = MarketBasketAPI.as_view('market_basket_api')
retail_app.add_url_rule('/items_purchsed_along/<name>', view_func=market_basket_view, methods=['GET','POST', ])

#sales forcast next 7 days table, 2 months forcast table and trend plot
next_7days_pred_view = PredNextSevenDaysAPI.as_view('next_7days_pred_view_api')
retail_app.add_url_rule('/get_next_sevedays_pred/<name>', view_func=next_7days_pred_view, methods=['GET',])
two_months_pred_view = PredTwoMonthsAPI.as_view('two_months_pred_api')
retail_app.add_url_rule('/get_curr_next_month_pred/<name>', view_func=two_months_pred_view, methods=['GET',])
hist_n_pred_view = HistNPredAPI.as_view('hist_n_pred_api')
retail_app.add_url_rule('/get_hist_and_pred/<name>', view_func=hist_n_pred_view, methods=['GET',])

