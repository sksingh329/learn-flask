import uuid
from flask import request 
from flask.views import MethodView
from flask_smorest import Blueprint, abort 
from db import stores, items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description= "Operations on items")

@blp.route("/items/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, messag="Item not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message = "Item not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, messag="Item not found")

    


@blp.route("/items")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many= True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
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