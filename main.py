from flask import Flask
from google.appengine.api import taskqueue

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
    
@app.route("/mail")
def send():
	task = taskqueue.add(
            url='/send',
            target='mailer')

        self.response.write(
            'Task {} enqueued, ETA {}.'.format(task.name, task.eta))