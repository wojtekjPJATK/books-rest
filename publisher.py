from flask_restful import Resource
from googleapiclient.discovery import build
from flask import request
import base64


class PubSubPublisher(Resource):

    def post(self):
        message = request.get_json()
        data = message.get('msg')

        service = build('pubsub', 'v1')
        topic_path = 'projects/solwit-pjatk-arc-2018-gr4/topics/dummy'
        service.projects().topics().publish(
        topic=topic_path, body={
          "messages": [{
              "data": base64.b64encode(data)
          }]
        }).execute()
        return message, 201
