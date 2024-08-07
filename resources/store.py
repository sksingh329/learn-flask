import uuid
from flask import request 
from flask.views import MethodView
from flask_smorest import Blueprint, abort 
from db import stores
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description= "Operations on stores")

@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, messag="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, messag="Store not found")


@blp.route("/stores")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many= True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):        
        for store in stores.values():
            if store["name"] == store_data["name"]:
                abort(
                    409,
                    message= "Conflict. Store with same name already exist."
                )

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store,201