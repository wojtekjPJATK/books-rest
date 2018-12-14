import model_datastore
from flask import Flask, request, jsonify, session


app = Flask(__name__)

model = model_datastore


@app.route("/signin", methods = 'POST')
def signin():
    content = request.get_json()
    if model.isCorrectUser(content['login'], content['password']):
        model.destroyAllUserSessions(content['login'])
        session = model.createSession(content['login'])
        session['uuid'] = session['sessionID']
        return jsonify(session['uuid'])

@app.route("/join", methods = [ 'POST' ])
def join():
    content = request.get_json()
    if not model.isUserInDB(content['login']):
        data = {}
        data['username'] = content['login']
        data['password'] = content['password']
        data['security_lvl'] = 'normal'
        data['favBooks'] = None
        model.create(data)
        session = model.createSession(content['username'])
        session['uuid'] = session['sessionID']
        return jsonify(session['uuid'])

@app.route("/book", methods = [ 'GET', 'POST'])
def books():
        uuid = session['uuid']
        username = model.getUsernameFromSession(uuid)
        user = model.getUser(username)            
        if request.method == 'GET':
                books = model.BookList()
                favBooks = list((user['favBooks']))
                return jsonify(books, favBooks)
        else:
                content  = request.get_json()
                if not model.checkIfBookExists(content['author'], content['title']):
                        img = request.files.get('image')            
                        image_url = model.upload_image_file(img)
                        data = {}
                        data['title'] = content['title']
                        data['author'] = content['author']
                        data['description'] = content['description']
                        data['imageUrl'] = image_url
                        data['addedBy'] = user['id']
                        book = model.createBook(data)

@app.route("/book/id", methods = ['GET', 'PATCH', 'DELETE'])
def book():
        id = request.args.get('id')
        if id is None:
                return jsonify(msg = 'Forgot id')
        if request.method == 'GET':
                book = model.BookRead(id)
                if book is not None:
                        return jsonify(book)

        elif request.method == 'PATCH':
                book = model.BookRead(id)
                if book is not None:
                        content = request.get_json()
                        if 'title' in content:
                                book['title'] = content['title']
                        if 'author' in content:        
                                book['author'] = content['author']
                        if 'description' in content:
                                book['description'] = content['description']
                        model.BookUpdate(book, id)

        else:
                model.BookDelete(id)

@app.route("/author", methods = ['GET', 'POST'])
def authors():
        if request.method == 'GET':
                authors = model.AuthorList()
                return jsonify(authors)
        else:
                content = request.get_json()
                if not model.isAuthorInDB(content['firstName'], content['lastName']):
                        data = {}
                        data['firstName'] = content['firstName']
                        data['lastName'] = content['lastName']
                        model.createAuthor(data)

@app.route("/author/id", methods = [ 'PATCH', 'DELETE'])
def author():
        id = request.args.get('id')
        if id is None:
                return jsonify(msg = 'Forgot id')
        if request.method == 'PATCH':
                author = model.AuthorRead(id)
                if author is not None:
                        content = request.get_json()
                        if 'firstName' in content:
                                author['firstName'] = content['firstName']
                        if 'lastName' in content:
                                author['lastName'] = content['lastName']
                        model.AuthorUpdate(author,id)
        else:
                model.AuthorDelete(id)  

@app.route("/favorites/id", methods = ['POST'])
def favBooks():
        id = request.args.get('id')
        if id is None:
                return jsonify(msg = 'Forgot id')
        uuid = session['uuid']
        username = model.getUsernameFromSession(uuid)
        user = model.getUser(username) 
        favBooks = user['favBooks']
        if favBooks is None:
                favBooks = []
                favBooks.append(id)
        elif id in favBooks:
                favBooks.remove(id)
        else:
                favBooks.append(id)
        
        user['favBooks'] = favBooks        
        model.UserUpdate(user, user['id'])
