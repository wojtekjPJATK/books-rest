from google.appengine.api import taskqueue


class TaskQueue(Resource):
    def post(self):
        task = taskqueue.add(url='/send', target='mailer', queue_name='mail', countdown=360)
        return {'message': 'hello world'}        
        # return 'Task {} enqueued, ETA {}.'.format(task.name, task.eta)
