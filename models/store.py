from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80), unique= True, nullable= False)
    items = db.relationship("ItemModel", bacl_populates="store", lazy="dynamic")