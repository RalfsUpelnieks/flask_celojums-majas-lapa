from flask import render_template, redirect
from flask.helpers import url_for
from controllers import get_agencies, get_trips
from settings import app

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ceļojumi')
def celojumi():
    return render_template("celojumi.html")

@app.route('/admin')
def admin():
    return redirect(url_for("admin_agencies"))

@app.route('/profils')
def profils():
    return render_template("profile.html")

@app.route('/admin/agencies')
def admin_agencies():
    return render_template("templates/agencies.html", agencies = get_agencies())

@app.route('/admin/trips')
def admin_trips():
    return render_template("templates/trips.html", trips = get_trips())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
