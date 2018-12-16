from google.appengine.api import taskqueue
from flask_restful import Resource


class TaskQueue(Resource):
    def get(self):
        task = taskqueue.add(url='/send', target='mailer', queue_name='mail', countdown=360)        
        return 'Task {} enqueued, ETA {}.'.format(task.name, task.eta)
