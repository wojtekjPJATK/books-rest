from __future__ import absolute_import

import datetime
import time

from flask import current_app
from google.cloud import storage
import six
from werkzeug import secure_filename
from werkzeug.exceptions import BadRequest
from google.cloud import pubsub_v1


project_id = "solwit-pjatk-arc-2018-gr4"
topic_name = "projects/solwit-pjatk-arc-2018-gr4/topics/covers"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)

def callback(message_future):
    # When timeout is unspecified, the exception method waits indefinitely.
    if message_future.exception(timeout=30):
        print('Publishing message on {} threw an Exception {}.'.format(
            topic_name, message_future.exception()))
    else:
        print(message_future.result())



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

    client = _get_storage_client()
    bucket = client.bucket('solwit-pjatk-bookshelf')
    blob = bucket.blob(filename)

    blob.upload_from_string(
        file_stream,
        content_type=content_type)

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    #pubsub message
    data = u'Storing a cover ended successfully'
    data = data.encode('utf-8')
    message_future = publisher.publish(topic_path, data=data)
    message_future.add_done_callback(callback)
    # We must keep the main thread from exiting to allow it to process
    # messages in the background.
    while True:
        time.sleep(60)


    return url