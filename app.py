from flask import Flask,request
import uuid
from db import items,stores
from flask_smorest import abort

app=Flask(__name__)

# stores=[{
#     'name':'store1',
#     'items':[{
#         'item_name':'chair',
#         'price':70
#     }]
# }]


@app.get("/store")
def get_stores():
    return{"Stores":list(stores.values())}



@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404,message = "Store not found")


@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in the JSON payload.",
        )
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"Store already exists.")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store

    return store

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return{"message":"store deleted"}
    except KeyError:
        abort(404,message="store not found")

# @app.post("/store/<string:name>/item")
# def store_item(name):
#     for store in stores:
#         if store['name']==name:
#             new_item={"item_name":request_data['item_name'],'price':request_data['price']}
#             store['items'].append(new_item)
#             return new_item, 201
#
#     return {"message":"store not found"},404

@app.get("/item")
def get_all_items():
    return{"items":list(items.values())}


@app.get("/item/<string:item_id>")
def get_items(item_id):
    try:
        return items[item_id],201
    except KeyError:
        abort(404,message = "item not found")

@app.post("/item")
def create_item():
    item_data = request.get_json()

    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
        )
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"Item already exists.")

    item_id=uuid.uuid4().hex
    new_item = {**item_data,"id":item_id}
    items[item_id]=new_item
    return new_item,201

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data=request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort (400,message="price/name not found.")
    try:
        item=items[item_id]
        item |= item_data
        
        return item
    except KeyError:
        abort(404, message="Item not found.")

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message":"item deleted"}
    except KeyError:
        abort(404,message = "item not found")


