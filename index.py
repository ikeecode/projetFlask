from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from folium import Map, Marker
from flask_migrate import Migrate
# from flask_googlemaps import GoogleMaps, Map
from random import randint
from string import ascii_letters
from fromApi import FromApi as fp
from models.users import (User, Address, Company, Post, Album, Photo, Todo, Comment, app, db)
from forms import *
import requests
from random import choice

# from models.users import app, db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kaba:ikeecode@localhost/flasko'
app.config['SECRET_KEY'] = "kfvbsdkfgsfgnkg(_çty( fdbdsd))"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config['GOOGLEMAPS_KEY'] = 'AIzaSyCi1YySTBjwmSZ3BmmgIRYs-rHcgC0-zCY'

db.init_app(app)

Bootstrap(app)
# GoogleMaps(app)
migrate = Migrate(app, db)

# login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'logIn'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def randomPassword():
    password=''
    for i in range(3):
        password += ascii_letters[randint(0, 26)]

    return password
#
# @app.route("/map/")
# def mapview():
#     # creating a map in the view
#     mymap = Map(
#         identifier="view-side",
#         lat=37.4419,
#         lng=-122.1419,
#         markers=[(37.4419, -122.1419)]
#     )
#     sndmap = Map(
#         identifier="sndmap",
#         lat=37.4419,
#         lng=-122.1419,
#         markers=[
#           {
#              'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
#              'lat': 37.4419,
#              'lng': -122.1419,
#              'infobox': "<b>Hello World</b>"
#           },
#           {
#              'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
#              'lat': 37.4300,
#              'lng': -122.1400,
#              'infobox': "<b>Hello World from other place</b>"
#           }
#         ]
#     )
#     return render_template('example.html', mymap=mymap, sndmap=sndmap)



# la page principale
@app.route('/', methods=['GET', 'POST'])
def chargementUser():
    number      = 0
    myusers     = []
    userLength  = 0
    genForm     = GeneratorForm()

    if genForm.validate_on_submit():
        number = genForm.numberChosen.data
        if number < 0:
            flash('Evitez de mettre un nombre negatif')
        userDataNumber = User.query.order_by(User.id).count()
        # print(userDataNumber, '='*20)
        if number > userDataNumber:
            number_to_add = number - userDataNumber
            try:
                fp.prepare_users(number_to_add)
            except:
                pass
            myusers = User.query.order_by(User.id).all()
            myusers = [item for item in myusers if not item.archive]

        myusers = User.query.order_by(User.id).all()
        myusers = [item for item in myusers if not item.archive]

        userLength = len(myusers)
        # print('userLength', userLength)
        # print(myusers)

    return render_template('loadUsers.html',
                            myusers=myusers,
                            number=number,
                            userLength=userLength,
                            genForm=genForm)


# la page de connexion

# @app.route('/chargement/connexion/<string:email>', methods=['GET', 'POST'])
@app.route('/connexion/', methods=['GET', 'POST'])
def logIn():
    form = LoginForm()
    # form.login.data = email
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.login.data).first()
        if user:
            # print('this user exists')
            if user.password == None:
                flash('No previous password!')
                password = randomPassword()
                flash('Votre mot de passe est '+ password)
                user.password = password
                # print(password)
                # db.session.add(user)
                db.session.commit()
            elif user.password != form.password.data:
                flash('Votre mot de passe est incorrect !')

            elif user.password == form.password.data:
                flash('Bienvenue sur votre profile !')
                login_user(user)
                return redirect(url_for('userMenu', next=request.endpoint))
        else:
            flash('Cet Utilisateur n\'existe pas dans la base ! ')

    return render_template('login.html', form=form)


# le menu Utilisateur
@app.route('/menu/', methods=['GET', 'POST'])
@login_required
def userMenu():
    mon_menu = ['post', 'todos', 'albums', 'infosuser']
    return render_template('user_menu.html', mon_menu=mon_menu)


# se deconnecter
@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logOut():
    logout_user()
    flash('You have been logged out !')
    return redirect(url_for('logIn'))

