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
id = 4
# current_user_items  = User.query.filter_by(id=id).first()
# print("first",currSent_user_items)

# print("second",current_user_items)
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

myusers = Comment.query.order_by(Comment.id).all()
# for user in myusers:
#     print(user.archive)
# myusers = [item for item in myusers if not item.archive]
# print(myusers)

def getId(User):
    Users = User.query
    liste_ = []
    for user in Users:
        liste_.append(user.id)
    maximum_liste = max(liste_)
    return maximum_liste+1


YE =  (User.query.filter_by(id=4).first()).company
print(YE)
# print("GET ID",getId(Post))

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
# dictApiC = dictApiAddress = dictApiGeo = {}
# dictApi = {
#            "address": {
#             "city": "Rufisque",
#             "geo": {
#                 "lat": -53.9509,
#                 "lng": -44.4618
#             },
#             "street": "Vara Pame",
#             "suite": "Suite 099",
#             "zipcode": "90569-8771"
#         },
#         "company": {
#             "bs": "Autonomie scalable supply-chains",
#             "catchPhrase": "Active didactic contingency",
#             "name": "Est-Crist"
#         },
#         "email": "Mereme@melissa.tv",
#         "id": 2,
#         "name": "Mathilde Howell",
#         "phone": 869616,
#         "username": "Santoni",
#         "website": "merieme.net"
#         }
# # print(dictApi)
# dictApiAddress = dictApi["address"]
# # print(dictApiAddress)
# dictApiGeo = dictApiAddress["geo"]
# # print(dictApiGeo)
# dictApiCompany = dictApi["company"]
# print(dictApiCompany)


# dictApi = []
# id=1
# ePost = Post.query.filter_by(id=id).first()
# for comment in list(ePost.comments):
    
#     dictApi.append({
#         "postId" : comment.postId,
#         "name" : comment.name,
#         "email" : comment.email,
#         "body" : comment.body,
#     })
# print(dictApi)


# dictApicomm = {}
# for comment in Posts:
#     dictApicomm ["post"] = {
#         comment
#     }
# print(len(dictApicomm))



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



"""
# @app.route('/api/users/<int:user_id>', methods=['GET','POST'])
# def apiUserId(user_id):
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
#         req = request.get_json()
#         addressJson = req["address"]
#         geoJson     = addressJson["geo"]
#         companyJson = req["company"]
#         company.bs          = companyJson.get("bs")
#         company.catchPhrase = companyJson.get("catchPhrase")
#         company.name        = companyJson.get("name")

#         address.city        = addressJson.get("city")
#         address.geo         = addressJson.get("geo")
#         address.lat         = geoJson.get("lat")
#         address.lng         = geoJson.get("lng")
#         address.street      = addressJson.get("street")
#         address.suite       = addressJson.get("suite")
#         address.zipcode     = addressJson.get("zipcode")
        
#         user.name           = req.get("name")
#         user.username       = req.get("username")
#         user.phone          = req.get("phone")
#         user.website        = req.get("website")
#         user.email          = req.get("email")
#         db.session.commit()
#         return  jsonify({"PUT OK":req})
#     #DELETE A POST BY ID
#     elif request.method=='DELETE':  
#         user = User.query.filter_by(id=user_id).first()
#         user.archive = False
#         db.session.commit()
#         return  jsonify({"DELETE OK"})    
#     else:
#         return "ERROR"
"""