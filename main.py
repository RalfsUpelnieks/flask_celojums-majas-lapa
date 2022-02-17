import os
from flask import render_template, redirect, request, Response, flash, session
from flask.helpers import url_for, send_file
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

def is_user_logged():
    return True if session.get('user') == True else False

def is_user_admin():
    if is_user_logged():
        return True if User.query.filter_by(id=session['user']).first().role_id != 0 else False
    else:
        return False

def get_user_data(id):
    return User.query.filter_by(id=id).first()

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
    if is_user_logged():
        return render_template("profile.html", reservations = Reservation.query.filter_by(owner_id=session['user']).all(), trips = Trip.query.all(), countries = Country.query.all(), user = get_user_data(session['user']))
    else:
        return redirect(url_for("login"))

@app.route('/register')
def register():
    return render_template("register.html", form = AddUserForm())

@app.route('/login')
def login():
    return render_template("login.html", form = SignInForm()) if is_user_logged() == False else redirect(url_for("profils"))

@app.route('/logout')
def logout():
    session['user'] = None
    return redirect(url_for("index"))

@app.route('/admin/agencies')
def admin_agencies():
    return render_template("templates/agencies.html", agencies = Agency.query.all()) if is_user_logged() and is_user_admin() else redirect(url_for("login"))

@app.route('/admin/countries')
def admin_countries():
    return render_template("templates/countries.html", countries = Country.query.all(), agencies = Agency.query.all()) if is_user_logged() and is_user_admin() else redirect(url_for("login"))

@app.route('/admin/trips')
def admin_trips():
    return render_template("templates/trips.html", trips = Trip.query.all(), agencies = Agency.query.all(), countries = Country.query.all()) if is_user_logged() and is_user_admin() else redirect(url_for("login"))

@app.route('/admin/statistics')
def statistics():
    return render_template("templates/statistics.html", trips = Trip.query.all(), reservations = Reservation.query.all()) if is_user_logged() and is_user_admin() else redirect(url_for("login"))

# Aģentūru un ceļojumu pievienošana
@app.route('/admin/add')
def admin_add():
    return redirect(url_for("admin_add_agencies")) if is_user_logged() and is_user_admin() else redirect(url_for("login"))

@app.route('/admin/add/agencies', methods=['GET', 'POST'])
def admin_add_agencies():
    if is_user_logged() and is_user_admin():
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
    else:
        redirect(url_for("login"))

@app.route('/admin/add/country', methods=['GET', 'POST'])
def admin_add_country():
    if is_user_logged() and is_user_admin():
        form = AddCountryForm()
        if form.validate_on_submit():
            country = Country(country=form.country.data, abbreviation=form.abbreviation.data)
            db.session.add(country)
            db.session.commit()
            return redirect(url_for('admin_countries'))
        return render_template("templates/add_country.html", form=form)
    else:
        redirect(url_for("login"))

@app.route('/admin/add/trips', methods=['GET', 'POST'])
def admin_add_trips():
    if is_user_logged() and is_user_admin():
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
            print(form.date_from.data)

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
    else:
        redirect(url_for("login"))


# Aģentūru un ceļojumu dzēšana
@app.route('/admin/remove/agency/<int:id>')
def admin_remove_agency(id):
    if is_user_logged() and is_user_admin():
        remove_agency = Agency.query.filter_by(id=id).first()
        db.session.delete(remove_agency)
        db.session.commit()
        return redirect(url_for('admin_agencies'))
    else:
        redirect(url_for("login"))

@app.route('/admin/remove/country/<int:id>')
def admin_remove_country(id):
    if is_user_logged() and is_user_admin():
        remove_country = Country.query.filter_by(id=id).first()
        db.session.delete(remove_country)
        db.session.commit()
        return redirect(url_for('admin_countries'))
    else:
        redirect(url_for("login"))

@app.route('/admin/remove/trip/<int:id>')
def admin_remove_trip(id):
    if is_user_logged() and is_user_admin():
        remove_trip = Trip.query.filter_by(id=id).first()
        db.session.delete(remove_trip)
        db.session.commit()
        return redirect(url_for('admin_trips'))
    else:
        redirect(url_for("login"))

