from marshmallow import Schema,fields

class ItemSchema(Schema):
    id=fields.Str(dump_only=True)
    name=fields.Str(required=True)
    price=fields.Float(required=True)
    store_id=fields.Str(required=True)

class ItemUpdateSchema(Schema):
    id=fields.Str(required=True)
    price=fields.Float(required=True)

class StoreSchema(Schema):
    id=fields.Str(dump_only=True)
    name=fields.Str(required=True)
