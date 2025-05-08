# library_api/main.py

import uuid
from flask import Flask, jsonify, request
from marshmallow import ValidationError

from .schemas import BookSchema

def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False

    # in-memory storage
    books = []

    # схеми для (де)серіалізації
    book_schema = BookSchema()
    books_schema = BookSchema(many=True)

    @app.route('/books', methods=['GET'])
    def get_books():
        """Отримати список всіх книг."""
        return jsonify(books_schema.dump(books)), 200

    @app.route('/books/<string:book_id>', methods=['GET'])
    def get_book(book_id):
        """Отримати книгу за ID."""
        book = next((b for b in books if b['id'] == book_id), None)
        if not book:
            return jsonify({'message': 'Book not found'}), 404
        return jsonify(book_schema.dump(book)), 200

    @app.route('/books', methods=['POST'])
    def add_book():
        """Додати нову книгу."""
        try:
            data = book_schema.load(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        data['id'] = str(uuid.uuid4())
        books.append(data)
        return jsonify(book_schema.dump(data)), 201

    @app.route('/books/<string:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        """Видалити книгу за ID."""
        book = next((b for b in books if b['id'] == book_id), None)
        if not book:
            return jsonify({'message': 'Book not found'}), 404
        books.remove(book)
        return '', 204

    return app

def main():
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
