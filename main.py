from flask import Flask, render_template
app = Flask('app')

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/ceļojumi')
def celojumi():
  return render_template("celojumi.html")

@app.route('/admin')
def admin():
  return render_template("admin.html")

@app.route('/profils')
def profils():
  return render_template("profile.html")

app.run(host='0.0.0.0', port=8080)