# Aģentūru, valstu un ceļojumu rediģēšana
@app.route('/admin/edit/trip/<int:id>', methods=['GET', 'POST'])
def admin_edit_trip(id):
    if is_user_logged() and is_user_admin():
        edit_trip = Trip.query.filter_by(id=id).first()
        agencies = SelectField('Aģentūra', choices=Agency.query.all(), validators=[DataRequired()], default=Agency.query.filter_by(id=edit_trip.agency_id).first())
        country_from = SelectField('Izceļošanas valsts', choices=Country.query.all(), validators=[DataRequired()], default = Country.query.filter_by(id=edit_trip.country_from).first())
        country_to = SelectField('Galamērķa valsts', choices=Country.query.all(), validators=[DataRequired()], default=Country.query.filter_by(id=edit_trip.country_to).first())

        setattr(AddTripForm, 'agency', agencies)
        setattr(AddTripForm, 'country_from', country_from)
        setattr(AddTripForm, 'country_to', country_to)
        
        form = AddTripForm()
        if form.validate_on_submit():
            country_from = Country.query.filter_by(country=form.country_from.data.split(",")[0]).first().id
            country_to = Country.query.filter_by(country=form.country_to.data.split(",")[0]).first().id
            edit_trip.agency_id=Agency.query.filter_by(name=form.agency.data).first().id
            edit_trip.country_from=country_from
            edit_trip.country_to=country_to
            edit_trip.date_from=form.date_from.data
            edit_trip.date_to=form.date_to.data
            edit_trip.description=form.description.data
            edit_trip.cost=form.cost.data
            edit_trip.ticket_amount=form.ticket_amount.data
            db.session.commit()
            return redirect(url_for('admin_trips'))
        return render_template("templates/edit_trip.html", id=id, form=form, trip=edit_trip)
    else:
        redirect(url_for("login"))

@app.route('/admin/edit/country/<int:id>', methods=['GET', 'POST'])
def admin_edit_country(id):
    if is_user_logged() and is_user_admin():
        country = Country.query.filter_by(id=id).first()
        form = AddCountryForm()
        if form.validate_on_submit():
            country.country = form.country.data
            country.abbreviation = form.abbreviation.data
            db.session.commit()
            return redirect(url_for('admin_countries'))
        return render_template("templates/edit_country.html", form=form, id=id, country=country)
    else:
        redirect(url_for("login"))
    
@app.route('/admin/edit/agency/<int:id>', methods=['GET', 'POST'])
def admin_edit_agency(id):
    if is_user_logged() and is_user_admin():
        agency = Agency.query.filter_by(id = id).first()
        form = AddAgencyForm()
        if form.validate_on_submit():
            agency.name = form.name.data
            agency.address = form.address.data
            agency.number = form.phone_number.data
            db.session.commit()
            return redirect(url_for('admin'))
        return render_template("templates/edit_agency.html", form=form, id=id, agency=agency)
    else:
        redirect(url_for("login"))

@app.route('/sign_up', methods=['POST'])
def sign_up():
    if request.method == "POST":
        user = User(
            email = request.form['email'],
            password = generate_password_hash(request.form['password'], method='sha256'),
            name = request.form['name'],
            surname = request.form['surname'],
            role_id = 0 )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('profils'))
    return "404"

@app.route('/sign_in', methods=['POST'])
def sign_in():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form['email']).first()
        if not user or not check_password_hash(user.password, request.form['password']):
            flash("Nav tāds lietotājs")
            return redirect(url_for('login'))
        else:
            session['user'] = user.id
            return redirect(url_for('profils'))

    return "404"
    # return render_template("templates/register.html") # To Do

#rezervācijas sistēma
@app.route('/reservation/<int:id>')
def reservation(id):
    if is_user_logged():
        trip = Trip.query.get(id)
        trip.views += 1
        db.session.commit()
        return render_template("reservation.html", trip = trip, countries = Country.query.all(), user = get_user_data(session['user']))
    flash("Lūdzu pieslēdzaties!")
    return redirect(url_for('login'))

