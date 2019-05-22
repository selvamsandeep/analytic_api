from flask import Blueprint

from distribution.api import ItemsAPI, ItemsAPI1, ItemsAPI2
from distribution.api import PartyAPI, PartyAPI1, PartyAPI2
from distribution.api import VisualAPI1, VisualAPI2, VisualAPI3, VisualAPI4

distribution_app = Blueprint('distribution_app', __name__)

#Item wise pridiction  page
item_view = ItemsAPI.as_view('item_api')
distribution_app.add_url_rule('/items/<name>', view_func=item_view, methods=['GET','POST',])
item_view1 = ItemsAPI1.as_view('item_api1')
distribution_app.add_url_rule('/get_item_monthly_sales/<name>', view_func=item_view1, methods=['POST',])
item_view2 = ItemsAPI2.as_view('item_api2')
distribution_app.add_url_rule('/item_qty_sold_to_party/<name>', view_func=item_view2, methods=['POST',])

#Party wise pridiction page
party_view = PartyAPI.as_view('party_api')
distribution_app.add_url_rule('/parties/<name>', view_func=party_view, methods=['GET','POST',])
party_view1 = PartyAPI1.as_view('party_api1')
distribution_app.add_url_rule('/get_party_monthly_sales/<name>', view_func=party_view1, methods=['POST',])
party_view2 = PartyAPI2.as_view('party_api2')
distribution_app.add_url_rule('/party_puchased_items_qty/<name>', view_func=party_view2, methods=['POST',])

#sales insights page
visual_view1 = VisualAPI1.as_view('visual_api1')
distribution_app.add_url_rule('/partywise_aggregated_sales/<name>', view_func=visual_view1, methods=['GET',])
visual_view2 = VisualAPI2.as_view('visual_api2')
distribution_app.add_url_rule('/itemwise_aggregated_salse_in_amt/<name>', view_func=visual_view2, methods=['GET',])
visual_view3 = VisualAPI3.as_view('visual_api3')
distribution_app.add_url_rule('/montly_sales/<name>', view_func=visual_view3, methods=['GET',])
visual_view4 = VisualAPI1.as_view('visual_api4')
distribution_app.add_url_rule('/quaterly_sales/<name>', view_func=visual_view4, methods=['GET',])
