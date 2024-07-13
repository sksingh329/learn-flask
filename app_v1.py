import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)

@app.get("/stores")
def get_stores():
    return {"stores": list(stores.values())}

@app.post("/stores")
def create_store():
    store_data = request.get_json()
    
    if( "name" not in store_data ):
        abort(
            400,
            message= "Bad request. Ensure name field is there in JSON payload"
        )
    
    for store in stores.values():
        if store["name"] == store_data["name"]:
            abort(
                409,
                message= "Conflict. Stoe with same name already exist."
            )

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store,201


@app.get("/stores/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, messag="Store not found")


@app.delete("/stores/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, messag="Store not found")


@app.post("/items") 
def create_item():
    item_data = request.get_json()

    if (
        "price" not in item_data
        or "storeId" not in item_data
        or "name" not in item_data
    ):
        abort(400, 
              message= "Bad request. Ensure price, storeId and name is in JSON paylaod")
        
    for item in items.values():
        if(
            item["price"] == item_data["price"]
            and item["storeId"] == item_data["storeId"] 
        ):
            abort(
                409,
                message= "Conflict - Item already exist for store"
            )

    if item_data["storeId"] not in stores:
        abort(404, messag="Store not found")
    
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201


@app.get("/items")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/items/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, messag="Item not found")

@app.put("/items/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data and "name" not in item_data:
        abort(400, message = "Bad request. Ensure 'price' and 'name' is included in JSON paylaod.")
    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message = "Item not found")

@app.delete("/items/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, messag="Item not found")