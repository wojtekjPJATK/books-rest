from flask_restful import Resource
import db as db
from googleapiclient.discovery import build
from flask import request
import base64
import json


class PubSubSubscriber(Resource):

    def post(self):
        message = json.loads(request.data.decode('utf-8'))
        content = base64.b64decode(message['message']['data'])
        message = json.dumps(message)
        key_id = db.postMessage(message, content)
        return 'OK', 200
