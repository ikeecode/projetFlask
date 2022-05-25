from crypt import methods
from webbrowser import get
from flask import Flask, jsonify, render_template, redirect, url_for, request, flash, abort
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
@app.route('/api/users', methods=['GET','POST'])
def apiUsers():
    Users = User.query
    if request.method=='GET':
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
        return jsonify(dictApi)
    # POST A NEW USER
    elif request.method == 'POST':
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
        return  jsonify({'POST OK':dictApi})
    else:
        return 'ERROR'


@app.route('/api/users/<int:user_id>', methods=['GET','POST'])
def apiUserId(user_id):
    if request.method=='GET':
        dictApi ={}
        user = User.query.filter_by(id=user_id).first()
        Addresses = (User.query.filter_by(id=user_id).first()).address
        Companies = (User.query.filter_by(id=user_id).first()).company
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

        return jsonify(dictApi)
    #DELETE A POST BY ID
    elif request.method=='DELETE':  
        user = User.query.filter_by(id=user_id).first()
        user.archive = False
        db.session.commit()
        return  jsonify({"DELETE OK"})    
    else:
        return "ERROR"


"""######           POST validate         ######"""
@app.route('/api/posts', methods=['GET','POST'])
def apiPosts():
    #GET ALL POST ON DATABASE
    if request.method == 'GET':
        Posts    = Post.query
        dictApi = []
        for post in Posts:
            dictApi.append({
                "userId" : post.userId,
                "idApi" : post.idApi,
                "title" : post.title,
                "body" : post.body,
            })
        return  jsonify(dictApi)
    #POST A NEW POST
    elif request.method == 'POST':
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
        return  jsonify({'POST OK':dictApi})
    else:
        return 'ERROR'


@app.route('/api/posts/<int:post_id>', methods=['GET','PUT','DELETE'])
def apiPostId(post_id):
    #GET POST BY ID
    if request.method=='GET':
        post    = Post.query.filter_by(id=post_id).first()
        dictApi = {
            "userId" : post.userId,
            "idApi" : post.idApi,
            "title" : post.title,
            "body" : post.body,
        }
        return  jsonify(dictApi)
    #MODIFY A POST BY ID
    elif request.method=='PUT':
        post = Post.query.filter_by(id=post_id).first()
        req = request.get_json()
        post.title = req.get("title")
        post.userId = req.get("userId")
        post.body = req.get("body")
        db.session.commit()
        return  jsonify({"PUT OK":req})
    #DELETE A POST BY ID
    elif request.method=='DELETE':  
        post = Post.query.filter_by(id=post_id).first()
        dictApi = {
            "userId" : post.userId,
            "idApi" : post.idApi,
            "title" : post.title,
            "body" : post.body,
        }
        post.archive = False
        db.session.commit()
        return  jsonify({"DELETE OK":dictApi})    
    else:
        return "ERROR"

@app.route('/api/posts/<int:post_id>/comments', methods=['GET','DELETE'])
def apiPostComments(post_id):
    dictApi = []
    if request.method=='GET':
        ePost = Post.query.filter_by(id=post_id).first()
        for comment in list(ePost.comments):
            dictApi.append({
                "postId" : comment.postId,
                "name"   : comment.name,
                "email"  : comment.email,
                "body"   : comment.body,
            })
        return  jsonify(dictApi)
    elif request.method=='DELETE':
        Comments = Comment.query.filter_by(postId=post_id)
        for comment in Comments:
            comment.archive=False
        return  "DELETED"
    else:
        return "ERROR"

@app.route('/api/user/<int:user_id>/albums', methods=['GET','DELETE'])
def apiPostAlbums(user_id):
    dictApi = []
    if request.method=='GET':
        Users = User.query.filter_by(id=user_id).first()
        for album in list(Users.albums):
            dictApi.append({
                "userId" : album.userId,
                "id"     : album.id,
                "title"  : album.title
            })
        return  jsonify(dictApi)
    elif request.method=='DELETE':
        Albums = Album.query.filter_by(userId=user_id)
        for album in Albums:
            album.archive=False
        return  "DELETED"
    else:
        return "ERROR"




