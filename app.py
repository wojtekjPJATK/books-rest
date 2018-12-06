from flask import Flask
from google.appengine.api import taskqueue
from datetime import time

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
    
@app.route("/mail")
def send():
	task = taskqueue.add(
            url='/send',
            target='mailer', 
            queue_name='mail', 
            countdown=360)

        return 'Task {} enqueued, ETA {}.'.format(task.name, task.eta)