@app.route('/menu/menuItem/infosuser/carte')
@login_required
def folium_map():
    user_address = Address.query.get(current_user.id)
    coordonnees = (user_address.lat, user_address.lng)
    tooltip = 'Appuyer'
    message = 'Vous etes chez ' + current_user.name
    folium_map  = Map(location=coordonnees, zoom_start=10, tiles ='OpenStreetMap')
    Marker(coordonnees, popup=f"<strong>{message}</strong>", tooltip=tooltip).add_to(folium_map)

    return folium_map._repr_html_()

@app.route('/photo/<int:photo_id>')
@login_required
def view(photo_id):
    photo = Photo.query.get(photo_id)
    return render_template('photo.html', photo=photo)

@app.route('/album/<int:album_id>/photos')
@login_required
def view_photos(album_id):
    photos = Album.query.filter_by(idApi=int(album_id)).first().photos
    photosLength = len(photos)
    return render_template('photos.html', photos=photos, photosLength=photosLength)

@app.route('/menu/menuItem/<string:item>', methods=['GET', 'POST'])
@login_required
def menuItem(item):
    current_user_items = ['']
    itemLength = 0
    # visitez la page post
    # les items sont les options du menu

    if item == 'infosuser':
        user_address = Address.query.get(current_user.id)
        user_company = Company.query.get(current_user.id)
        return render_template(
                'infos_user.html',
                user_address=user_address,
                user_company=user_company,
        )
    elif item == 'post':
        # chargerPost = Charger()
        current_user_items  = User.query.filter_by(idApi=current_user.idApi).first().posts
        current_user_items  = [item for item in current_user_items if item.archive==False]

        itemLength = len(current_user_items)
        if request.method == 'POST':
            if request.form['submit-button'] == 'charger':
                # print('clicked ')
                try:
                    fp.prepare_posts(user_id=current_user.idApi)
                except:
                    # flash('Posts of '+ current_user.email + ' already loaded ')
                    pass
                # current_user_items  = Post.query.filter_by(userId=current_user.idApi).all()
                current_user_items  = User.query.filter_by(idApi=current_user.idApi).first().posts
                current_user_items  = [item for item in current_user_items if item.archive==False]
                itemLength = len(current_user_items)

                return render_template(
                    "post.html",
                    current_user_items=current_user_items,
                    itemLength=itemLength
                )

            elif request.form['submit-button'] == 'ajouter':
                if current_user.idApi:
                    return redirect(url_for('ajouterPost'))
                else:
                    return redirect(url_for('ajouterPost'))
            return render_template(
                "post.html",
                current_user_items=current_user_items,
                itemLength=itemLength
            )

    elif item == 'todos':
        current_user_items  = User.query.filter_by(idApi=current_user.idApi).first().todos #this change
        current_user_items  = [item for item in current_user_items if not item.archive]
        itemLength = len(current_user_items)
        if request.method == 'POST':
            if request.form['submit-button'] == 'charger':
                try:
                    fp.prepare_todos(user_id=current_user.idApi) #this change
                except:
                    # flash('Todos of '+ current_user.email + ' already loaded ')
                    pass

                current_user_items  = User.query.filter_by(idApi=current_user.idApi).first().todos #this change
                itemLength = len(current_user_items)

                return render_template(
                    "todos.html", #this change
                    current_user_items=current_user_items,
                    itemLength=itemLength
                )

            elif request.form['submit-button'] == 'ajouter':
                if current_user.idApi:
                    return redirect(url_for('ajouterTodo')) #this change
                else:
                    return redirect(url_for('ajouterTodo')) #this change
            return render_template(
                "todos.html", #this change
                current_user_items=current_user_items,
                itemLength=itemLength
            )

    elif item == 'albums':
        if current_user.fromApi:
            current_user_items  = User.query.filter_by(idApi=current_user.idApi).first().albums
        else:
            current_user_items  = User.query.filter_by(id=current_user.id).first().albums

        itemLength = len(current_user_items)
        if request.method == 'POST':
            if request.form['submit-button'] == 'charger':
                # fp.prepare_albums(user_id=current_user.idApi)

                try:
                    fp.prepare_albums(user_id=current_user.idApi)
                except:
                    # flash('Albums of '+ current_user.email + ' already loaded ')
                    print('there is an error ')
                    pass

                current_user_items  = User.query.filter_by(idApi=current_user.idApi).first().albums
                itemLength = len(current_user_items)

                return render_template("albums.html", current_user_items=current_user_items, itemLength=itemLength)

            elif request.form['submit-button'] == 'ajouter':
                if current_user.idApi:
                    return redirect(url_for('ajouterAlbum'))
                else:
                    return redirect(url_for('ajouterAlbum'))
            return render_template("albums.html", current_user_items=current_user_items, itemLength=itemLength)


    return render_template(f"{item}.html", current_user_items=current_user_items, itemLength=itemLength)

