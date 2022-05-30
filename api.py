from crypt import methods
from webbrowser import get
from flask import Flask, jsonify, render_template, redirect, url_for, request, flash, abort, session
from numpy import tile

# from flask_googlemaps import GoogleMaps, Map

from fromApi import FromApi as fp
from models.users import *
from forms import *
import requests

# from models.users import app, db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://marieme:marieme@localhost/flasko'
app.config['SECRET_KEY'] = "kfvbsdkfgsfgnkg(_çty( fdbdsd))"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config['GOOGLEMAPS_KEY'] = 'AIzaSyCi1YySTBjwmSZ3BmmgIRYs-rHcgC0-zCY'

db.init_app(app)

"""
############################################################################################
##                                     FONCTIONS                                          ##
############################################################################################
"""

def getId(User):
    Users = User.query
    liste_ = []
    for user in Users:
        liste_.append(user.id)
    maximum_liste = max(liste_)
    return maximum_liste+1

"""
############################################################################################
##                                          API                                           ##
############################################################################################
"""
# GET ALL USER
@app.route('/api/users')
def apiUsersGet():
    Users = User.query.filter_by(archive=False)
    dictApi = []
    for user in Users:
        id = user.id
        Addresses = User.query.filter_by(id=id).first().address
        Companies = User.query.filter_by(id=id).first().company
        dictApi.append({
            "id": user.idApi,
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "address": {
            "street": Addresses.street,
            "suite": Addresses.suite,
            "city": Addresses.city,
            "zipcode": Addresses.zipcode,
            "geo": {
                "lat": Addresses.lat,
                "lng": Addresses.lng
            }
            },
            "phone": user.phone,
            "website": user.website,
            "company": {
            "name": Companies.name,
            "catchPhrase": Companies.catchPhrase,
            "bs": Companies.bs
            }
        })
    try:
        return jsonify(dictApi)
    except:
        return jsonify({"Error": "Post doesn't work well !"})
# POST A NEW USER
@app.route('/api/users', methods=['POST'])
def apiUsersPost():
    dictApiCompany = dictApiAddress = dictApiGeo = {}
    dictApi = request.get_json()
    dictApiAddress = dictApi["address"]
    dictApiGeo = dictApiAddress["geo"]
    address_add = Address(
                    street   = dictApiAddress.get("street"),
                    suite    = dictApiAddress.get("suite"),
                    city     = dictApiAddress.get("city"),
                    zipcode  = dictApiAddress.get("zipcode"),
                    lat      = dictApiGeo.get("lat"),
                    lng      = dictApiGeo.get("lng")
                )
    db.session.add(address_add)
    db.session.commit()
    dictApiCompany = dictApi["company"]
    company_add = Company(
                    name         = dictApiCompany.get("name"),
                    catchPhrase  = dictApiCompany.get("catchPhrase"),
                    bs           = dictApiCompany.get("bs")
                ) 
    db.session.add(company_add)
    db.session.commit()
    user_add = User(
                    id        = getId(User),
                    name      =dictApi.get("name"),
                    username  =dictApi.get("username"),
                    email     =dictApi.get("email"),
                    addressId =(getId(Address)-1),
                    companyId =(getId(Company)-1),
                    phone     =dictApi.get("phone"),
                    website   =dictApi.get("website")
                )
    db.session.add(user_add)
    db.session.commit()
    try:
        return  jsonify({'POST OK':dictApi})
    except:
        return jsonify({"Error": "Post doesn't work well !"})

# GET ONE USER BY HIS ID
@app.route('/api/users/<int:user_id>')
def apiUserIdGet(user_id):
    dictApi ={}
    user = User.query.filter_by(id=user_id,archive=False).first()
    Addresses = (User.query.filter_by(id=user_id,archive=False).first()).address
    Companies = (User.query.filter_by(id=user_id,archive=False).first()).company
    dictApi={
        "id": user.idApi,
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "address": {
        "street": Addresses.street,
        "suite": Addresses.suite,
        "city": Addresses.city,
        "zipcode": Addresses.zipcode,
        "geo": {
            "lat": Addresses.lat,
            "lng": Addresses.lng
        }
        },
        "phone": user.phone,
        "website": user.website,
        "company": {
        "name": Companies.name,
        "catchPhrase": Companies.catchPhrase,
        "bs": Companies.bs
        }
    }
    try:
        return jsonify(dictApi)
    except:
        return jsonify({"Error": "Request doesn't work well !"})
