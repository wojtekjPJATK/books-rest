import db

class User(Resource):
    def get(self):
        getUser()
        return {'message': 'hello world'}        
        # return 'Task {} enqueued, ETA {}.'.format(task.name, task.eta) key-6711a55ff758dc0abe97ec95aac9fe5c
