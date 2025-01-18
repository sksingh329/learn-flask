import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema

# A blueprint is a way to organize related views

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")
    
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted"}
        except KeyError:
            abort(404, message="Store not found")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
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