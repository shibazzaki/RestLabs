# library_api/main.py

import os
import uuid
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/library'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        from .models import Book
        db.create_all()

    from .models import Book
    from .schemas import BookSchema

    book_schema = BookSchema()
    books_schema = BookSchema(many=True)

    @app.route('/books', methods=['GET'])
    def get_books():
        limit = request.args.get('limit', default=10, type=int)
        offset = request.args.get('offset', default=0, type=int)
        query = Book.query.offset(offset).limit(limit).all()
        return jsonify(books_schema.dump(query)), 200

    @app.route('/books/<string:book_id>', methods=['GET'])
    def get_book(book_id):
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book not found'}), 404
        return jsonify(book_schema.dump(book)), 200

    @app.route('/books', methods=['POST'])
    def add_book():
        try:
            data: Book = book_schema.load(request.get_json(), session=db.session)
        except ValidationError as err:
            return jsonify(err.messages), 400

        data.id = str(uuid.uuid4())
        db.session.add(data)
        db.session.commit()
        return jsonify(book_schema.dump(data)), 201

    @app.route('/books/<string:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book not found'}), 404
        db.session.delete(book)
        db.session.commit()
        return '', 204

    return app

def main():
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
