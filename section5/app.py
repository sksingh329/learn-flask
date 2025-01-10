import uuid
from flask import Flask,request # type: ignore
from flask_smorest import abort # type: ignore
from db import stores, items


app = Flask(__name__)

@app.get('/store')
def get_stores():
    return {"stores": list(stores.values())}

@app.post('/store')
def create_store():
    # Here request_data is a dictionary
    store_data = request.get_json()
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in the JSON payload."
        )
    
    for store in stores:
        if store_data["name"] == store["name"]:
            abort(
                400,
                message=f"Store with name store_data['name'] already exist."
            )
    store_id = uuid.uuid4().hex
    # Unpacks all key-value pairs from store_data and adds the id key-value pair
    # Add a new key id wuth valye store_id
    # Creates a new dictionary with all key-value pairs from store_data and adds the id key-value pair
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    # Default status code is 200
    return new_store, 201

@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")


@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted"}
    except KeyError:
        abort(404, message="Store not found")
        

@app.post('/item')
def create_item():
    item_data = request.get_json()
    if(
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request. Ensure 'price', 'store_id' and 'name' are included in the JSON payload."
        )
    for item in items.values():
        if(
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"Item {item_data["name"]} already exist for store {item_data["store_id"]}")

    print(f"Checking stores before {item_data['store_id']}")
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")
    print(f"Checking stores after {item_data['store_id']}")
    
    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id": item_id}
    items[item_id] = new_item
    return new_item, 201
        
@app.get('/item')
def get_all_items():
    return {"items": list(items.values())}


@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except:
        abort(404, message="Item not found")


@app.put('/item/<string:item_id>')
def update_item(item_id):
    item_data = request.get_json()
    if "name" not in item_data and "price" not in item_data:
        abort(
            400,
            message="Bad request. Ensure 'name' or 'price' is included in the JSON payload."
        )
    try:
        item = items[item_id]
        item |= item_data
        # item.update(item_data)
        return item
    except:
        abort(404, message="Item not found")


@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except:
        abort(404, message="Item not found")