@app.route('/api/user/<int:post_id>/todos', methods=['GET','DELETE'])
def apiPostTodos(post_id):
    dictApi = []
    if request.method=='GET':
        Posts = Post.query.filter_by(id=post_id).first()
        for todos in list(Posts.todos):
            dictApi.append({
                "userId" : todos.userId,
                "id"     : todos.id,
                "title"  : todos.title,
                "completed":todos.completed
            })
        return  jsonify(dictApi)
    elif request.method=='DELETE':
        todos = Todo.query.filter_by(postId=post_id)
        for todo in todos:
            todo.archive=False
        return  "DELETED"
    else:
        return "ERROR"



"""#######       COMMENTS           ######"""
#DONE
@app.route('/api/comments', methods=['GET','POST'])
def apiComments():
    #GET ALL COMMENTS ON DATABASE
    if request.method=='GET':
        Comments    = Comment.query
        dictApi = []
        for comment in Comments:
            dictApi.append({
                "postId" : comment.postId,
                "name" : comment.name,
                "email" : comment.email,
                "body" : comment.body,
            })
        return  jsonify(dictApi)
    #POST A NEW COMMENT
    elif request.method == 'POST':
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
        return jsonify("POST OK",dictApi)
    else:
        return"error"

#DONE
@app.route('/api/comments/<int:comment_id>', methods=['GET', 'PUT', 'DELETE'])
def apiCommentId(comment_id):
    #GET A COMMENT BY ID
    if request.method=='GET':
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
    elif request.method=='PUT':
        comment = Comment.query.filter_by(id=comment_id).first()
        req = request.get_json()
        comment.postId = req.get("postId")
        comment.name = req.get("name")
        comment.email = req.get("email")
        comment.body = req.get("body")
        db.session.commit()
        return  jsonify({"OK PUT":req})
    #DELETE A COMMENT BY ID
    elif request.method=='DELETE':
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
    else:
        return"error"


"""######           ALBUMS          ######"""
@app.route('/api/albums', methods=['GET','POST'])
def apiAlbums():
    #GET ALL ALBUMS ON DATABASE
    if request.method == 'GET':
        Albums    = Album.query
        dictApi = []
        for album in Albums:
            dictApi.append({
                "userId" : album.userId,
                "id" : album.id,
                "title" : album.title
            })
        return  jsonify(dictApi)
    #POST A NEW POST
    elif request.method == 'POST':
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
    else:
        return 'ERROR'


@app.route('/api/albums/<int:album_id>', methods=['GET','PUT','DELETE'])
def apiAlbumId(album_id):
    #GET ALBUM BY ID
    if request.method=='GET':
        album    = Album.query.filter_by(id=album_id).first()
        dictApi = {
            "userId" : album.userId,
            "id" : album.id,
            "title" : album.title
        }
        return  jsonify(dictApi)
    #MODIFY A ALBUM BY ID
    elif request.method=='PUT':
        album = Album.query.filter_by(id=album_id).first()
        req = request.get_json()
        album.title = req.get("title")
        album.userId = req.get("userId")
        db.session.commit()
        return  jsonify({"PUT OK":req})
    #DELETE A ALBUM BY ID
    elif request.method=='DELETE':  
        album = Album.query.filter_by(id=album_id).first()
        dictApi = {
            "userId" : album.userId,
            "id" : album.id,
            "title" : album.title
        }
        album.archive = True
        db.session.commit()
        return  jsonify({"DELETE OK":dictApi})    
    else:
        return "ERROR"


