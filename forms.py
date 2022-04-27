from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, NumberRange


class GeneratorForm(FlaskForm):
    numberChosen = IntegerField('', validators=[InputRequired()])
    # generatorBtn = SubmitField('Charger des users')

class UserForm(FlaskForm):
    nameUser  = StringField('Name', validators=[InputRequired()])
    username  = StringField('Username', validators=[InputRequired()])
    email     = StringField('Email', validators=[InputRequired()])
    phone     = IntegerField('Phone', validators=[InputRequired(), NumberRange(min=0, max=1_000_000)])
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
    login = StringField('Login', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

    logBtn = SubmitField('Se connecter')


class Charger(FlaskForm):
    charger = SubmitField('Charger')
