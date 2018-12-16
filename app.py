from flask import Flask
from datetime import time
from flask_restful import Resource, Api
from flask_cors import CORS
from info import Info
from task import TaskQueue
from login import Login
from user import User
from publisher import PubSubPublisher
from subscriber import PubSubSubscriber
import cloudstorage
from google.appengine.api import app_identity


app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api.add_resource(Info, '/')
api.add_resource(TaskQueue, '/mail')
api.add_resource(Login, '/login')
api.add_resource(User, '/user')
api.add_resource(PubSubPublisher, '/pubsub')
api.add_resource(PubSubSubscriber, '/_ah/push-handlers/dummypush')