"""
######################################################################################################
    LES FONCTIONS QUI DONNENT AFFICHES LES ARCHIVES
######################################################################################################
"""

# affichage des archives

# ARCHIVES USERS
@app.route('/archive/users', methods=['GET', 'POST'])
def userArchive():
    genForm = GeneratorForm()
    current_user_items_from_archive  = User.query
    current_user_items_from_archive  = [item for item in current_user_items_from_archive if item.archive==True]
    itemLength = len(current_user_items_from_archive)
    return render_template(
        "loadUsers.html",
        genForm=genForm,
        current_user_items_from_archive=current_user_items_from_archive,

        itemLength=itemLength
    )

# ARCHIVES POSTS
@app.route('/archive/post')
@login_required
def postArchive():
    current_user_items_from_archive  = User.query.filter_by(idApi=current_user.idApi).first().posts
    current_user_items_from_archive  = [item for item in current_user_items_from_archive if item.archive==True]
    itemLength = len(current_user_items_from_archive)
    return render_template(
        "post.html",
        current_user_items_from_archive=current_user_items_from_archive,
        itemLength=itemLength
    )

# ARCHIVES COMMENTAIRES D'UN POSTS
@app.route('/archive/post/<int:post_id>/comments')
@login_required
def commentsArchive(post_id):
    current_user_items_from_archive = Post.query.filter_by(idApi=post_id).first().comments
    current_user_items_from_archive = [item for item in current_user_items_from_archive if item.archive]
    itemLength = len(current_user_items_from_archive)
    return render_template(
        "display_comments.html",
        current_user_items_from_archive=current_user_items_from_archive,
        itemLength=itemLength,
        post_id=post_id
    )

# ARCHIVES TODOS
@app.route('/archive/todos', methods=['GET', 'POST'])
@login_required
def todoArchive():
        current_user_items_from_archive  = User.query.filter_by(idApi=current_user.idApi).first().todos
        current_user_items_from_archive  = [item for item in current_user_items_from_archive if item.archive==True]
        itemLength = len(current_user_items_from_archive)
        return render_template(
            "todos.html",
            current_user_items_from_archive=current_user_items_from_archive,
            itemLength=itemLength
        )


"""
###############################################################################################################
LES FONCTIONS QUI PERMETTENT DE SUPPRIMER (ARCHIVER)
###############################################################################################################
"""

# SUPPRESSION DES USERS
@app.route('/delete/user/<int:user_id>')
def deleteUser(user_id):
    user_to_delete = User.query.get_or_404(user_id)
    if not user_to_delete.archive:
        user_to_delete.archive = True
        try:
            db.session.commit()
            flash("User deleted !")
            return redirect(url_for('chargementUser'))
        except:
            return redirect(url_for('chargementUser'))
    else:
        user_to_delete.archive = False
        db.session.commit()
        return redirect(url_for('chargementUser'))



# SUPPRESSION DES TODOS
@app.route('/delete/todo/<int:todo_id>')
@login_required
def deleteTodo(todo_id):
    todo_to_delete = Todo.query.get_or_404(todo_id)
    if not todo_to_delete.archive:
        todo_to_delete.archive = True
        db.session.commit()
        flash('Votre todo est supprimé !')
        return redirect(url_for('menuItem', item='todos'))
    else:
        todo_to_delete.archive = False
        db.session.commit()
        return redirect(url_for('menuItem', item='todos'))


