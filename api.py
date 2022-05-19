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
@app.route('/api/users')
def apiUsers():
    Users = User.query
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

@app.route('/api/users/<int:user_id>')
def apiUserId(user_id):
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

@app.route('/api/p/posts/<int:post_id>', methods=['PUT'])
def apiPoster(post_id):
    post = Post.query.filter_by(id=post_id).first()
    req = request.get_json()
    post.title = req.get("title")
    post.userId = req.get("userId")
    post.body = req.get("body")
    db.session.commit()
    return  "ok PUT"
    

@app.route('/api/posts/<int:post_id>')
def apiPostId(post_id):
    post    = Post.query.filter_by(id=post_id).first()
    dictApi = {
        "userId" : post.userId,
        "idApi" : post.idApi,
        "title" : post.title,
        "body" : post.body,
    }
    return  jsonify(dictApi)


@app.route('/api/posts', methods=['GET','POST'])
def apiPosts():
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
        return  "ok"
    else:
        return 'ERROR'

# @app.route('/api/posts',, methods=['GET', 'POST'])
# def apiPosts():
#     Posts    = Post.query

#     dictApi = {
#         "userId" : request.json['userId'],
#         "idApi" : request.json['idApi'],
#         "title" : request.json['title'],
#         "body" : request.json['body'],
#     }
#     addPost = Post()
#     return  jsonify(dictApi)

# @app.route('/api/posts/<int:post_id>/comments')
# def apiUserComments(post_id):
#     dictApi = []
#     Post = Post.query.filter_by(id=post_id).first()
#     for comment in list(Post.comments):
#         dictApi.append({
#             "postId" : comment.postId,
#             "name" : comment.name,
#             "email" : comment.email,
#             "body" : comment.body,
#         })
#     return  jsonify(dictApi)

# @app.route('/api/comments')
# def apiComments():
#     Comments    = Comment.query
#     dictApi = []
#     for comment in Comments:
#         dictApi.append({
#             "postId" : comment.postId,
#             "name" : comment.name,
#             "email" : comment.email,
#             "body" : comment.body,
#         })
#     return  jsonify(dictApi)

# #A REVOIR
# # @app.route('/api/comments')
# # def apiPostComments():
# #     Comments    = Comment.query
# #     dictApi = []
# #     for comment in Comments:
# #         dictApi.append({
# #             "postId" : comment.postId,
# #             "name" : comment.name,
# #             "email" : comment.email,
# #             "body" : comment.body,
# #         })
# #     return  jsonify(dictApi)





# @app.route('/donnees')
# def donnees():
#     Users = User.query
#     listNbrPost = []
#     for user in Users:
#         nbrPost = {user.name : len(user.posts)}
#         listNbrPost.append(nbrPost)
#     return render_template('donnees.html', listNbrPost=listNbrPost)

# @app.route('/donneestry')
# def donneestry():
#     Users = User.query
#     listNbrPost = []
#     for user in Users:
#         nbrPost = {user.name : len(user.posts)}
#         listNbrPost.append(nbrPost)
#     return render_template('donneestry.html', listNbrPost=listNbrPost)
# """
# #####################################
# #                 API               #
# #####################################
# """
# @app.route('/api/users')
# def apiUsers():
#     Users = User.query
#     dictApi = []
#     for user in Users:
#         id = user.id
#         Addresses = (User.query.filter_by(id=id).first()).address
#         Companies = (User.query.filter_by(id=id).first()).company
#         dictApi.append({
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
#         })
#     return jsonify(dictApi)

# @app.route('/api/users/<int:user_id>')
# def apiUserId(user_id):
#     dictApi ={}
#     user = User.query.filter_by(id=user_id).first()
#     Addresses = (User.query.filter_by(id=user_id).first()).address
#     Companies = (User.query.filter_by(id=user_id).first()).company
#     dictApi={
#         "id": user.idApi,
#         "name": user.name,
#         "username": user.username,
#         "email": user.email,
#         "address": {
#         "street": Addresses.street,
#         "suite": Addresses.suite,
#         "city": Addresses.city,
#         "zipcode": Addresses.zipcode,
#         "geo": {
#             "lat": Addresses.lat,
#             "lng": Addresses.lng
#         }
#         },
#         "phone": user.phone,
#         "website": user.website,
#         "company": {
#         "name": Companies.name,
#         "catchPhrase": Companies.catchPhrase,
#         "bs": Companies.bs
#         }
#     }

#     return jsonify(dictApi)

# @app.route('/api/posts')
# def apiPosts():
#     Posts    = Post.query
#     dictApi = []
#     for post in Posts:
#         dictApi.append({
#             "userId" : post.userId,
#             "idApi" : post.idApi,
#             "title" : post.title,
#             "body" : post.body,
#         })
#     return  jsonify(dictApi)

# @app.route('/api/posts/<int:post_id>')
# def apiPostId(post_id):
#     post    = Post.query.filter_by(id=post_id).first()
#     dictApi = {
#         "userId" : post.userId,
#         "idApi" : post.idApi,
#         "title" : post.title,
#         "body" : post.body,
#     }
#     return  jsonify(dictApi)

# # @app.route('/api/posts',, methods=['GET', 'POST'])
# # def apiPosts():
# #     Posts    = Post.query

# #     dictApi = {
# #         "userId" : request.json['userId'],
# #         "idApi" : request.json['idApi'],
# #         "title" : request.json['title'],
# #         "body" : request.json['body'],
# #     }
# #     addPost = Post()
# #     return  jsonify(dictApi)

# @app.route('/api/posts/<int:post_id>/comments')
# def apiUserComments(post_id):
#     dictApi = []
#     Post = Post.query.filter_by(id=post_id).first()
#     for comment in list(Post.comments):
#         dictApi.append({
#             "postId" : comment.postId,
#             "name" : comment.name,
#             "email" : comment.email,
#             "body" : comment.body,
#         })
#     return  jsonify(dictApi)

# @app.route('/api/comments')
# def apiComments():
#     Comments    = Comment.query
#     dictApi = []
#     for comment in Comments:
#         dictApi.append({
#             "postId" : comment.postId,
#             "name" : comment.name,
#             "email" : comment.email,
#             "body" : comment.body,
#         })
#     return  jsonify(dictApi)

# #A REVOIR
# @app.route('/api/comments')
# def apiPostComments():
#     Comments    = Comment.query
#     dictApi = []
#     for comment in Comments:
#         dictApi.append({
#             "postId" : comment.postId,
#             "name" : comment.name,
#             "email" : comment.email,
#             "body" : comment.body,
#         })
#     return  jsonify(dictApi)





if __name__=='__main__':
    app.run(debug=True)

