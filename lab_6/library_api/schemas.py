# library_api/schemas.py

import datetime
from marshmallow import Schema, fields, validate

class BookSchema(Schema):
    id = fields.String(dump_only=True, description="UUID книги")
    title = fields.String(
        required=True,
        validate=validate.Length(min=1),
        description="Назва книги"
    )
    author = fields.String(
        required=True,
        validate=validate.Length(min=1),
        description="Автор книги"
    )
    published_year = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=datetime.datetime.now().year),
        description="Рік публікації"
    )
