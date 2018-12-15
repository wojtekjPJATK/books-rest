from st import storage
import uuid 
from flask import current_app
from google.cloud import datastore


builtin_list = list


def init_app(app):
    pass

def get_client():
    return datastore.Client('solwit-pjatk-arc-2018-gr4')

def from_datastore(entity):
    if not entity:
        return None
    if isinstance(entity, builtin_list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    return entity

#---------------------------------> BOOKS

def BookList():
    ds = get_client()
    query = ds.query(kind='Book', order=['title'])
    results = list(query.fetch())
    entities = []
    for result in results:
        entities.append(from_datastore(result))
        
    return entities

def BookRead(id):
    ds = get_client()
    key = ds.key('Book', int(id))
    results = ds.get(key)
    if results is None:
        return None
    return from_datastore(results)

def BookUpdate(data, id=None):
    ds = get_client()
    if id:
        key = ds.key('Book', int(id))
    else:
        key = ds.key('Book')

    entity = datastore.Entity(
        key=key,
        exclude_from_indexes=['description'])

    if 'id' in data:
        del data['id']

    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)

createBook = BookUpdate

def BookDelete(id):
    ds = get_client()
    key = ds.key('Book', int(id))
    ds.delete(key)

def upload_image_file(file):
    if not file:
       return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url

def getBookByTitle(title):
    ds = get_client()
    query = ds.query(kind = 'Book')
    books = query.fetch()
    results = []
    for book in books:
        if title.lower() in book['title'].lower():
            results.append(from_datastore(book))
    
    return results

def getBookByAuthor(author):
    ds = get_client()
    query = ds.query(kind = 'Book')
    books = query.fetch()
    results = []
    for book in books:
        if author.lower() in book['author'].lower():
            results.append(from_datastore(book))
    
    return results

# search barbaric style 
def findBookByAnything(string):
    ds = get_client()
    query = ds.query(kind = 'Book')
    books = query.fetch()
    results = []
    string = string.lower()
    for book in books:
        if string in book['title'].lower():
            results.append(from_datastore(book))
        elif string in book['description'].lower():
            results.append(from_datastore(book))
        else:
            for author in book['author']:
                if string in author.lower():
                    results.append(from_datastore(book))
                    break
    return results              
        

def checkIfBookExists(title, author):
    ds = get_client()
    query = ds.query(kind = 'Book')
    query.add_filter('Author', '=', author)
    query.add_filter('Title', '=', title)
    results = list(query.fetch(1))
    if results is None:
        return False
    elif not results:
        return False
    else:
        return True

#---------------------------------> AUTHORS

def AuthorRead(id):
    ds = get_client()
    key = ds.key('Author', int(id))
    results = ds.get(key)
    if results is None:
        return None
    return from_datastore(results)

def AuthorUpdate(data, id=None):
    ds = get_client()
    if id:
        key = ds.key('Author', int(id))
    else:
        key = ds.key('Author')

    entity = datastore.Entity(
        key=key
       )
    if 'id' in data:
        del data['id']
    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)

createAuthor = AuthorUpdate

def AuthorList():
    ds = get_client()
    query = ds.query(kind='Author', order=['lastName'])
    results = query.fetch()
    alist = []
    for result in results:
        alist.append(from_datastore(result))
    return alist

def AuthorDelete(id):
    ds = get_client()
    key = ds.key('Author', int(id))
    ds.delete(key)

def isAuthorInDB(name, surname):
    ds = get_client()
    query = ds.query(kind='Author')
    query.add_filter('firstName', '=', name)
    query.add_filter('lastName', '=', surname)
    result = list(query.fetch())
    if result:
        return True
    else:
        return False

def getAuthor(name, surname):
    ds = get_client()
    query = ds.query(kind = 'Author')
    query.add_filter('firstName', '=', name)
    query.add_filter('lastName', '=', surname)
    result = list(query.fetch())
    return from_datastore(result)

#---------------------------------> USERS
    
def getUser(username):
    ds = get_client()
    query = ds.query(kind = 'User')
    query.add_filter('username', '=', username)
    result = list(query.fetch())
    
    if result is None:
        return None
    elif not result:
        return None
    r = result.pop()
    return from_datastore(r) 

def UserRead(id):
    ds = get_client()
    key = ds.key('User', int(id))
    results = ds.get(key)
    return from_datastore(results)

def UserUpdate(data, id=None):
    ds = get_client()
    if id:
        key = ds.key('User', int(id))
    else:
        key = ds.key('User')
    entity = datastore.Entity(
        key=key,
        )
    if 'id' in data:
        del data['id']
    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)

create = UserUpdate

def UserDelete(id):
    ds = get_client()
    key = ds.key('User', int(id))
    ds.delete(key)

def isUserInDB(username):
    ds = get_client()
    query = ds.query(kind='User')
    query.add_filter('username', '=', username)
    result = list(query.fetch())
    if result:
        return True
    else:
        return False

def isCorrectUser(username, password):
    ds = get_client()
    query = ds.query(kind = 'User')
    query.add_filter('username', '=', username)
    query.add_filter('password', '=', password)
    result = list(query.fetch())
    if result:
        return True
    else:
        return False

#---------------------------------> SESSION

def createSession(username):
    ds = get_client()

    key = ds.key('Session')
    entity = datastore.Entity(key=key)
    entity.update({
        'sessionID': str(uuid.uuid1()),
        'user': username,
        'status': 'active'
    })
    ds.put(entity)
    return entity

def destroySession(uuid):
    ds = get_client()
    query = ds.query(kind = 'Session')
    query.add_filter('sessionID', '=', uuid)
    result = from_datastore(query.fetch(1))
    key = ds.key('Session', int(result['id']))
    ds.delete(key)

def destroyAllUserSessions(username):
    ds = get_client()
    query = ds.query(kind = 'Session')
    query.add_filter('user', '=', username)
    results = list(query.fetch())

    for result in results:
        r = from_datastore(result)
        key = ds.key('Session', int(r['id']))      
        ds.delete(key)

def checkIfSessionActive(uuid):
    ds = get_client()
    query = ds.query(kind = 'Session')
    query.add_filter('sessionID', '=', uuid)
    query.add_filter('status', '=', 'active')
    result = list(query.fetch())
    if result is None:
        return False
    elif not result:
        return False
    else:
        return True

def getUsernameFromSession(uuid):
    ds = get_client() 
    query = ds.query(kind = 'Session')
    query.add_filter('sessionID', '=', uuid)
    result = list(query.fetch())
    if result is None:
        return None
    elif not result:
        return None
    else:
        r = result.pop()
        return r['user']
