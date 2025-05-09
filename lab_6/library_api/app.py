# library_api/app.py

from flask import Flask
from flask_restful import Api
from flasgger import Swagger

from .resources import BookListResource, BookResource

def create_app():
    app = Flask(__name__)

    # Базова конфігурація Swagger
    template = {
        "swagger": "2.0",
        "info": {
            "title": "Library API",
            "description": "CRUD API для книг з Flask-RESTful і Swagger UI",
            "version": "1.0.0"
        },
        "definitions": {
            "Book": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "published_year": {"type": "integer"}
                },
                "required": ["title", "author", "published_year"]
            }
        }
    }
    Swagger(app, template=template)

    api = Api(app)
    api.add_resource(BookListResource, '/books')
    api.add_resource(BookResource, '/books/<string:book_id>')

    return app

def main():
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
