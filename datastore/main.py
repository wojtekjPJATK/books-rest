import model_datastore
from flask import Flask, request, jsonify, session, abort


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
        else:
                return jsonify(msg = "Wrong username or password")

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
        else:
                return jsonify(msg = "User alredy exists")

@app.route("/book", methods = [ 'GET', 'POST'])
def books():
        if 'uuid' not in session:
                return abort(401)
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
                        return jsonify(book)
                else:
                        return jsonify(msg = "Book already exists")

@app.route("/book/id", methods = ['GET', 'PATCH', 'DELETE'])
def book():
        if 'uuid' not in session:
                return abort(401)
        id = request.args.get('id')
        if id is None:
                return jsonify(msg = 'Forgot id')
        if request.method == 'GET':
                book = model.BookRead(id)
                if book is not None:
                        return jsonify(book)
                else:
                        return jsonify(msg = "No book with this id")

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
                        book = model.BookUpdate(book, id)
                        return jsonify(book)
                else:
                        return jsonify(msg = "No book with this id")
        else:
                model.BookDelete(id)
                return jsonify(msg = "Deleted")

@app.route("/author", methods = ['GET', 'POST'])
def authors():
        if 'uuid' not in session:
                return abort(401)        
        if request.method == 'GET':
                authors = model.AuthorList()
                return jsonify(authors)
        else:
                content = request.get_json()
                if not model.isAuthorInDB(content['firstName'], content['lastName']):
                        data = {}
                        data['firstName'] = content['firstName']
                        data['lastName'] = content['lastName']
                        author = model.createAuthor(data)
                        return jsonify(author)
                else:
                        return jsonify(msg = "Author already in database")

@app.route("/author/id", methods = [ 'PATCH', 'DELETE'])
def author():
        if 'uuid' not in session:
                return abort(401)        
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
                        author = model.AuthorUpdate(author,id)
                        return jsonify(author)
                else:
                        return jsonify(msg = "No author with this id")
        else:
                model.AuthorDelete(id) 
                return jsonify(msg = "Deleted")

@app.route("/favorites/id", methods = ['POST'])
def favBooks():
        if 'uuid' not in session:
                return abort(401)        
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
        user = model.UserUpdate(user, user['id'])
        return jsonify(user['favBooks'])

@app.route("/session/id", methods = [ 'GET' , 'DELETE' ])
def sessions():
        if request.method == 'GET':
                if 'uuid' not in session:
                        return jsonify(False)
                uuid = session['uuid']
                username = model.getUsernameFromSession(uuid)
                user = model.getUser(username) 
                return jsonify(user)
        else:
                if 'uuid' not in session:
                        return abort(401)
                model.destroySession(session['uuid'])
                session.pop('uuid', None)
                return jsonify(msg = "Deleted")

@app.errorhandler(401)
def session_not_found(e):
    return "<p> Error 401. Session not found </p>"

