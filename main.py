import os
from random import randint
from flask import render_template, redirect, request, Response
from flask.helpers import url_for
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired
from settings import app
from forms import *
from models import *
import json
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import desc
from werkzeug.utils import secure_filename

@app.route('/')
def index():
    qry = Trip.query.order_by(desc(Trip.views)).limit(4)
    return render_template("index.html", top_trips=qry, countries = Country.query.all())

@app.route('/catalogue')
def celojumi():
    return render_template("catalogue.html", trips = Trip.query.all(), countries = Country.query.all())

@app.route('/admin')
def admin():
    return redirect(url_for("admin_agencies"))

@app.route('/profile')
def profils():
    return render_template("profile.html", reservation = Reservation.query.all(), trips = Trip.query.all(), countries = Country.query.all())

@app.route('/register')
def register():
    return render_template("templates/register.html") # To Do

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/log_in')
def log_in():
    return render_template("log-in.html")

@app.route('/admin/agencies')
def admin_agencies():
    return render_template("templates/agencies.html", agencies = Agency.query.all())

@app.route('/admin/countries')
def admin_countries():
    return render_template("templates/countries.html", countries = Country.query.all(), agencies = Agency.query.all())

@app.route('/admin/trips')
def admin_trips():
    return render_template("templates/trips.html", trips = Trip.query.all(), agencies = Agency.query.all(), countries = Country.query.all())

# Aģentūru un ceļojumu pievienošana
@app.route('/admin/add')
def admin_add():
    return redirect(url_for("admin_add_agencies"))

@app.route('/admin/add/agencies', methods=['GET', 'POST'])
def admin_add_agencies():
    form = AddAgencyForm()
    if form.validate_on_submit():
        # --Gundars
        # Vēlāk šeit (un admin_add_trips()) tiks pievienotas datu pārbaudes
        # Pagaidām, lai būtu iespējams strādāt ar datiem, atstāšu tīrus inputus
        agency = Agency(name=form.name.data, address=form.address.data, number=form.phone_number.data)
        db.session.add(agency)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template("templates/add_agency.html", form=form)

@app.route('/admin/add/country', methods=['GET', 'POST'])
def admin_add_country():
    form = AddCountryForm()
    if form.validate_on_submit():
        country = Country(country=form.country.data, abbreviation=form.abbreviation.data)
        db.session.add(country)
        db.session.commit()
        return redirect(url_for('admin_countries'))
    return render_template("templates/add_country.html", form=form)

@app.route('/admin/add/trips', methods=['GET', 'POST'])
def admin_add_trips():
    # Lai dinamiski atjauninātu aģentūru sarakstu ceļojumu izveides lapā
    # Aģentūru izvēlnes attribūts tiek pievienots klases struktūrai, ne instancei
    agencies = SelectField('Aģentūra', choices=Agency.query.all(), validators=[DataRequired()])
    country_from = SelectField('Izceļošanas valsts', choices=Country.query.all(), validators=[DataRequired()])
    country_to = SelectField('Galamērķa valsts', choices=Country.query.all(), validators=[DataRequired()])

    setattr(AddTripForm, 'agency', agencies)
    setattr(AddTripForm, 'country_from', country_from)
    setattr(AddTripForm, 'country_to', country_to)
    
    # Pēc tā var izveidot 'form' objektu ar atjauninātu aģentūru sarakstu
    form = AddTripForm()
    if form.validate_on_submit():
        # Pārbaude
        agency = Agency.query.filter_by(name=form.agency.data).first().id
        country_from = Country.query.filter_by(country=form.country_from.data.split(",")[0]).first().id
        country_to = Country.query.filter_by(country=form.country_to.data.split(",")[0]).first().id

        img_name = secure_filename(form.photo.data.filename)
        img_path=os.path.join(app.root_path, 'static/images/destinations', img_name)
        form.photo.data.save(img_path)

        trip = Trip(
            agency_id=agency,
            country_from=country_from,
            country_to=country_to,
            date_from=form.date_from.data,
            date_to=form.date_to.data,
            description=form.description.data,
            cost=form.cost.data,
            ticket_amount=form.ticket_amount.data,
            img_file = img_name,
            views=0)
        db.session.add(trip)
        db.session.commit()
        return redirect(url_for('admin_trips'))
    return render_template("templates/add_trip.html", form=form)

