

from flask_restplus import Resource, Namespace, fields

api = Namespace('Books', description='Book related operations')

book = api.model('Book', {
    'title': fields.String(required=True, description='The book title'),
    # ...
    'favorited': fields.Boolean(description='Added to user\'s favorites list', default=False)
})

book_id = api.model('Book ID', {
    'id': fields.String(required=True)
})


@api.route('/')
class AllBooks(Resource):

    # zwraca liste ksiazek wraz z ulubionymi, dostep chroniony, wiec bedziemy znac usera, ktory wysyla zapytanie
    @api.marshal_list_with(book)
    def get(self):
        return [{'title': 'Testowy'}, {'title': 'Wincyj testuf', 'favorited': True}]

    @api.marshal_with(book)
    @api.expect(book)
    def post(self):
        return api.payload


@api.route('/<id>')
class BookByID(Resource):

    @api.marshal_with(book)
    @api.expect(book_id)
    def get(self, id):
        return {'message': 'ok'}

    @api.marshal_with(book)
    @api.expect(book_id)
    @api.marshal_with(book)
    def delete(self):
        return

    @api.marshal_with(book)
    def put(self, id):
        return {'message': 'ok'}
