import db
from flask_restful import Resource

class Login(Resource):
    def post(self):
        user = db.getUser()
        return {'user': user}
