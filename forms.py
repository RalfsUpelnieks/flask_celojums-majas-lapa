from flask_wtf import Form
from wtforms import StringField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired
from models import Agency
from flask_wtf import FlaskForm


class AddAgencyForm(FlaskForm):
    name = StringField('Nosaukums', validators=[DataRequired()])
    address = StringField('Adrese', validators=[DataRequired()])
    phone_number = StringField('Numurs', validators=[DataRequired()])

class AddTripForm(FlaskForm):
    agencies = Agency.query.all()
    agency = SelectField('Aģentūra', choices = agencies, validators=[DataRequired()])
    country_from = StringField('Atiešanas valsts:', validators=[DataRequired()])
    country_to = StringField('Galamērķa valsts:', validators=[DataRequired()])
    date_from = DateField('Izbraukšanas datums', validators=[DataRequired()])
    date_to = DateField('Ierašanās datums', validators=[DataRequired()])
    description = StringField('Paskaidrojums', validators=[DataRequired()])
    cost = IntegerField('Cena', validators=[DataRequired()])
    ticket_amount = IntegerField('Biļešu skaits', validators=[DataRequired()])