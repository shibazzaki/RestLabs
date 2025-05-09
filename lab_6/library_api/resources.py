# library_api/resources.py

import uuid
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from .schemas import BookSchema

# in-memory storage
books = []
book_schema = BookSchema()
books_schema = BookSchema(many=True)

class BookListResource(Resource):
    def get(self):
        """
        Отримати всі книги
        ---
        responses:
          200:
            description: Список книг
            schema:
              type: array
              items:
                $ref: '#/definitions/Book'
        """
        return books_schema.dump(books), 200

    def post(self):
        """
        Додати книгу
        ---
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/Book'
        responses:
          201:
            description: Створена книга
            schema:
              $ref: '#/definitions/Book'
          400:
            description: Помилка валідації
        """
        json_data = request.get_json()
        try:
            data = book_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        data['id'] = str(uuid.uuid4())
        books.append(data)
        return book_schema.dump(data), 201

class BookResource(Resource):
    def get(self, book_id):
        """
        Отримати книгу за ID
        ---
        parameters:
          - in: path
            name: book_id
            type: string
            required: true
        responses:
          200:
            description: Дані книги
            schema:
              $ref: '#/definitions/Book'
          404:
            description: Книга не знайдена
        """
        book = next((b for b in books if b['id'] == book_id), None)
        if not book:
            return {'message': 'Book not found'}, 404
        return book_schema.dump(book), 200

    def delete(self, book_id):
        """
        Видалити книгу за ID
        ---
        parameters:
          - in: path
            name: book_id
            type: string
            required: true
        responses:
          204:
            description: Книга успішно видалена
          404:
            description: Книга не знайдена
        """
        global books
        book = next((b for b in books if b['id'] == book_id), None)
        if not book:
            return {'message': 'Book not found'}, 404
        books = [b for b in books if b['id'] != book_id]
        return '', 204