# SUPPRESSION DES POSTS
@app.route('/delete/post/<int:post_id>')
@login_required
def deletePost(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    # print(post_to_delete.archive)
    if not post_to_delete.archive:
        post_to_delete.archive = True
        try:
            db.session.commit()
            flash('Votre post a été supprimé !')
            # print('commentaire supprimé')
            # print(post_to_delete.archive)

            return redirect(url_for('menuItem', item='post'))
        except:
            print('a problem occured')
            return redirect(url_for('menuItem', item='post'))
    elif post_to_delete.archive == True:
        post_to_delete.archive = False
        db.session.commit()
        return redirect(url_for('menuItem', item='post'))
    else:
        pass

# SUPPRESSION DES COMMENTAIRES
@app.route('/delete/comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def deleteComment(comment_id):
    print(comment_id)
    comment_to_delete = Comment.query.get_or_404(comment_id)
    print(comment_to_delete.postId, comment_to_delete.id)
    if not comment_to_delete.archive:
        comment_to_delete.archive = True
        try:
            db.session.commit()
            # flash('Le commentaire est supprimé !')
            return redirect(url_for('afficheComments', post_id=comment_to_delete.postId))
        except:
            # flash('Une erreur a eu lieu, veuillez reessayer ! ')
            return redirect(url_for('afficheComments', post_id=comment_to_delete.postId))
    elif comment_to_delete.archive:
        comment_to_delete.archive = False
        db.session.commit()
        return redirect(url_for('afficheComments', post_id=comment_to_delete.postId))
    else:
        pass



# FONCTION PERMETTANT L'AFFICHAGE DES COMMENTS D'UN POST
# afficher les commentaires d'un post
@app.route('/post/<int:post_id>/comments')
@login_required
def afficheComments(post_id):
    current_user_items = Post.query.filter_by(idApi=post_id).first().comments
    current_user_items = [item for item in current_user_items if not item.archive]
    itemLength = len(current_user_items)

    return render_template(
                            'display_comments.html',
                            current_user_items=current_user_items,
                            itemLength=itemLength,
                            post_id=post_id
                        )

"""
#####################################################################################################
LES FONCTIONS PERMETTANT DE FAIRE DES MODIFICATIONS (UPDATES)
#####################################################################################################
"""
# les modifications
@app.route('/update/infouser', methods=['GET', 'POST'])
@login_required
def updateInfoUser():
    user_address = Address.query.filter_by(id=current_user.addressId).first()
    user_company = Company.query.filter_by(id=current_user.companyId).first()

    formAddress = AddressForm()
    formCompany = CompanyForm()
    formUser    = UserForm()

    formCompany.name.data        = user_company.name
    formCompany.catchPhrase.data = user_company.catchPhrase
    formCompany.bs.data          = user_company.bs

    formAddress.street.data     = user_address.street
    formAddress.suite.data      = user_address.suite
    formAddress.city.data       = user_address.city
    formAddress.zipcode.data    = user_address.zipcode
    formAddress.lat.data        = user_address.lat
    formAddress.lng.data        = user_address.lng

    formUser.nameUser.data      = current_user.name
    formUser.username.data      = current_user.username
    formUser.email.data         = current_user.email
    formUser.phone.data         = current_user.phone
    formUser.website.data       = current_user.website
    formUser.password.data      = current_user.password

    if formUser.validate_on_submit():
    # if request.method ==   'POST':
            user_company.name        = request.form.get('name')
            user_company.catchPhrase = request.form.get('catchPhrase')
            user_company.bs          = request.form.get('bs')

            user_address.street      = request.form.get('street')
            user_address.suite       = request.form.get('suite')
            user_address.city        = request.form.get('city')
            user_address.zipcode     = request.form.get('zipcode')
            user_address.lat         = request.form.get('lat')
            user_address.lng         = request.form.get('lng')

            current_user.nameUser       = request.form.get('nameUser')
            current_user.username       = request.form.get('username')
            current_user.email          = request.form.get('email')
            current_user.phone          = request.form.get('phone')
            current_user.website        = request.form.get('website')
            current_user.password       = request.form.get('password')

            try:
                db.session.commit()
                return redirect(url_for('menuItem', item='infosuser'))
            except:
                return render_template(
                                        'update_infosuser.html',
                                        formAddress=formAddress,
                                        formCompany=formCompany,
                                        formUser=formUser
                                    )
    return render_template(
                            'update_infosuser.html',
                            formAddress=formAddress,
                            formCompany=formCompany,
                            formUser=formUser
                        )


@app.route('/update/album/<int:album_id>', methods=['GET', 'POST'])
@login_required
def updateAlbum(album_id):
    albumform = AlbumForm()
    album_to_update = Album.query.filter_by(id = album_id).first()
    # if not album_to_update.idApi:
    #     album_to_update = Album.query.filter_by(id=album_id).first()
    albumform.title.data = album_to_update.title

    if request.method == 'POST':
        album_to_update.title = request.form.get('title')
        db.session.commit()
        return redirect(url_for('menuItem', item='albums'))
    else:
        return render_template('update_album.html',
                                albumform=albumform,
                                album_to_update=album_to_update,
                                album_id=album_id
                                )

    return render_template('update_album.html',
                            albumform=albumform,
                            album_to_update=album_to_update
                            )


@app.route('/update/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def updatePost(post_id):
    postform = PostForm()
    post_to_update = Post.query.get_or_404(post_id)
    postform.title.data = post_to_update.title
    postform.body.data  = post_to_update.body
    if request.method == 'POST':
        post_to_update.title = request.form.get('title')
        post_to_update.body = request.form.get('body')
        try:
            db.session.commit()
            flash('Votre Post a été mis à jour !')
            return redirect(url_for('menuItem', item='post'))
        except:
            flash('Error! Looks like there is an error ')
            return render_template('update_post.html',
                            postform=postform,
                            post_to_update=post_to_update
                            )
    else:
        return render_template('update_post.html',
                        postform=postform,
                        post_to_update=post_to_update
                        )


@app.route('/update/comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def updateComment(comment_id):
    comment_to_update = Comment.query.get_or_404(comment_id)
    commentform = CommentForm()

    commentform.name.data   = comment_to_update.name
    commentform.email.data  = comment_to_update.email
    commentform.body.data   = comment_to_update.body

    if commentform.validate_on_submit():
        comment_to_update.name  = commentform.name.data
        comment_to_update.email = commentform.email.data
        comment_to_update.body  = commentform.body.data

        try:
            db.session.commit()
            return redirect(url_for('afficheComments', post_id=comment_to_update.postId))
        except:
            return render_template('update_comment.html',
                                    commentform=commentform,
                                    comment_to_update=comment_to_update,
                                    comment_id=comment_id)
    else:
        return render_template('update_comment.html',
                                commentform=commentform,
                                comment_to_update=comment_to_update,
                                comment_id=comment_id)

@app.route('/update/todo/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def updateTodo(todo_id):
    todo_to_update = Todo.query.get(todo_id)
    todoform = TodoForm()
    todoform.title.data = todo_to_update.title
    if request.method == 'POST':
        todo_to_update.title = request.form.get('title')
        try:
            db.session.commit()
            return redirect(url_for('menuItem', item='todos'))
        except:
            return render_template('update_todo.html',
                                    todoform=todoform,
                                    todo_to_update=todo_to_update
                                    )
    else:
        return render_template('update_todo.html',
                                todoform=todoform,
                                todo_to_update=todo_to_update
                                )


"""
###################################################################################################
LES FONCTIONS QUI PERMETTENT D'AJOUTER DANS LA BASE A TRAVERS UN FORMULAIRE
###################################################################################################

"""

# les routes des formulaires d'ajout
@app.route('/ajout/comment/<int:post_id>', methods=['GET', 'POST'])
@login_required
def ajouterComment(post_id):
    commentform = CommentForm()
    if commentform.validate_on_submit():
        comment_instance = Comment(
            postId  = post_id,
            name    = commentform.name.data,
            email   = commentform.email.data,
            body    = commentform.body.data,
            archive = False
        )
        db.session.add(comment_instance)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        commentform = CommentForm(formdata=None)
    return render_template('ajouter_comments.html', commentform=commentform, post_id=post_id)



@app.route('/ajout/post', methods=['GET', 'POST'])
@login_required
def ajouterPost():
    postform = PostForm()
    if postform.validate_on_submit():
        post_instance = Post(
            userId = current_user.idApi if current_user.idApi else current_user.id,
            idApi  = None,
            fromApi= False,
            title  = postform.title.data,
            body   = postform.body.data
        )
        db.session.add(post_instance)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        postform = PostForm(formdata=None)
    return render_template('ajouter_post.html', postform=postform)



@app.route('/ajout/todo', methods=['GET', 'POST'])
@login_required
def ajouterTodo():
    todoform = TodoForm()
    if todoform.validate_on_submit():
        todo_instance = Todo(
            userId  = current_user.idApi if current_user.fromApi else current_user.id,
            title   = todoform.title.data,
            completed = False
        )

        db.session.add(todo_instance)

        try:
            db.session.commit()
        except:
            db.session.rollback()

        todoform = TodoForm(formdata=None)
    return render_template('ajouter_todo.html', todoform=todoform)


@app.route('/ajout/album', methods=['GET', 'POST'])
@login_required
def ajouterAlbum():
    albumform = AlbumForm()
    if albumform.validate_on_submit():
        album_instance = Album(
            userId = current_user.idApi if current_user.fromApi else current_user.id,
            idApi  = None,
            title  = albumform.title.data
        )
        db.session.add(album_instance)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        albumform = AlbumForm(formdata=None)
    return render_template('ajouter_album.html', albumform=albumform)


@app.route('/ajout/user', methods=['GET', 'POST'])
def ajouter_user():
    # name = username = email = phone = password = submit = None
    formAddress = AddressForm()
    formCompany = CompanyForm()
    formUser    = UserForm()
    if formUser.validate_on_submit():
        userEmail    = User.query.filter_by(email=formUser.email.data).first()
        companyName  = Company.query.filter_by(name=formCompany.name.data).first()
        addressSuite = Address.query.filter_by(suite=formAddress.suite.data).first()

        if userEmail is None:
            userAddress = Address(
                street  = formAddress.street.data,
                suite   = formAddress.suite.data,
                city    = formAddress.city.data,
                zipcode = formAddress.zipcode.data,
                lat     = formAddress.lat.data,
                lng     = formAddress.lng.data,
            )
            try:
                db.session.add(userAddress)
                db.session.commit()
            except:
                db.session.rollback()

            userCompany = Company(
                name        = formCompany.name.data,
                catchPhrase = formCompany.catchPhrase.data,
                bs          = formCompany.bs.data,
            )

            try:
                db.session.add(userCompany)
                db.session.commit()
            except:
                db.session.rollback()


            userAddressId = Address.query.filter_by(suite=userAddress.suite).first()
            userCompanyId = Company.query.filter_by(name=userCompany.name).first()

            user = User(
                name      = formUser.nameUser.data,
                fromApi   = False,
                username  = formUser.username.data,
                email     = formUser.email.data,
                addressId = userAddressId.id,
                website   = formUser.website.data,
                phone     = formUser.phone.data,
                companyId = userCompanyId.id,
                password  = formUser.password.data,
            )
            try:
                db.session.add(user)
                db.session.commit()
            except:
                db.session.rollback()
        # emptying the form after submit
        formAddress = AddressForm(formdata=None)
        formCompany = CompanyForm(formdata=None)
        formUser    = UserForm(formdata=None)

    return render_template('ajouter_user.html',
                            formUser=formUser,
                            formAddress=formAddress,
                            formCompany=formCompany,
                            )


if __name__=='__main__':
    app.run(debug=True)
