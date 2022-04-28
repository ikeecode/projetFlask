import requests
from random import randint
from models.users import *

# offline work
from json import load

class FromApi:
    api_url  = 'https://jsonplaceholder.typicode.com/'
    # api_url  = '../users.json' # offline work
    # api_url  = '../posts.json' # offline work

    compteur = 0

    # online work
    @classmethod
    def api_to_json(cls, url):
        try:
            response = requests.get(cls.api_url + url).json()
            return response
        except:
            print('Verifiez la connexion')


    # # offline work
    # @classmethod
    # def api_to_json(cls, url):
    #     with open(f"../{url}.json", 'r') as file:
    #         return load(file)


    @classmethod
    def prepare_photos(cls, album_id):
        endpoint = f'albums/{album_id}/photos'
        photos   = cls.api_to_json(endpoint)
        for photo in photos:
            photo_instance    = Photo(
                albumId       = photo.get('albumId'),
                title         = photo.get('title'),
                url           = photo.get('url'),
                thumbnail_url = photo.get('thumbnailUrl')
            )

            db.session.add(photo_instance)


    @classmethod
    def prepare_albums(cls, user_id):
        endpoint = f'users/{user_id}/albums'
        albums = cls.api_to_json(endpoint)
        for album in albums:
            album_instance = Album(
                userId = album.get('userId'),
                idApi  = album.get('id'),
                title  = album.get('title')
            )
            # print(album_instance)
            db.session.add(album_instance)
            album_id = album.get('id')
            cls.prepare_photos(album_id)

        try:
            db.session.commit()
        except:
            db.session.rollback()



    @classmethod
    def prepare_todos(cls, user_id):
        endpoint = f'users/{user_id}/todos/'
        todos = cls.api_to_json(endpoint)
        for todo in todos:
            todo_instance = Todo(
                userId    = todo.get('userId'),
                title     = todo.get('title'),
                completed = todo.get('completed')
            )
            # print(todo_instance)
            db.session.add(todo_instance)
        try:
            db.session.commit()
        except:
            db.session.rollback()



    @classmethod
    def prepare_comments(cls, post_id):
        endpoint = f'posts/{post_id}/comments/'
        comments = cls.api_to_json(endpoint)
        for comment in comments:
            comment_instance = Comment(
                    postId   = comment.get('postId'),
                    name     = comment.get('name'),
                    email    = comment.get('email'),
                    body     = comment.get('body')
            )
            # print(comment_instance)
            db.session.add(comment_instance)


    @classmethod
    def prepare_posts(cls, user_id):
        endpoint = f'users/{user_id}/posts/'
        posts = cls.api_to_json(endpoint)
        for i, post in enumerate(posts):
            post_instance = Post(
                userId    = post.get('userId'),
                idApi     = post.get('id'),
                fromApi   = True,
                title     = post.get('title'),
                body      = post.get('body')
            )
            db.session.add(post_instance)
            post_id = post.get('id')
            # print(post_id)
            # print('chargement des commentaires du posts ' + str(post_id))
            cls.prepare_comments(post_id)

        try:
            db.session.commit()
        except:
            db.session.rollback()


    @classmethod
    def prepare_users(cls, number):

        users = cls.api_to_json('users') #online work
        # users = cls.api_to_json('users') #offline work

        compteur = 0

        addressInDB = [ad.suite   for   ad   in Address.query.all()]
        companyInDB = [cp.name    for   cp   in Company.query.all()]
        usersInDB   = [user.email for   user in User.query.all()]

        if number <= len(users):
            for i, user in enumerate(users):
                if cls.compteur == number:
                    print('stop'*10)
                    break
                # print('number', number, 'compteur', cls.compteur)

                #  handling the address
                address = user.get('address')
                geo     = address.get('geo')

                # create an Address object
                address_instance = Address(
                        street   = address.get('street'),
                        suite    = address.get('suite'),
                        city     = address.get('city'),
                        zipcode  = address.get('zipcode'),
                        lat      = geo.get('lat'),
                        lng      = geo.get('lng')
                )

                # print(address_instance)
                if address_instance.suite not in addressInDB:
                    db.session.add(address_instance)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()



                # handling the company
                company             = user.get('company')
                company_instance    = Company(
                        name        = company.get('name'),
                        catchPhrase = company.get('catchPhrase'),
                        bs          = company.get('bs')
                )
                print(company_instance)
                # print(company_instance)

                if company_instance.name not in companyInDB:
                    db.session.add(company_instance)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()



                ## retrieve address identificator
                addressId = Address.query.filter_by(suite=address.get('suite')).first().id

                ## retrieve company identificator
                companyId = Company.query.filter_by(name=company.get('name')).first().id

                ## create user object
                user_instance     = User(
                        name      = user.get('name'),
                        idApi     = user.get('id'),
                        fromApi   = True,
                        username  = user.get('username'),
                        email     = user.get('email'),
                        addressId = addressId,
                        phone     = randint(200000, 1_000_000),
                        website   = user.get('website'),
                        companyId = companyId
                )

                if user_instance.email not in usersInDB:
                    db.session.add(user_instance)
                    try:
                        db.session.commit()
                        cls.compteur +=1
                        print('insertion..')
                    except:
                        db.session.rollback()
                        continue

        else:
            print('L\'api ne contient que 10 users')




# FromApi.prepare_users(number=1)
# FromApi.prepare_posts(user_id=1)
# FromApi.prepare_todos(user_id=1)
# FromApi.prepare_albums(1)
