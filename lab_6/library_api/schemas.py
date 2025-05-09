# library_api/schemas.py

import datetime
from marshmallow import Schema, fields, validate

current_year = datetime.datetime.now().year

class BookSchema(Schema):
    id = fields.String(
        dump_only=True,
        metadata={"description": "UUID книги"}
    )
    title = fields.String(
        required=True,
        validate=validate.Length(min=1),
        metadata={"description": "Назва книги"}
    )
    author = fields.String(
        required=True,
        validate=validate.Length(min=1),
        metadata={"description": "Автор книги"}
    )
    published_year = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=current_year),
        metadata={"description": "Рік публікації"}
    )