@app.route('/api/albums/<int:album_id>/photos', methods=['GET','DELETE'])
def apiAlbumsPhotos(photo_id):
    dictApi = []
    if request.method=='GET':
        Photos = Album.query.filter_by(id=photo_id).first()
        for photo in list(Photos.comments):
            dictApi.append({
                "postId" : photo.postId,
                "name"   : photo.name,
                "email"  : photo.email,
                "body"   : photo.body,
            })
        return  jsonify(dictApi)
    elif request.method=='DELETE':
        Photos = Photo.query.filter_by(albumId=photo_id)
        for photo in Photos:
            photo.archive=False
        return  "DELETED"
    else:
        return "ERROR"


"""######           PHOTOS          ######"""

@app.route('/api/photos', methods=['GET','POST'])
def apiPhotos():
    #GET ALL PHOTO ON DATABASE
    if request.method == 'GET':
        Photos    = Photo.query
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
    elif request.method == 'POST':
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
    else:
        return 'ERROR'


@app.route('/api/photos/<int:photo_id>', methods=['GET','PUT','DELETE'])
def apiPhotoId(photo_id):
    #GET PHOTO BY ID
    if request.method=='GET':
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
    elif request.method=='PUT':
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
    elif request.method=='DELETE':  
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
    else:
        return "ERROR"




# @app.route('/api/users/m/<int:user_id>', methods=['GET','POST'])
# def apiUserrId(user_id):
#     if request.method=='GET':
#         dictApi ={}
#         user = User.query.filter_by(id=user_id).first()
#         Addresses = (User.query.filter_by(id=user_id).first()).address
#         Companies = (User.query.filter_by(id=user_id).first()).company
#         dictApi={
#             "id": user.idApi,
#             "name": user.name,
#             "username": user.username,
#             "email": user.email,
#             "address": {
#             "street": Addresses.street,
#             "suite": Addresses.suite,
#             "city": Addresses.city,
#             "zipcode": Addresses.zipcode,
#             "geo": {
#                 "lat": Addresses.lat,
#                 "lng": Addresses.lng
#             }
#             },
#             "phone": user.phone,
#             "website": user.website,
#             "company": {
#             "name": Companies.name,
#             "catchPhrase": Companies.catchPhrase,
#             "bs": Companies.bs
#             }
#         }

#         return jsonify(dictApi)
#     elif request.method=='PUT':
#         addressJson = geoJson = companyJson = {}
#         user = User.query.filter_by(id=user_id).first()
#         company = (User.query.filter_by(id=user_id).first()).company
#         address = (User.query.filter_by(id=user_id).first()).address
#         print(user)
#         req = request.get_json()
#         print(req)
#         addressJson = req["address"]
#         print("ADRESSE : ",addressJson)
#         geoJson     = addressJson["geo"]
#         print("GEO : ",geoJson)
#         companyJson = req["company"]
#         # company.bs          = companyJson.get("bs")
#         # company.catchPhrase = companyJson.get("catchPhrase")
#         # company.name        = companyJson.get("name")

#         # address.city        = addressJson.get("city")
#         # address.geo         = addressJson.get("geo")
#         # address.lat         = geoJson.get("lat")
#         # address.lng         = geoJson.get("lng")
#         # address.street      = addressJson.get("street")
#         # address.suite       = addressJson.get("suite")
#         # address.zipcode     = addressJson.get("zipcode")
        
#         # user.name           = req.get("name")
#         # user.username       = req.get("username")
#         # user.phone          = req.get("phone")
#         # user.website        = req.get("website")
#         # user.email          = req.get("email")
#         # db.session.commit()
#         return  jsonify({"PUT OK":req})
#     #DELETE A POST BY ID
#     elif request.method=='DELETE':  
#         user = User.query.filter_by(id=user_id).first()
#         user.archive = False
#         db.session.commit()
#         return  jsonify({"DELETE OK"})    
#     else:
#         return "ERROR"

@app.route('/', methods=['GET','PUT','DELETE'])
def apis():
    # if request.method=='GET':
    return render_template('api.html')




if __name__=='__main__':
    app.run(debug=True, port=5004)

