from marshmallow import fields, Schema

class AuthorSchema(Schema):
    id = fields.Int()
    name = fields.Str()