#DELETE A POST BY ID
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def apiUserIdDelete(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.archive = True
    db.session.commit()
    try:
        return  jsonify({"DELETE OK"})
    except:
        return jsonify({"Error": "Request doesn't work well !"})
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def apiUserIdPut(user_id):
    addressJson = geoJson = companyJson = {}
    user = User.query.filter_by(id=user_id).first()
    company = (User.query.filter_by(id=user_id).first()).company
    address = (User.query.filter_by(id=user_id).first()).address
    req = request.get_json()
    addressJson = req["address"]
    geoJson     = addressJson["geo"]
    companyJson = req["company"]
    company.bs          = companyJson.get("bs")
    company.catchPhrase = companyJson.get("catchPhrase")
    company.name        = companyJson.get("name")

    address.city        = addressJson.get("city")
    address.geo         = addressJson.get("geo")
    address.lat         = geoJson.get("lat")
    address.lng         = geoJson.get("lng")
    address.street      = addressJson.get("street")
    address.suite       = addressJson.get("suite")
    address.zipcode     = addressJson.get("zipcode")
    
    user.name           = req.get("name")
    user.username       = req.get("username")
    user.phone          = req.get("phone")
    user.website        = req.get("website")
    user.email          = req.get("email")
    db.session.commit()
    return  jsonify({"PUT OK":req})

@app.route('/api/user/<int:user_id>/albums')
def apiPostAlbumsGet(user_id):
    dictApi = []
    Users = User.query.filter_by(id=user_id).first()
    for album in list(Users.albums):
        dictApi.append({
            "userId" : album.userId,
            "id"     : album.id,
            "title"  : album.title
        })
    try:
        return  jsonify(dictApi)
    except:
        return jsonify({"Error": "Request doesn't work well !"})
@app.route('/api/user/<int:user_id>/albums', methods=['DELETE'])
def apiPostAlbumsDelete(user_id):
    Albums = Album.query.filter_by(userId=user_id,archive=False)
    for album in Albums:
        album.archive=True
    try:
        return  "DELETED"
    except:
        return jsonify({"Error": "Request doesn't work well !"})
@app.route('/api/user/<int:post_id>/todos')
def apiPostTodosGet(post_id):
    dictApi = []
    Posts = Post.query.filter_by(id=post_id,archive=False).first()
    for todos in list(Posts.todos):
        dictApi.append({
            "userId" : todos.userId,
            "id"     : todos.id,
            "title"  : todos.title,
            "completed":todos.completed
        })
    try:
        return  jsonify(dictApi)
    except:
        return jsonify({"Error": "Request doesn't work well !"})
@app.route('/api/user/<int:post_id>/todos', methods=['DELETE'])
def apiPostTodosDelete(post_id):
    todos = Todo.query.filter_by(postId=post_id)
    for todo in todos:
        todo.archive=True
    try:
        return  "DELETED"
    except:
        return jsonify({"Error": "Request doesn't work well !"})


"""######           POST validate         ######"""
#GET ALL POST ON DATABASE
@app.route('/api/posts')
def apiPostsGet():
    Posts    = Post.query.filter_by(archive=False)
    dictApi = []
    for post in Posts:
        dictApi.append({
            "userId" : post.userId,
            "idApi" : post.idApi,
            "title" : post.title,
            "body" : post.body,
        })
    try:
        return  jsonify(dictApi) #render_template('apiPosts.html', dictApi=dictApi)
    except:
        return jsonify({"Error": "Request doesn't work well !"})
#Post a new post on database
@app.route('/api/posts', methods=['POST'])
def apiPostsPost():
    #POST A NEW POST
    dictApi = {
        "id" : getId(Post),
        "userId" : request.json['userId'],
        "title" : request.json['title'],
        "body" : request.json['body']
    }
    post_add = Post(
                    id=dictApi.get("id"),
                    userId=dictApi.get("userId"),
                    title=dictApi.get("title"),
                    body=dictApi.get("body")
                )
    db.session.add(post_add)
    db.session.commit()
    try:
        return  jsonify({'POST OK':dictApi})
    except:
        return jsonify({"Error": "Request doesn't work well !"})


#GET POST BY ID
@app.route('/api/posts/<int:post_id>')
def apiPostIdGet(post_id):
    post    = Post.query.filter_by(id=post_id, archive=False).first()
    dictApi = {
        "userId" : post.userId,
        "idApi" : post.idApi,
        "title" : post.title,
        "body" : post.body,
    }
    try:
        return  jsonify(dictApi)
    except:
        return jsonify({"Error": "Request doesn't work well !"})
#MODIFY A POST BY ID
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def apiPostPut(post_id):
    post = Post.query.filter_by(id=post_id).first()
    req = request.get_json()
    post.title = req.get("title")
    post.userId = req.get("userId")
    post.body = req.get("body")
    db.session.commit()
    try:
        return  jsonify({"PUT OK":req})
    except:
        return jsonify({"Error": "Request doesn't work well !"})
#DELETE A POST BY ID
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def apiPostDelete(post_id): 
    post = Post.query.filter_by(id=post_id).first()
    dictApi = {
        "userId" : post.userId,
        "idApi" : post.idApi,
        "title" : post.title,
        "body" : post.body,
    }
    post.archive = True
    db.session.commit()
    try:
        return  jsonify({"DELETE OK":dictApi}) 
    except:
        return jsonify({"Error": "Request doesn't work well !"})


# GEt all comments in a post
@app.route('/api/posts/<int:post_id>/comments')
def apiPostCommentsGet(post_id):
    dictApi = []
    ePost = Post.query.filter_by(id=post_id,archive=False).first()
    for comment in list(ePost.comments):
        dictApi.append({
            "postId" : comment.postId,
            "name"   : comment.name,
            "email"  : comment.email,
            "body"   : comment.body,
        })
    try:
        return  jsonify(dictApi)
    except:
        return jsonify({"Error": "Request doesn't work well !"})
# Delete All comments in a post
@app.route('/api/posts/<int:post_id>/comments', methods=['DELETE'])
def apiPostCommentsDelete(post_id):  
    Comments = Comment.query.filter_by(postId=post_id,archive=False)
    for comment in Comments:
        comment.archive=True
    try:
        return  "DELETED"
    except:
        return jsonify({"Error": "Request doesn't work well !"})

"""#######       COMMENTS           ######"""
#DONE
@app.route('/api/comments')
def apiCommentsGet():
    #GET ALL COMMENTS ON DATABASE
    Comments    = Comment.query
    dictApi = []
    for comment in Comments:
        dictApi.append({
            "postId" : comment.postId,
            "name" : comment.name,
            "email" : comment.email,
            "body" : comment.body,
        })
    try:
        return  jsonify(dictApi)
    except:
        return jsonify({"Error": "Request doesn't work well !"})
#POST A NEW COMMENT
@app.route('/api/comments', methods=['POST'])
def apiCommentsPost():
    dictApi = {
        "id" : getId(Comment),
        "postId" : request.json['postId'],
        "name" : request.json['name'],
        "email" : request.json['email'],
        "body" : request.json['body']
    }
    comment_add = Comment(
                    id=dictApi.get("id"),
                    postId=dictApi.get("postId"),
                    name=dictApi.get("name"),
                    email=dictApi.get("email"),
                    body=dictApi.get("body")
                )
    db.session.add(comment_add)
    db.session.commit()
    try:
        return jsonify("POST OK",dictApi)
    except:
        return jsonify({"Error": "Request doesn't work well !"})


#GET A COMMENT BY ID
@app.route('/api/comments/<int:comment_id>')
def apiCommentIdGet(comment_id):
    data = dict()
    comment = Comment.query.get_or_404(comment_id)
    data = {
            'id' : comment.id,
            'postId' : comment.postId,
            'name' : comment.name,
            'email' : comment.email,
            'body' : comment.body,
    }
    return data
# MODIFY A COMMENT BY ID
@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
def apiCommentIdPut(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    req = request.get_json()
    comment.postId = req.get("postId")
    comment.name = req.get("name")
    comment.email = req.get("email")
    comment.body = req.get("body")
    db.session.commit()
    return  jsonify({"OK PUT":req})
#DELETE A COMMENT BY ID
@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def apiCommentIdDelete(comment_id):
        comment = Comment.query.filter_by(id=comment_id).first()
        comment.archive = True
        data = {
                'id'     : comment.id,
                'postId' : comment.postId,
                'name'   : comment.name,
                'email'  : comment.email,
                'body'   : comment.body,
        }
        db.session.commit()
        return jsonify({"DELETED":data})


"""######           ALBUMS          ######"""
#GET ALL ALBUMS ON DATABASE
@app.route('/api/albums')
def apiAlbumsGet():
    Albums    = Album.query.filter_by(archive=False)
    dictApi = []
    for album in Albums:
        dictApi.append({
            "userId" : album.userId,
            "id" : album.id,
            "title" : album.title
        })
    return  jsonify(dictApi)
#POST A NEW POST
@app.route('/api/albums', methods=['POST'])
def apiAlbumsPost():
    dictApi = {
        "id" : getId(Album),
        "userId" : request.json['userId'],
        "title" : request.json['title']
    }
    album_add = Album(
                    id=dictApi.get("id"),
                    userId=dictApi.get("userId"),
                    title=dictApi.get("title")
                )
    db.session.add(album_add)
    db.session.commit()
    return  jsonify({'POST OK':dictApi})

#GET ALBUM BY ID
@app.route('/api/albums/<int:album_id>')
def apiAlbumIdGet(album_id):
    album    = Album.query.filter_by(id=album_id).first()
    dictApi = {
        "userId" : album.userId,
        "id" : album.id,
        "title" : album.title
    }
    return  jsonify(dictApi)
#MODIFY A ALBUM BY ID
@app.route('/api/albums/<int:album_id>', methods=['PUT'])
def apiAlbumIdPut(album_id):
    album = Album.query.filter_by(id=album_id).first()
    req = request.get_json()
    album.title = req.get("title")
    album.userId = req.get("userId")
    db.session.commit()
    return  jsonify({"PUT OK":req})
#DELETE A ALBUM BY ID
@app.route('/api/albums/<int:album_id>', methods=['GET','PUT','DELETE'])
def apiAlbumIdDelete(album_id): 
    album = Album.query.filter_by(id=album_id).first()
    dictApi = {
        "userId" : album.userId,
        "id" : album.id,
        "title" : album.title
    }
    album.archive = True
    db.session.commit()
    return  jsonify({"DELETE OK":dictApi})    



@app.route('/api/albums/<int:album_id>/photos')
def apiAlbumsPhotosGet(photo_id):
    dictApi = []
    Photos = Album.query.filter_by(id=photo_id,archive=False).first()
    for photo in list(Photos.comments):
        dictApi.append({
            "postId" : photo.postId,
            "name"   : photo.name,
            "email"  : photo.email,
            "body"   : photo.body,
        })
    return  jsonify(dictApi)
@app.route('/api/albums/<int:album_id>/photos', methods=['DELETE'])
def apiAlbumsPhotosDelete(photo_id):
    Photos = Photo.query.filter_by(albumId=photo_id)
    for photo in Photos:
        photo.archive=True
    return  "DELETED"


"""######           PHOTOS          ######"""

#GET ALL PHOTO ON DATABASE
@app.route('/api/photos', methods=['GET','POST'])
def apiPhotosGet():
    Photos    = Photo.query.filter_by(archive=False)
    dictApi = []
    for photo in Photos:
        dictApi.append({
            "albumId" : photo.albumId,
            "id" : photo.id,
            "title" : photo.title,
            "url" : photo.url,
            "thumbnailUrl" : photo.thumbnailurl
        })
    return  jsonify(dictApi)
#POST A NEW PHOTO
@app.route('/api/photos', methods=['GET','POST'])
def apiPhotosPost():
    dictApi = {
        "id" : getId(Photo),
        "albumId" : request.json['albumId'],
        "id" : request.json['id'],
        "title" : request.json['title'],
        "url" : request.json['url'],
        "thumbnailUrl" : request.json['thumbnailUrl']
    }
    photo_add = Photo(
                    id           = dictApi.get("id"),
                    albumId      = dictApi.get("albumId"),
                    title        = dictApi.get("title"),
                    url          = dictApi.get("url"),
                    thumbnailurl = dictApi.get("thumbnailUrl")
                )
    db.session.add(photo_add)
    db.session.commit()
    return  jsonify({'POST OK':dictApi})

#GET PHOTO BY ID
@app.route('/api/photos/<int:photo_id>')
def apiPhotoIdGet(photo_id):
    photo    = Photo.query.filter_by(id=photo_id).first()
    dictApi = {
        "albumId" : photo.albumId,
        "id" : photo.id,
        "title" : photo.title,
        "url" : photo.url,
        "thumbnailurl" : photo.thumbnailurl
    }
    return  jsonify(dictApi)
#MODIFY A PHOTO BY ID
@app.route('/api/photos/<int:photo_id>', methods=['PUT'])
def apiPhotoIdPut(photo_id):
    photo              = Photo.query.filter_by(id=photo_id).first()
    req                = request.get_json()
    photo.albumId      = req.get("albumId")
    photo.id           = req.get("id")
    photo.title        = req.get("title")
    photo.url          = req.get("url")
    photo.thumbnailurl = req.get("thumbnailurl")
    db.session.commit()
    return  jsonify({"PUT OK":req})
#DELETE A PHOTO BY ID
@app.route('/api/photos/<int:photo_id>', methods=['DELETE'])
def apiPhotoIdDelete(photo_id):  
    photo = Photo.query.filter_by(id=photo_id).first()
    dictApi = {
        "id"           : getId(Photo),
        "albumId"      : photo.albumId,
        "id"           : photo.id,
        "title"        : photo.title,
        "url"          : photo.url,
        "thumbnailUrl" : photo.thumbnailurl
    }
    photo.archive = True
    db.session.commit()
    return  jsonify({"DELETE OK":dictApi})    


"""######           TODOS validate         ######"""
#GET ALL TODOS ON DATABASE
@app.route('/api/todos')
def apiTodosGet():
    Todos    = Todo.query.filter_by(archive=False)
    dictApi = []
    for todo in Todos:
        dictApi.append({
            "userId" : todo.userId,
            "id"     : todo.id,
            "title"  : todo.title,
            "completed":todo.completed
        })
    try:
        return  jsonify(dictApi) #render_template('apiPosts.html', dictApi=dictApi)
    except:
        return jsonify({"Error": "Request doesn't work well !"})
#Post a new todos on database
@app.route('/api/todos', methods=['POST'])
def apiTodosPost():
    #POST A NEW POST
    dictApi = {
        "userId" : request.json['userId'],
        "id"     : getId(Todo),
        "title"  : request.json['title'],
        "completed":request.json['completed']
    }
    todo_add = Post(
                    id=dictApi.get("id"),
                    userId=dictApi.get("userId"),
                    title=dictApi.get("title"),
                    body=dictApi.get("completed")
                )
    db.session.add(todo_add)
    db.session.commit()
    try:
        return  jsonify({'POST OK':dictApi})
    except:
        return jsonify({"Error": "Request doesn't work well !"})

#GET A TODOS BY ID
@app.route('/api/todos/<int:todos_id>')
def apiTodosIdGet(todos_id):
    data = dict()
    todo = Todo.query.get_or_404(todos_id)
    data = {
            "userId" : todo.userId,
            "id"     : todo.id,
            "title"  : todo.title,
            "completed":todo.completed
    }
    return data
# MODIFY A TODOS BY ID
@app.route('/api/todos/<int:todos_id>', methods=['PUT'])
def apiTodosIdPut(todos_id):
    todo = Todo.query.filter_by(id=todos_id).first()
    req = request.get_json()
    todo.postId = req.get("userId")
    todo.name = req.get("id")
    todo.email = req.get("title")
    todo.body = req.get("completed")
    db.session.commit()
    return  jsonify({"OK PUT":req})
#DELETE A COMMENT BY ID
@app.route('/api/todos/<int:todos_id>', methods=['DELETE'])
def apiTodosIdDelete(todos_id):
        todo = Todo.query.filter_by(id=todos_id).first()
        todo.archive = True
        data = {
                'id'     : todo.id,
                'postId' : todo.userId,
                'name'   : todo.title,
                'email'  : todo.completed
        }
        db.session.commit()
        return jsonify({"DELETED":data})



"""
############################################################################################
##                                     VIEW API                                           ##
############################################################################################
"""



@app.route('/api_home', methods=['GET','PUT','DELETE'])
def apis():
    # if ('user' in session):
    #     return render_template('api.html', session=session)
    # else:
        return render_template('api.html')

@app.route('/')
def apiConnect():
    return render_template('apiConnect.html')
@app.route('/', methods=['POST'])
def apiConnectPost():
    email = request.form['email'],
    password = request.form['password']
    user = Utilisateur.query.filter_by(email=email[0],password=password).first()
    if user!=None:
        # flash('connexion réussie')
        return redirect(url_for('apis'))
    else:
        # flash('Mot de passe incorrect')
        return render_template('apiConnect.html')

@app.route('/add_utilisateur')
def apiAddUtilisateurGet():
    return render_template('apiAddUtilisateur.html')

@app.route('/add_utilisateur', methods=['POST'])
def apiAddUtilisateur():
    utilisateur = Utilisateur(
        email = request.form['email'],
        password = request.form['password'],
        profil = request.form['profil']
    )
    try:
        db.session.add(utilisateur)
        db.session.commit()
        return render_template('api.html')
    except:
        return render_template('apiAddUtilisateur.html')




if __name__=='__main__':
    app.run(debug=True, port=5004)
    