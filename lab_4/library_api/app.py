# library_api/main.py

import os
import uuid
from datetime import datetime
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

    # Створюємо таблиці при старті
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
        cursor = request.args.get('cursor')
        query = Book.query.order_by(Book.created_at, Book.id)

        if cursor:
            try:
                created_at_str, last_id = cursor.split('|')
                created_at = datetime.fromisoformat(created_at_str)
                # вибираємо ті, що йдуть після курсора
                query = query.filter(
                    (Book.created_at > created_at) |
                    ((Book.created_at == created_at) & (Book.id > last_id))
                )
            except Exception:
                return jsonify({'message': 'Invalid cursor'}), 400

        # вибираємо на один елемент більше, щоб знати, чи є next_cursor
        items = query.limit(limit + 1).all()
        has_more = len(items) == limit + 1
        items_to_return = items[:limit]

        next_cursor = None
        if has_more:
            last = items_to_return[-1]
            next_cursor = f"{last.created_at.isoformat()}|{last.id}"

        return jsonify({
            'items': books_schema.dump(items_to_return),
            'next_cursor': next_cursor
        }), 200

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
