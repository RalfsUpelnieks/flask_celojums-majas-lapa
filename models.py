from flask_sqlalchemy import SQLAlchemy
from settings import app

# Database Connection
db_name = 'travely_database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Agency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    number = db.Column(db.String(18))
    children = db.relationship("Trip", cascade="all, delete")
    def __repr__(self):
        return f'<Agency: {self.id} - {self.name}>'

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agency_id = db.Column(db.Integer, db.ForeignKey("agency.id"))
    country_from = db.Column(db.String(30))
    country_to = db.Column(db.String(30))
    date_from = db.Column(db.Date)
    date_to = db.Column(db.Date)
    description = db.Column(db.String(280))
    cost = db.Column(db.Float)
    ticket_amount = db.Column(db.Integer)
    views = db.Column(db.Integer)
    def __repr__(self):
        return f'<Trip: {self.country_from} - {self.country_to} from agency {self.agency_id}>'