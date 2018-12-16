from __future__ import absolute_import

import datetime
import time

from flask import current_app
from google.cloud import storage
import six
from werkzeug import secure_filename
from werkzeug.exceptions import BadRequest
from google.cloud import pubsub_v1



def _get_storage_client():
    return storage.Client(
        project='solwit-pjatk-arc-2018-gr4')


def _check_extension(filename, allowed_extensions):
    if ('.' not in filename or
            filename.split('.').pop().lower() not in allowed_extensions):
        raise BadRequest(
            "{0} has an invalid name or extension".format(filename))


def _safe_filename(filename):
    filename = secure_filename(filename)
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit('.', 1)
    return "{0}-{1}.{2}".format(basename, date, extension)


def upload_file(file_stream, filename, content_type):

    _check_extension(filename, ['png', 'jpg', 'jpeg', 'gif'])
    filename = _safe_filename(filename)
    filesize = os.path.getsize(file_stream)

    if filesize <= 10 000 000: 

        client = _get_storage_client()
        bucket = client.bucket('solwit-pjatk-bookshelf')
        blob = bucket.blob(filename)

        blob.upload_from_string(
          file_stream,
         content_type=content_type)

        url = blob.public_url

        if isinstance(url, six.binary_type):
         url = url.decode('utf-8')

    else:
    pubsub_complete()

    return url

#initialise pubsub and send message
def pubsub_complete():
    
    
    project_id = "solwit-pjatk-arc-2018-gr4"
    topic_name = "projects/solwit-pjatk-arc-2018-gr4/topics/bookcovers"
    subscription_name = "bookcover"

    # Instantiates a publisher and subscriber client
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_name}`
    topic_path = subscriber.topic_path(project_id, topic_name)

    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_name}`
    subscription_path = subscriber.subscription_path(
        project_id, subscription_name)

    # Create the topic.
    topic = publisher.create_topic(topic_path)
    print('\nTopic created: {}'.format(topic.name))

    # Create a subscription.
    subscription = subscriber.create_subscription(
        subscription_path, topic_path)
    print('\nSubscription created: {}\n'.format(subscription.name))

    # Publish message.
    data = u'File size is above 10MB'
    # Data must be a bytestring
    data = data.encode('utf-8')
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data=data)

    def callback(message):
        message.ack()
        messages.add(message)


    # Receive messages. The subscriber is nonblocking.
    subscriber.subscribe(subscription_path, callback=callback)

    print('\nListening for messages on {}...\n'.format(subscription_path))