from marshmallow import Schema, fields, validate
from .models import FormatType


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    synopsis = fields.Str()
    isbn = fields.Str()
    cover_url = fields.Str()
    publisher = fields.Str()
    language = fields.Str(validate=validate.OneOf(['Français', 'Anglais']))
    added_at = fields.DateTime(dump_only=True)
    number_of_pages = fields.Int()
    format = fields.Str(validate=validate.OneOf([format.value for format in FormatType]))