# Aģentūru un ceļojumu dzēšana
@app.route('/admin/remove/agency/<int:id>')
def admin_remove_agency(id):
    remove_agency = Agency.query.filter_by(id=id).first()
    db.session.delete(remove_agency)
    db.session.commit()
    return redirect(url_for('admin_agencies'))

@app.route('/admin/remove/country/<int:id>')
def admin_remove_country(id):
    remove_country = Country.query.filter_by(id=id).first()
    db.session.delete(remove_country)
    db.session.commit()
    return redirect(url_for('admin_countries'))

@app.route('/admin/remove/trip/<int:id>')
def admin_remove_trip(id):
    remove_trip = Trip.query.filter_by(id=id).first()
    db.session.delete(remove_trip)
    db.session.commit()
    return redirect(url_for('admin_trips'))

@app.route('/sign_up', methods=['POST'])
def sign_up():
    form = AddUserForm()
    if request.method == "POST":
        user = User(
            email = request.form['email'],
            password = generate_password_hash(request.form['password'], method='sha256'),
            name = request.form['name'],
            surname = request.form['surname'],
            role_id = 0 )
        db.session.add(user)
        db.session.commit()
        return str(user)
    return "404"

@app.route('/sign_in', methods=['POST'])
def sign_in():
    form = SignInForm()
    if request.method == "POST":
        user = User.query.filter_by(email=request.form['email']).first()
        if not user or not check_password_hash(user.password, request.form['password']):
            return "Nav tāds lietotājs"
        else:
            return str(user)

    return "404"
    # return render_template("templates/register.html") # To Do

#rezervācijas sistēma
@app.route('/reservation/<int:id>')
def reservation(id):
    trip = Trip.query.get(id)
    trip.views += 1
    db.session.commit()
    return render_template("reservation.html", trip = trip, countries = Country.query.all())
    

@app.route('/reservation/add/<int:id>')
def reservation_add(id):
    user = 1
    id = randint(100000000, 1000000000)
    if(Reservation.query.get(id)):
        id = randint(100000000, 1000000000)
    reservation = Reservation(id = id, user_id=user, trip_id=id)
    db.session.add(reservation)
    db.session.commit()
    return redirect(url_for('celojumi'))

# Aģentūru un ceļojumu dzēšana
@app.route('/reservation/remove/<int:id>')
def reservation_remove(id):
    remove_reservation = Reservation.query.filter_by(id=id).first()
    db.session.delete(remove_reservation)
    db.session.commit()
    return redirect(url_for('profils'))

@app.route('/catalogue_filter', methods=["POST"])
def catalogue_filtes():
    country_from = None if not request.form['from'] else int(request.form['from'])
    country_to = None if not request.form['to'] else int(request.form['to'])
    from_date = None if not request.form['from_date'] else datetime.strptime(request.form['from_date'], '%Y-%m-%d').date()
    to_date = None if not request.form['to_date'] else datetime.strptime(request.form['to_date'], '%Y-%m-%d').date()
    Trips = Trip.query.filter((Trip.country_from == country_from) | (Trip.country_to == country_to) | (Trip.date_from == from_date) | (Trip.date_to == to_date)).all()
    output = []

    for trip in Trips:
        if (country_from != None and int(trip.country_from) != int(country_from) or
            country_to != None and int(trip.country_to) != int(country_to) or
            from_date != None and trip.date_from != from_date or
            to_date != None and trip.date_to != to_date):
            continue

        trip.cost = float(trip.cost)
        trip = trip.serialize()
        trip['country_from'] = Country.query.filter(Country.id==trip['country_from_id']).first().country
        trip['country_to'] = Country.query.filter(Country.id==trip['country_to_id']).first().country
        output.append(trip)
    return Response(json.dumps(output, default=str), mimetype='application/json')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)