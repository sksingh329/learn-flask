from flask import Flask,request # type: ignore

app = Flask(__name__)

stores = [
    {
        "name": "My Wonderful Store",
        "items": [
            {
                "name": "My Item",
                "price": 15.99
            }
        ]
    }
]

@app.get('/store')
def get_stores():
    return {"stores": stores}

@app.post('/store')
def create_stores():
    # Here request_data is a dictionary
    request_data = request.get_json()

    new_store = {"name": request_data["name"], "items": []}

    stores.append(new_store)

    # Default status code is 200
    return new_store, 201

@app.post('/store/<string:name>/item')
def create_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            request_data = request.get_json()
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404

@app.get('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store not found"}, 404

@app.get('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404
