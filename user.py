import db as db
from flask_restful import Resource


class User(Resource):
    def get(self):
        a = db.postUser()
        return a
        # return 'Task {} enqueued, ETA {}.'.format(task.name, task.eta) key-6711a55ff758dc0abe97ec95aac9fe5c
