# library_api/schemas.py

import datetime
from marshmallow import Schema, fields, validate

class BookSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(
        required=True,
        validate=validate.Length(min=1, error="Title must not be empty")
    )
    author = fields.String(
        required=True,
        validate=validate.Length(min=1, error="Author must not be empty")
    )
    published_year = fields.Integer(
        required=True,
        validate=validate.Range(
            min=0,
            max=datetime.datetime.now().year,
            error="Published year must be between 0 and current year"
        )
    )
