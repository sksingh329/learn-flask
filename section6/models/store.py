from db import db 

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    items = db.relationship('ItemModel', lazy='dynamic', back_populates='store', cascade="all, delete")  
    tags = db.relationship('TagModel', lazy='dynamic', back_populates='store', cascade="all, delete") 