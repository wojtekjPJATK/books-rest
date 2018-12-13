from google.appengine.api import taskqueue
from flask_restful import Resource


class TaskQueue(Resource):
    def post(self):
        task = taskqueue.add(url='/send', target='mailer', queue_name='mail', countdown=360)
        return {'message': 'hello world'}        
        # return 'Task {} enqueued, ETA {}.'.format(task.name, task.eta) key-6711a55ff758dc0abe97ec95aac9fe5c
