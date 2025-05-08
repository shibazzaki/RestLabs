# library_api/models.py

from .app import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    published_year = db.Column(db.Integer, nullable=False)
