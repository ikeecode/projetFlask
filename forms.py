from flask_wtf import FlaskForm
# from flask_wtf.file import FileField
from wtforms import StringField, FloatField, PasswordField, SubmitField, IntegerField, TextAreaField, EmailField, TelField, URLField
from wtforms.validators import InputRequired, NumberRange

class GeneratorForm(FlaskForm):
    numberChosen = IntegerField('', validators=[InputRequired()])
    # generatorBtn = SubmitField('Charger des users')

class UserForm(FlaskForm):
    nameUser  = StringField('Name', validators=[InputRequired()])
    username  = StringField('Username', validators=[InputRequired()])
    email     = EmailField('Email', validators=[InputRequired()])
    phone     = TelField('Phone', validators=[InputRequired()])
    website   = StringField('Website', validators=[InputRequired()])
    password  = PasswordField('Password', validators=[InputRequired()])
    submit    = SubmitField('Valider les informations')

class AddressForm(FlaskForm):
    street   = StringField('Street', validators=[InputRequired()])
    suite    = StringField('Suite', validators=[InputRequired()])
    city     = StringField('City', validators=[InputRequired()])
    zipcode  = StringField('Zipcode', validators=[InputRequired()])
    lat      = FloatField('Latitude', validators=[InputRequired()])
    lng      = FloatField('Longitude', validators=[InputRequired()])

class CompanyForm(FlaskForm):
    name        = StringField('Name ', validators=[InputRequired()])
    catchPhrase = StringField('Catch Phrase ', validators=[InputRequired()])
    bs          = StringField('Bs ', validators=[InputRequired()])

class LoginForm(FlaskForm):
    login    = StringField('Login', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    logBtn   = SubmitField('Se connecter')


class Charger(FlaskForm):
    charger = SubmitField('Charger')

class PostForm(FlaskForm):
    title  = StringField('Title', validators=[InputRequired()])
    body   = TextAreaField('Body', validators=[InputRequired()])
    addBtn = SubmitField('Ajouter')


class CommentForm(FlaskForm):
    name    = StringField('Name', validators=[InputRequired()])
    email   = EmailField('Email', validators=[InputRequired()])
    body    = TextAreaField('Body', validators=[InputRequired()])
    addBtn  = SubmitField('Ajouter')



class AlbumForm(FlaskForm):
    title   = StringField('Title', validators=[InputRequired()])
    addBtn  = SubmitField('Ajouter')


class PhotoForm(FlaskForm):
    title        = StringField('Title', validators=[InputRequired()])
    url          = URLField('Photo url', validators=[InputRequired()])
    thumbnailurl = URLField('Thumbnail url', validators=[InputRequired()])
    addBtn       = SubmitField('Ajouter')

class TodoForm(FlaskForm):
    title  = StringField('Title', validators=[InputRequired()])
    addBtn = SubmitField('Ajouter')
    # completed = BooleanField('Etat')
