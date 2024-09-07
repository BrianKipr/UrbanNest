from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()

class ProductSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    price = fields.Float()

class OrderSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    total_amount = fields.Float()
    status = fields.Str()
