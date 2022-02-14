from django import views
from settings import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

# Database

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

_metadata = MetaData(naming_convention=convention)

# Database Connection
db_name = 'travely_database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app, metadata=_metadata)

# Migrate
migrate = Migrate(app, db, render_as_batch=True)


class Agency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    number = db.Column(db.String(18))
    children = db.relationship("Trip", cascade="all, delete")
    def __repr__(self):
        return self.name

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(48), nullable=False)
    abbreviation = db.Column(db.String(2), nullable=False)
    def __repr__(self):
        return f'{self.country}, {self.abbreviation}'

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agency_id = db.Column(db.Integer, db.ForeignKey("agency.id"))
    country_from = db.Column(db.Integer)
    country_to = db.Column(db.Integer)
    date_from = db.Column(db.Date)
    date_to = db.Column(db.Date)
    description = db.Column(db.String(280))
    cost = db.Column(db.Float)
    ticket_amount = db.Column(db.Integer)
    views = db.Column(db.Integer)
    def __repr__(self):
        return f'<Trip: {self.country_from} - {self.country_to} from agency {self.agency_id}>'

    def get_agency_from_id(self):
        return Agency.query.filter(Agency.id == self.agency_id).first()
    
    def serialize(self):
        return {
            "id": self.id,
            "agency_id": self.agency_id,
            "country_from_id": self.country_from,
            "country_to_id": self.country_to,
            "country_from": "",
            "country_to": "",
            "date_from": self.date_from,
            "date_to": self.date_to,
            "description": self.description,
            "cost": self.cost,
            "ticket_amount": self.ticket_amount,
            "views": self.views
            }
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    role_id = db.Column(db.Integer)
    def __repr__(self):
        return f'User: {self.name} {self.surname}, roleID = {self.role_id}'
    

'''
set FLASK_APP=models.py

flask db init

flask db migrate -m "(nosaukums)"

flask db upgrade

flask db migrate -m "Atbilstoši, esmu pievienojis jaunu, kritiski vajadzīgu tabulu iekš jau iepriekšveidotās datubāzes, ko izmantojam šajā vietnē. Atbilstoši, tabulas nosaukums ir Country."
'''
