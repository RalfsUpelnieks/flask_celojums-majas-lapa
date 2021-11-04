from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask.helpers import url_for
from datetime import datetime

app = Flask('app')

# Database Connection
db_name = 'test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  completed = db.Column(db.Integer, default=0)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return '<Task %r>' % self.id

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

@app.route('/admin/countries')
def admin_countries():
  return render_template("templates/countries.html", num = [1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,0])

@app.route('/admin/agencies')
def admin_agencies():
  return render_template("templates/agencies.html", num = [1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,0])

@app.route('/admin/trips')
def admin_trips():
  return render_template("templates/trips.html", num = [1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,0])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
