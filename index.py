from flask import Flask, render_template, redirect, url_for, request, flash, abort

from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from folium import Map, Marker
from random import randint
from string import ascii_letters
from fromApi import FromApi as fp
from models.users import (User, Address, Company, Post, app, db)
from forms import *

# from models.users import app, db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kaba:ikeecode@localhost/flasko'
app.config['SECRET_KEY'] = "kfvbsdkfgsfgnkg(_çty( fdbdsd))"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db.init_app(app)

Bootstrap(app)

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
        print(userDataNumber, '='*20)
        if number > userDataNumber:
            number_to_add = number - userDataNumber
            try:
                fp.prepare_users(number_to_add)
            except:
                pass
            myusers = User.query.order_by(User.id).all()

        myusers = User.query.order_by(User.id).all()
        userLength = len(myusers)
        # print('userLength', userLength)
        # print(myusers)

    return render_template('loadUsers.html',
                            myusers=myusers,
                            number=number,
                            userLength=userLength,
                            genForm=genForm)
# @app.route('/')
# def index():
#     form = UserForm()
#     return render_template('index.html', form=form)

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
                print(password)
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
        if request.method == 'POST':
            if request.form['submit-button'] == 'charger':
                # print('clicked ')
                try:
                    fp.prepare_posts(user_id=current_user.idApi)
                except:
                    flash('Posts of '+ current_user.email + ' already loaded ')
                # current_user_items  = Post.query.filter_by(userId=current_user.idApi).all()
                current_user_items  = User.query.filter_by(idApi=current_user.idApi).first().posts
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

    elif item == 'todos':
        if request.method == 'POST':
            if request.form['submit-button'] == 'charger':
                try:
                    fp.prepare_todos(user_id=current_user.idApi) #this change
                except:
                    flash('Todos of '+ current_user.email + ' already loaded ')

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
        if request.method == 'POST':
            if request.form['submit-button'] == 'charger':
                try:
                    fp.prepare_albums(user_id=current_user.idApi)
                except:
                    flash('Albums of '+ current_user.email + ' already loaded ')

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


@app.route('/ajout/post', methods=['GET', 'POST'])
@login_required
def ajouterPost():
    return render_template('ajouter_post.html')


@app.route('/ajout/todo', methods=['GET', 'POST'])
@login_required
def ajouterTodo():
    return render_template('ajouter_todo.html')


@app.route('/ajout/album', methods=['GET', 'POST'])
@login_required
def ajouterAlbum():
    return render_template('ajouter_album.html')

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
