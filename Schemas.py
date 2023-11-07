from marshmallow import Schema, fields


class ItemSchema(Schema):
    name = fields.Str(required=True)
    runs = fields.Int(required=True)
    balls = fields.Int(required=True)
    out = fields.Str(required=True)


class ItemGetSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
    runs = fields.Int(dump_only=True)
    balls = fields.Int(dump_only=True)
    out = fields.Str(dump_only=True)


class SuccessMessageSchema(Schema):
    message=fields.Str(dump_only=True)


class ItemQueryParameters(Schema):
    id = fields.Str(required=True)

class ItemOptionalQuerySchema(Schema):
    id = fields.Str(required=False)

class UserGetAndDeleteSchema(Schema):
    id=fields.Int(required=True)


class UserSchema(Schema):
    id=fields.Int(dump_only=True)
    username=fields.Str(required=True)
    password=fields.Str(required=True,load_only=True)



