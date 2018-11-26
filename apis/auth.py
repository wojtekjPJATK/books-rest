from flask_restplus import Resource, Namespace

api = Namespace('Authorization', description='Auth related operations')


@api.route('/join')
class Join(Resource):
    def post(self):
        return {'message': 'ok'}


@api.route('/signin')
class SignIn(Resource):
    def post(self):
        return {'message': 'ok'}

# Tutaj będzie więcej endpointów - zależy jak będziemy robić autentykację - Flask-JWT?
