from marshmallow import Schema, fields


class ItemSchema(Schema):
    # Only to retrun the id, not to accept it
    id = fields.Str(dump_only=True)
    # Required fields
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)