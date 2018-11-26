from flask_restplus import Api

from .book import api as books
from .auth import api as auth

api = Api(version='0.1', title='Book API', description='An API for books')

api.add_namespace(books)
api.add_namespace(auth)
