import requests
from random import randint
from models.users import *

# offline work
from json import load

class FromApi:
    # api_url  = 'https://jsonplaceholder.typicode.com/'
    # api_url  = '../users.json' # offline work
    # api_url  = '../posts.json' # offline work

    compteur = 0

    # # online work
    # @classmethod
    # def api_to_json(cls, url):
    #     return requests.get(cls.api_url + url).json()

    # offline work
    @classmethod
    def api_to_json(cls, url):
        with open(f"../{url}.json", 'r') as file:
            return load(file)

    @classmethod
    def prepare_todos(cls, user_id):
        todos = cls.api_to_json('todos')
        for todo in todos:
            if todo.get('userId') == user_id:
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
        comments = cls.api_to_json('comments')
        for comment in comments:
            if comment.get('postId') == post_id:
                comment_instance = Comment(
                        postId   = comment.get('postId'),
                        name     = comment.get('name'),
                        email    = comment.get('email'),
                        body     = comment.get('body')
                )

                db.session.add(comment_instance)
        try:
            db.session.commit()
        except:
            db.session.rollback()



    @classmethod
    def prepare_posts(cls, user_id):
        posts = cls.api_to_json('posts')
        post_id = ''
        for i, post in enumerate(posts):
            if post.get('userId') == user_id:
                post_instance = Post(
                    userId    = post.get('userId'),
                    idApi     = post.get('id'),
                    fromApi   = True,
                    title     = post.get('title'),
                    body      = post.get('body')
                )
                post_id = post.get('id')
                db.session.add(post_instance)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        cls.prepare_comments(post_id)


    @classmethod
    def prepare_users(cls, number):

        # users = cls.api_to_json('users') #online work
        users = cls.api_to_json('users') #offline work

        compteur = 0

        addressInDB = [ad.suite   for   ad   in Address.query.all()]
        companyInDB = [cp.name    for   cp   in Company.query.all()]
        usersInDB   = [user.email for   user in User.query.all()]

        if number <= len(users):
            for i, user in enumerate(users):
                if cls.compteur == number + 1 :
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
                    try:
                        db.session.add(address_instance)
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

                # print(company_instance)

                if company_instance.name not in companyInDB:
                    try:
                        db.session.add(company_instance)
                        db.session.commit()
                    except:
                        db.session.rollback()



                ## retrieve address identificator
                addressId = Address.query.filter_by(suite=address.get('suite')).first().id

                ## retrieve company identificator
                companyId = Company.query.filter_by(name=company.get('name')).first().id

                ## create user object
                user_instance = User(
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




FromApi.prepare_users(10)
FromApi.prepare_posts(user_id=1)

FromApi.prepare_todos(1)
