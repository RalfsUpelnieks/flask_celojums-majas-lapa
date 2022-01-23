from flask import render_template, redirect
from flask.helpers import url_for
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired
from settings import app
from forms import AddAgencyForm, AddTripForm
from models import db, Agency, Trip

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ceļojumi')
def celojumi():
    return render_template("celojumi.html", trips = Trip.query.all())

@app.route('/admin')
def admin():
    return redirect(url_for("admin_agencies"))

@app.route('/profils')
def profils():
    return render_template("profile.html")

@app.route('/admin/agencies')
def admin_agencies():
    return render_template("templates/agencies.html", agencies = Agency.query.all())

@app.route('/admin/trips')
def admin_trips():
    return render_template("templates/trips.html", trips = Trip.query.all(), agencies = Agency.query.all())

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

@app.route('/admin/add/trips', methods=['GET', 'POST'])
def admin_add_trips():
    # Lai dinamiski atjauninātu aģentūru sarakstu ceļojumu izveides lapā
    # Aģentūru izvēlnes attribūts tiek pievienots klases struktūrai, ne instancei
    agencies = SelectField('Aģentūra', choices=Agency.query.all(), validators=[DataRequired()])
    setattr(AddTripForm, 'agency', agencies)
    
    # Pēc tā var izveidot 'form' objektu ar atjauninātu aģentūru sarakstu
    form = AddTripForm()
    if form.validate_on_submit():
        # Pārbaude
        agency = Agency.query.filter_by(name=form.agency.data).first().id
        trip = Trip(
            agency_id=agency,
            country_from=form.country_from.data,
            country_to=form.country_to.data,
            date_from=form.date_from.data,
            date_to=form.date_to.data,
            description=form.description.data,
            cost=form.cost.data,
            ticket_amount=form.ticket_amount.data,
            views=0 )
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

@app.route('/admin/remove/trip/<int:id>')
def admin_remove_trip(id):
    remove_trip = Trip.query.filter_by(id=id).first()
    db.session.delete(remove_trip)
    db.session.commit()
    return redirect(url_for('admin_trips'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
