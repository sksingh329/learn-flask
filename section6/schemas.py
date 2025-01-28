from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    # Only to retrun the id, not to accept it
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()


class StoreSchema(PlainStoreSchema):
    items = fields.Nested(PlainItemSchema, many=True, dump_only=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Str(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema, dump_only=True)