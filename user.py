import db as db
from flask_restful import Resource


class User(Resource):
    def get(self):
        a = db.postUser()
        return a
