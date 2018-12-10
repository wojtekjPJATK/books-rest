from st import storage
import uuid 
from flask import current_app
from google.cloud import datastore

client = datastore.Client()

def getUser(self, username):
    ds = get_client()
    query = ds.query(kind = 'User')
    query.add_filter('username', '=', username)
    result = list(query.fetch())

    return result