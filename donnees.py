from numpy import maximum
from models.users import *
import csv
import json

#recup from base
Userss    = User.query
Posts    = Post.query
Albums   = Album.query
Comments = Comment.query
listUtilisateur = listPost = listAlbum = listComment = listNbrPost= []

# nom collones
colonnes_users = ["id", "name", "username", "email","phone","website","idApi"]
colonnes_posts = ["id", "userId", "idApi", "fromApi", "title", "body"]
colonnes_comments = ["id", "postId", "name", "email", "body"]
colonnes_albums = ["id", "userId", "idApi", "title"]
# comment = {"id": l.id, "postId": l.postId, "name" : i.name, "email" : i.email, "body": l.body}
# album = {"id": l.id, "userId": l.userId, "idApi": l.idApi, "title": l.title}

# Userss = User.query
# for user in Userss:
#     id = user.id
#     fg = (User.query.filter_by(id=id).first()).address
#     print(fg.street)

def getId(User):
    Users = User.query
    liste_ = []
    for user in Users:
        liste_.append(user.id)
    maximum_liste = max(liste_)
    return maximum_liste+1

print("GET ID",getId(Post))

# dictApi ={}
# id= 1
# user = User.query.filter_by(id=id).first()
# Addresses = (User.query.filter_by(id=id).first()).address
# Companies = (User.query.filter_by(id=id).first()).company
# dictApi={
#     "id": user.idApi,
#     "name": user.name,
#     "username": user.username,
#     "email": user.email,
#     "address": {
#     "street": Addresses.street,
#     "suite": Addresses.suite,
#     "city": Addresses.city,
#     "zipcode": Addresses.zipcode,
#     "geo": {
#         "lat": Addresses.lat,
#         "lng": Addresses.lng
#     }
#     },
#     "phone": user.phone,
#     "website": user.website,
#     "company": {
#     "name": Companies.name,
#     "catchPhrase": Companies.catchPhrase,
#     "bs": Companies.bs
#     }
# }
# print(dictApi)


# dictApi = []
# id=1
# for user in Users:
#     id = user.id
#     Addresses = (User.query.filter_by(id=id).first()).address
#     Companies = (User.query.filter_by(id=id).first()).company
#     dictApi.append({
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
#     })
# print(dictApi)


# dictApi = {}
# id=1
# ePost = Post.query.filter_by(id=id).first()
# for comment in list(ePost.comments):
    
#     dictApi [str(comment.id)] = {
#         "postId" : comment.postId,
#         "name" : comment.name,
#         "email" : comment.email,
#         "body" : comment.body,
#     }
# print(dictApi)


# dictApicomm = {}
# for comment in Comments:
#     dictApicomm [str(comment.id)] = {
#         "postId" : comment.postId,
#         "name" : comment.name,
#         "email" : comment.email,
#         "body" : comment.body,
#     }



# id=1
# userComment = Comment.query.filter_by(postId=id).all().comments
# dictUserComment = {}
# for unique in userComment:
#     dictUserComment [str(unique.id)] = {
#         "postId" : unique.postId,
#         "name" : unique.name,
#         "email" : unique.email,
#         "body" : unique.body,
#     }
# # Unique = Album.query.filter_by(idApi=int(id)).first().photos
# print(dictUserComment)



# with open ("donneeJSON.json","w") as mon_fichier:
#     json.dump(listNbrPost, mon_fichier)
# # RECUP USERS
# for i in Users:
#     utilisateur = {"id" : i.id, "name" : i.name, "username" : i.username, "email" : i.email, "phone" : i.phone, "website" : i.website}
#     listUtilisateur.append(utilisateur)
# fichier = open('donneesCsv.csv', 'w')
# obj = csv.writer(fichier)
# with fichier:
#     obj = csv.DictWriter(fichier, fieldnames=colonnes_users)
#     obj.writeheader()
#     for k in listUtilisateur:
#         obj.writerow(k)

# # RECUP POSTS
# for l in Posts:
#     post = {"id": l.id, "userId": l.userId, "idApi": l.idApi, "fromApi": l.fromApi, "title": l.title, "body": l.body}
#     listPost.append(post)
# print(listPost)
# fichierPost = open('donneesPosts.csv', 'w')
# obj1 = csv.writer(fichierPost)
# with fichierPost:
#     obj1 = csv.DictWriter(fichierPost, fieldnames=colonnes_posts)
#     obj1.writeheader()
#     for m in listPost:
#         obj1.writerow(m)
