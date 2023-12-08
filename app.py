from flask import Flask,request
import uuid
from db import items,stores
from flask_smorest import abort

app=Flask(__name__)

stores=[{
    'name':'store1',
    'items':[{
        'item_name':'chair',
        'price':70
    }]
}]


@app.get("/store")
def get_stores():
    return{"Stores":list(stores.values())}

@app.post("/store")
def create_store():
    store_data=request.get_json()
    store_id =  uuid.uuid4().hex
    new_store={**store_data,"id":store_id}
    stores[store_id]=new_store
    return new_store,201

# @app.post("/store/<string:name>/item")
# def store_item(name):
#     request_data=request.get_json()
#     for store in stores:
#         if store['name']==name:
#             new_item={"item_name":request_data['item_name'],'price':request_data['price']}
#             store['items'].append(new_item)
#             return new_item, 201
#
#     return {"message":"store not found"},404

@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        abort(404,message = "Store not found")
    item_id=uuid.uuid4().hex
    new_item = {**item_data,"id":item_id}
    items[item_id]=new_item
    return new_item,201

@app.get("/store")
def get_all_items():
    return{"items":list(items.values())}

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404,message = "Store not found")

@app.get("/item/<string:item_id>")
def get_items(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404,message = "item not found")