@app.route('/reservation/add/<int:id>')
def reservation_add(id):
    if is_user_logged():
        user = get_user_data(session['user'])
        trip = Trip.query.filter_by(id=id).first()
        trip = trip.serialize()
        country_from = Country.query.filter(Country.id==trip['country_from_id']).first()
        country_to = Country.query.filter(Country.id==trip['country_to_id']).first()
        trip['country_from'] = country_from.country
        trip['country_to'] = country_to.country
        reservation = Reservation(
            owner_name=user.name,
            owner_surname=user.surname,
            country_from=trip['country_from']+f"({country_from.abbreviation})",
            country_to=trip['country_to']+f"({country_to.abbreviation})",
            date_from=trip['date_from'],
            date_to=trip['date_to'],
            days=(trip['date_to']-trip['date_from']).days,
            price=trip['cost'],
            reservation_number=1000000001+Reservation.query.order_by(-Reservation.id).first().id if len(Reservation.query.all()) > 0 else 1000000001,
            trip_id=id,
            owner_id=user.id
        )
        db.session.add(reservation)
        db.session.commit()
        flash("Veiksmīgi rezervēts ceļojums!")
        return redirect(url_for('profils'))
    flash("Lūdzu pieslēdzaties!")
    return redirect(url_for('login'))

# Aģentūru un ceļojumu dzēšana
@app.route('/reservation/remove/<int:id>')
def reservation_remove(id):
    remove_reservation = Reservation.query.filter_by(id=id).first()
    db.session.delete(remove_reservation)
    db.session.commit()
    return redirect(url_for('profils'))

@app.route('/catalogue_filter', methods=["POST"])
def catalogue_filter():
    Trips = Trip.query.all()
    validations = {
        "country_from_id": None if not request.form['from'] else int(request.form['from']),
        "country_to_id": None if not request.form['to'] else int(request.form['to']),
        "date_from": None if not request.form['from_date'] else datetime.strptime(request.form['from_date'], '%Y-%m-%d').date(),
        "date_to": None if not request.form['to_date'] else datetime.strptime(request.form['to_date'], '%Y-%m-%d').date()
    }
    output = []
    requirements = len(validations)
    valids_passed = 0
    for trip in Trips:
        trip = trip.serialize()
        for validation in validations:
            if validations[validation] == None:
                requirements -= 1
                continue
            else:
                if (validation == "date_from" and trip[validation] >= validations[validation] or
                    validation == "date_to" and trip[validation] <= validations[validation] or
                    trip[validation] == validations[validation]
                ):
                    valids_passed += 1 
        
        if valids_passed == requirements:
            trip['country_from'] = Country.query.filter(Country.id==trip['country_from_id']).first().country
            trip['country_to'] = Country.query.filter(Country.id==trip['country_to_id']).first().country
            output.append(trip)

        requirements = len(validations)
        valids_passed = 0
    return Response(json.dumps(output, default=str), mimetype='application/json')



@app.route("/upload/<trip_id>/<owner_id>")
def upload_reservation(trip_id, owner_id):
    reservation = Reservation.query.filter_by(id=trip_id).first()
    if not reservation or reservation.owner_id != int(owner_id) or int(owner_id) != session['user']:
        return redirect(url_for("profils"))
    else:
        html_content = f'''
            <table>
                <tr>
                    <th>{reservation.owner_name + " " + reservation.owner_surname}</th>
                    <th>Rez. Nr. {reservation.reservation_number}</th>
                </tr>
                <tr>
                    <th>Maršruts</th>
                    <th>{reservation.country_from + " - " + reservation.country_to}</th>
                </tr>
                <tr>
                    <th>Izbraukšana</th>
                    <th>{reservation.date_from.strftime("%Y-%m-%d %H:%M")}</th>
                </tr>
                <tr>
                    <th>Atgriešanās</th>
                    <th>{reservation.date_to.strftime("%Y-%m-%d %H:%M")}</th>
                </tr>
                <tr>
                    <th>Dienu skaits</th>
                    <th>{reservation.days}</th>
                </tr>
                <tr>
                    <th>Cena</th>
                    <th>{reservation.price} euro</th>
                </tr>
            </table>
        
        '''
        html_text = '''
            <!DOCTYPE html>
            <html lang="lv">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Document</title>
                    <style>
                        table, th{
                            text-align: left;
                            border: 1px solid black;
                            border-collapse: collapse;
                        }
                        th{
                            width: 300px;
                        }
                    </style>
                </head>
                <body>
                    ''' + html_content + '''
                </body>
            </html>
        '''
        path = os.getcwd()
        file = open(path+f"\\media\\reserved_trip.html", "w",  encoding="utf-8")
        file.write(html_text)
        file.close()
        return send_file(path+f"\\media\\reserved_trip.html", as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)