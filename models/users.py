from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kaba:ikeecode@localhost/flasko'
app.config['SECRET_KEY'] = "kfvbsdkfgsfgnkg(_çty( fdbdsd))"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


# initialisation de la base de donnee
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#

class Address(db.Model):
    __tablename__ ='address'
    id       = db.Column(db.Integer, primary_key=True, nullable=False)
    street   = db.Column(db.String(200), nullable=False)
    suite    = db.Column(db.String(200), nullable=False, unique=True)
    city     = db.Column(db.String(200), nullable=False)
    zipcode  = db.Column(db.String(200), nullable=False)
    lat      = db.Column(db.Float, nullable=False)
    lng      = db.Column(db.Float, nullable=False)

    users    = db.relationship('User', backref='address', cascade='all, delete-orphan')

    def __str__(self):
        return f"Address(id:{self.id}, street:{self.street}, city:{self.city}, zipcode:{self.zipcode}), lat:{self.lat}, lng:{self.lng})"



class Company(db.Model):
    __tablename__ ='company'
    id          = db.Column(db.Integer, primary_key=True, nullable=False)
    name        = db.Column(db.String(200), nullable=False, unique=True)
    catchPhrase = db.Column(db.String(200), nullable=False)
    bs          = db.Column(db.String(200), nullable=False)

    users       = db.relationship('User', backref='company', cascade='all, delete-orphan')

    def __str__(self):
        return f"Company(id:{self.id}, name:{self.name}, catchPhrase:{self.catchPhrase}, bs:{self.bs})"

class User(UserMixin, db.Model):
    __tablename__ ='users'
    id        = db.Column(db.Integer, primary_key=True, nullable=False)
    idApi     = db.Column(db.Integer, nullable=True, unique=True)
    fromApi   = db.Column(db.Boolean, nullable=True, default=False)
    name      = db.Column(db.String(200), nullable=False)
    username  = db.Column(db.String(200), nullable=False, unique=True)
    email     = db.Column(db.String(200), unique=True, nullable=False, index=True)
    addressId = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    phone     = db.Column(db.Integer, nullable=False)
    website   = db.Column(db.String(200), nullable=False)
    companyId = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    password  = db.Column(db.String(200), nullable=True)

    todos     = db.relationship('Todo', backref='users', cascade='all, delete-orphan')
    albums    = db.relationship('Album', backref='users', cascade='all, delete-orphan')
    posts     = db.relationship('Post', backref='users', cascade='all, delete-orphan')


    def __str__(self):
        return f"User(id:{self.id}, name:{self.name}, username:{self.username}, email:{self.email}), phone:{self.phone}, website:{self.website})"



class Todo(db.Model):
    __tablename__ ='todos'
    userId    = db.Column(db.Integer, db.ForeignKey('users.idApi'), nullable=False)
    id        = db.Column(db.Integer, primary_key=True, nullable=False)
    title     = db.Column(db.String(200), nullable=False, unique=True)
    completed = db.Column(db.Boolean, nullable=False)


    def __str__(self):
        return f"Todo(id:{self.id}, title:{self.title}, completed:{self.completed}, userId:{self.userId})"

class Album(db.Model):
    __tablename__ ='albums'
    userId    = db.Column(db.Integer, db.ForeignKey('users.idApi'), nullable=False)
    id        = db.Column(db.Integer, primary_key=True, nullable=False)
    title     = db.Column(db.String(200), nullable=False, unique=True)
    photos    = db.relationship('Photo', backref='albums', cascade='all, delete-orphan')

    def __str__(self):
        return f"Album(userId:{self.userId}, id:{self.id}, title:{self.title})"



class Photo(db.Model):
    __tablename__ ='photos'
    albumId      = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=False)
    id           = db.Column(db.Integer, primary_key=True, nullable=False)
    title        = db.Column(db.String(200), nullable=False)
    url          = db.Column(db.String(200), nullable=False)
    thumbnailUrl = db.Column(db.LargeBinary, nullable=False)

    def __str__(self):
        return f"Photo(albumId:{self.albumId}, id:{self.id}, title:{self.title}, url:{self.url})"


class Post(db.Model):
    __tablename__ ='posts'
    id        = db.Column(db.Integer, primary_key=True, nullable=False)
    userId    = db.Column(db.Integer, db.ForeignKey('users.idApi'), nullable=False)
    idApi     = db.Column(db.Integer, nullable=True, unique=True)
    fromApi   = db.Column(db.Boolean, nullable=True, default=False)
    title     = db.Column(db.String(200), nullable=False)
    body      = db.Column(db.Text, nullable=False)
    comments  = db.relationship('Comment', backref='posts', cascade='all, delete-orphan')


    def __str__(self):
        return f"Post(userId:{self.userId}, id:{self.id}, title:{self.title})"


class Comment(db.Model):
    __tablename__ ='comments'
    postId = db.Column(db.Integer, db.ForeignKey('posts.idApi'), nullable=False)
    id     = db.Column(db.Integer, primary_key=True, nullable=False)
    name   = db.Column(db.String(200), nullable=False)
    email  = db.Column(db.String(200), nullable=False)
    body   = db.Column(db.Text, nullable=False)

    def __str__(self):
        return f"Comment(postId:{self.postId}, id:{self.id}, name:{self.name}, email:{self.email})"
