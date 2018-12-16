from flask_restful import Resource


class Info(Resource):
    def get(self):
        return {'message': 'mainpage hello world'}
