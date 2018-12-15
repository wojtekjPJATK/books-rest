import model_datastore
from flask import Flask, request, jsonify, session, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = model_datastore

@app.route("/signin", methods = ['POST'])
def signin():
        content = request.get_json()
        if content is None:
                return jsonify(msg = "No JSON for me huh?")
        if model.isCorrectUser(content['login'].strip(), content['password'].strip()):
                model.destroyAllUserSessions(content['login'].strip())
                my_session = model.createSession(content['login'].strip())
                return jsonify(id = my_session['sessionID'])
        else:
                return jsonify(msg = "Wrong username or password")

@app.route("/join", methods = [ 'POST' ])
def join():
        content = request.get_json()
        if content is None:
                return jsonify(msg = "No JSON for me huh?")
        if not model.isUserInDB(content['login'].strip()):
                data = {}
                data['username'] = content['login'].strip()
                data['password'] = content['password'].strip()
                data['security_lvl'] = 'normal'
                data['favBooks'] = None
                model.create(data)
                my_session = model.createSession(content['login'])
                return jsonify(id = my_session['sessionID'])
        else:
                return jsonify(msg = "User alredy exists")

@app.route("/book", methods = [ 'GET', 'POST'])
def books():
        uuid = None
        if 'Authorization' not in request.headers:
                return abort(401)
        uuid = request.headers.get('Authorization')
        if uuid is None:
                return abort(401)
        if not model.checkIfSessionActive(uuid):
                return abort(401)
        username = model.getUsernameFromSession(uuid)
        user = model.getUser(username) 
        if user is None:
                return jsonify(msg = "Something went horribly wrong")                   
        if request.method == 'GET':
                books = model.BookList()
                if user['favBooks'] is not None:
                        favBooks = list((user['favBooks']))
                else: 
                        favBooks = []
                return jsonify(books = books, favBooks = favBooks)
        else:
                content  = request.get_json()
                if not model.checkIfBookExists(content['author'], content['title'].strip()):
                        img = request.files.get('image')            
                        image_url = model.upload_image_file(img)
                        data = {}
                        data['title'] = content['title'].strip()
                        data['author'] = list(content['author'])
                        data['description'] = content['description'].strip()
                        data['imageUrl'] = image_url
                        data['addedBy'] = user['id']
                        book = model.createBook(data)
                        return jsonify(book = book)
                else:
                        return jsonify(msg = "Book already exists")

@app.route("/book/<id>", methods = ['GET', 'PATCH', 'DELETE'])
def book(id):
        uuid = None
        if 'Authorization' not in request.headers:
                return abort(401)
        uuid = request.headers.get('Authorization')
        if uuid is None:
                return abort(401)
        if not model.checkIfSessionActive(uuid):
                return abort(401)
        if id is None:
                return jsonify(msg = 'Forgot id')
        if request.method == 'GET':
                book = model.BookRead(id)
                if book is not None:
                        return jsonify(book = book)
                else:
                        return jsonify(msg = "No book with this id")

        elif request.method == 'PATCH':
                book = model.BookRead(id)
                if book is not None:
                        content = request.get_json()
                        if 'title' in content:
                                book['title'] = content['title'].strip()
                        if 'author' in content:        
                                book['author'] = list(content['author'])
                        if 'description' in content:
                                book['description'] = content['description'].strip()
                        book = model.BookUpdate(book, id)
                        return jsonify(book = book)
                else:
                        return jsonify(msg = "No book with this id")
        else:
                model.BookDelete(id)
                return jsonify(msg = "Deleted")

@app.route("/author", methods = ['GET', 'POST'])
def authors():
        uuid = None
        if 'Authorization' not in request.headers:
                return abort(401)
        uuid = request.headers.get('Authorization')
        if uuid is None:
                return abort(401) 
        if not model.checkIfSessionActive(uuid):
                return abort(401)
        if request.method == 'GET':
                authors = model.AuthorList()
                return jsonify(authors = authors)
        else:
                content = request.get_json()
                if not model.isAuthorInDB(content['firstName'].strip(), content['lastName'].strip()):
                        data = {}
                        data['firstName'] = content['firstName'].strip()
                        data['lastName'] = content['lastName'].strip()
                        author = model.createAuthor(data)
                        return jsonify(author = author)
                else:
                        return jsonify(msg = "Author already in database")

@app.route("/author/<id>", methods = [ 'PATCH', 'DELETE'])
def author(id):
        uuid = None
        if 'Authorization' not in request.headers:
                return abort(401)
        uuid = request.headers.get('Authorization')
        if uuid is None:
                return abort(401) 
        if not model.checkIfSessionActive(uuid):
                return abort(401)     
        if id is None:
                return jsonify(msg = 'Forgot id')
        if request.method == 'PATCH':
                author = model.AuthorRead(id)
                if author is not None:
                        content = request.get_json()
                        if 'firstName' in content:
                                author['firstName'] = content['firstName'].strip()
                        if 'lastName' in content:
                                author['lastName'] = content['lastName'].strip()
                        author = model.AuthorUpdate(author,id)
                        return jsonify(author = author)
                else:
                        return jsonify(msg = "No author with this id")
        else:
                model.AuthorDelete(id) 
                return jsonify(msg = "Deleted")

@app.route("/favorites/<id>", methods = ['POST'])
def favBooks(id):
        uuid = None
        if 'Authorization' not in request.headers:
                return abort(401)
        uuid = request.headers.get('Authorization')
        if uuid is None:
                return abort(401)
        if not model.checkIfSessionActive(uuid):
                return abort(401)  
        if id is None:
                return jsonify(msg = 'Forgot id')
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
        return jsonify(favBooks = user['favBooks'])

@app.route("/session/<id>", methods = [ 'GET' , 'DELETE' ])
def sessions(id):
        uuid = None
        if 'Authorization' not in request.headers:
                return abort(401)
        uuid = request.headers.get('Authorization')
        if uuid is None:
                return abort(401)
        if not model.checkIfSessionActive(uuid):
                return abort(401)
        if request.method == 'GET':
                if not model.checkIfSessionActive(uuid):
                        return jsonify(session = False)
                username = model.getUsernameFromSession(uuid)
                user = model.getUser(username) 
                return jsonify(user = user)
        else:
                if not model.checkIfSessionActive(uuid):
                        return abort(401)
                model.destroySession(uuid)
                return jsonify(msg = "Deleted")



  

@app.errorhandler(401)
def session_not_found(e):
    return "<p> Error 401. Session not found </p>"

