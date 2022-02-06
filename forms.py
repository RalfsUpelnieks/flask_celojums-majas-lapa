from this import d
#from django.forms import EmailField
from flask_wtf import Form
#from wtforms import StringField
#from wtforms.fields.choices import SelectField
#from wtforms.fields.datetime import DateField
#from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired
from models import *
from flask_wtf import FlaskForm
from wtforms.fields import *


class AddAgencyForm(FlaskForm):
    name = StringField('Nosaukums', validators=[DataRequired()])
    address = StringField('Adrese', validators=[DataRequired()])
    phone_number = StringField('Numurs', validators=[DataRequired()])

class AddCountryForm(FlaskForm):
    country = StringField('Valsts nosaukums', validators=[DataRequired()])
    abbreviation = StringField('Saīsinājums', validators=[DataRequired()])

class AddTripForm(FlaskForm):
    agencies = Agency.query.all()
    countries = Country.query.all()

    agency = SelectField('Aģentūra', choices = agencies, validators=[DataRequired()])
    country_from = SelectField('Atiešanas valsts:', choices = countries, validators=[DataRequired()])
    country_to = SelectField('Galamērķa valsts:', choices = countries, validators=[DataRequired()])
    date_from = DateField('Izbraukšanas datums', validators=[DataRequired()])
    date_to = DateField('Ierašanās datums', validators=[DataRequired()])
    description = StringField('Paskaidrojums', validators=[DataRequired()])
    cost = IntegerField('Cena', validators=[DataRequired()])
    ticket_amount = IntegerField('Biļešu skaits', validators=[DataRequired()])

class AddUserForm(FlaskForm):
    email = EmailField('E-pasts', validators=[DataRequired()])
    password = PasswordField('Parole', validators=[DataRequired()])
    name = StringField('Vārds', validators=[DataRequired()])
    surname = StringField('Uzvārds', validators=[DataRequired()])

class SignInForm(FlaskForm):
    email = EmailField('E-pasts', validators=[DataRequired()])
    password = PasswordField('Parole', validators=[DataRequired()])