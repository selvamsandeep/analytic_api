from flask.views import MethodView
from flask import jsonify, request, abort, render_template


from user.decorators import user_required


from distribution.itemwise_purchase_model import create_item_party_qty_matrix
from distribution.itemwise_purchase_model import customers_going_to_buy
from distribution.itemwise_purchase_model import items_to_be_purchased
from distribution.dashboard_data import create_dataframe, partywise_aggregated_sales
from distribution.dashboard_data import itemwise_aggregated_salse_in_amt
from distribution.dashboard_data import montly_sales, quaterly_sales
from distribution.dashboard_data import get_item_monthly_sales,item_qty_sold_to_party
from distribution.dashboard_data import get_party_monthly_sales,party_puchased_items_qty

#import for retail api

X, item2idx, idx2item, party2idx, idx2party = create_item_party_qty_matrix()
data_frame = create_dataframe()
print(data_frame.shape)

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

parties = {1:'KSM Poultry Farm',
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

class ItemsAPI(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:          
            abort(400)

    def get(self, name): 
        
        return jsonify({"top10item":top10_item})

    
    def post(self, name):

        # item = top10_item[9]
        if not "item_id" in request.json:
            error = {
                "code": "MISSING_ITEM_ID_"
            }
            return jsonify({'error': error}), 400

        data= request.get_json() #force=True silent=True. can be used 
        #print (data['f_date'])
        print (data)
        try:
            print ('in')
            result=customers_going_to_buy(top10_item[int(data['item_id'])], X,  item2idx, idx2party)            
        except Exception as e:
            print (str(e))

        return jsonify({"Probable_Customers ":result}), 201 if result else 404

class ItemsAPI1(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)
    
    
    def get(self,name):
        pass
    
    def post(self,name):

        if not "item_id" in request.json:
            error = {
                "code": "MISSING_ITEM_ID_"
            }
            return jsonify({'error': error}), 400

        data= request.get_json() #force=True silent=True. can be used 
        print (data)        
        try:
            print ('in')            
            result= get_item_monthly_sales(top10_item[int(data['item_id'])], data_frame)
        except Exception as e:
            print (str(e))

        return jsonify({"item montly sales ":result}), 201 if result else 404


class ItemsAPI2(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)
    
    
    def get(self,name):
        pass
    
   
    def post(self,name):

        if not "item_id" in request.json:
            error = {
                "code": "MISSING_ITEM_ID_"
            }
            return jsonify({'error': error}), 400

        data= request.get_json() 
        #print(data)    
       
        try:           
            print ('in')
            party_list = customers_going_to_buy(top10_item[int(data['item_id'])], X, item2idx, idx2party)             
            result= item_qty_sold_to_party(top10_item[int(data['item_id'])], party_list, data_frame)
            #print(result)
            #print(json.dumps(result))
        except Exception as e:
            print (str(e))

        return jsonify({"item purchaed by customers":result}), 201 if result else 404

        
class PartyAPI(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)
    
    
    def get(self,name): 

        return jsonify({"top10paries":parties})

    
    def post(self,name):

        # item = top10_item[9]
        if not "party_id" in request.json:
            error = {
                "code": "MISSING_PARTY_ID_"
            }
            return jsonify({'error': error}), 400

        data= request.get_json() #force=True silent=True. can be used 
        #print (data['f_date'])
        print (data)
        try:
            print ('in')
            result=items_to_be_purchased(parties[int(data['party_id'])], X,  idx2item, party2idx)            
        except Exception as e:
            print (str(e))

        return jsonify({"Possible_items ":result}), 201 if result else 404

class PartyAPI1(MethodView):
    
    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)

    def get(self,name):
        pass

    
    def post(self,name):   

        if not "party_id" in request.json:
            error = {
                "code": "MISSING_PARTY_ID_"
            }
            return jsonify({'error': error}), 400

        data= request.get_json() #force=True silent=True. can be used 
        print (data)
        try:
            print ('in')            
            result= get_party_monthly_sales(parties[int(data['party_id'])], data_frame)
        except Exception as e:
            print (str(e))

        return jsonify({"party montly sales":result}), 201 if result else 404


class PartyAPI2(MethodView):
    
    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)
    

    def get(self,name):
        pass

    
    def post(self,name):
        data= request.get_json() 
        print(data)    
       
        try:           
            print ('in')
            item_list = items_to_be_purchased(parties[int(data['party_id'])], X,  idx2item, party2idx)
            result= party_puchased_items_qty(parties[int(data['party_id'])], item_list, data_frame)
            #print(result)
            #print(json.dumps(result))
        except Exception as e:
            print (str(e))

        return jsonify({"party purchaed by items qty":result}), 201 if result else 404



class VisualAPI1(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)    
    
    def get(self, name):
        try:
            result = partywise_aggregated_sales(data_frame)
        except Exception as e:
            print (str(e))

        return jsonify({"customerise aggregated sales": result}), 201 if result else 404

    def post(self, name):
        pass

class VisualAPI2(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)
        
    def get(self, name):
        try:
            result = itemwise_aggregated_salse_in_amt(data_frame)
        except Exception as e:
            print (str(e))

        return jsonify({"item wise aggregated sales": result}), 201 if result else 404

    def post(self, name):
        pass

class VisualAPI3(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)
        
    def get(self, name):
        try:
            result = montly_sales(data_frame)
        except Exception as e:
            print (str(e))

        return jsonify({"monthly sales": result}), 201 if result else 404

    def post(self, name):
        pass

        
class VisualAPI4(MethodView):

    decorators = [user_required]

    def __init__(self):       
        if (request.method != 'GET') and not request.json:
            abort(400)
    
    
    def get(self, name):
        try:
            result = quaterly_sales(data_frame)
        except Exception as e:
            print (str(e))

        return jsonify({"quterly sales": result}), 201 if result else 404
	
    def post(self, name):
        pass
    
