# library_api/schemas.py

from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from .models import Book as BookModel

class BookSchema(SQLAlchemySchema):
    class Meta:
        model = BookModel
        load_instance = True

    id = auto_field(dump_only=True)
    title = auto_field(required=True)
    author = auto_field(required=True)
    published_year = auto_field(required=True)
