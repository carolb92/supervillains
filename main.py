from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask("app")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///villain.db"
#connects the SQLAlchemy library to the app / lets your database access the functionality of SQLAlchemy
db = SQLAlchemy(app)

class Villain(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  description = db.Column(db.String(250), nullable=False)
  interests = db.Column(db.String(250), nullable=False)
  url = db.Column(db.String(250), nullable=False)
  date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  def __repr__(self):
    return "<Villain "+ self.name + ">"

db.create_all()
db.session.commit()

@app.route("/")
def villains_cards():
  return render_template("villain.html", villains=Villain.query.all())

@app.route("/add", methods=["GET"])
def add_villain():
  return render_template("addvillain.html", errors=[])

#This route will be called when the user finishes the add villain form
@app.route("/addVillain", methods=["POST"])
def add_user():
  #alerts users if they don’t submit all the required fields for a villain
  errors = []
  name = request.form.get("name")
  if not name:
    errors.append("Oops! Looks like you forgot a name!")
    
  description = request.form.get("description")
  if not description:
    errors.append("Oops! Looks like you forgot a description!")
    
  interests = request.form.get("interests")
  if not interests:
    errors.append("Oops! Looks like you forgot some interests!")
    
  url = request.form.get("url")
  if not url:
    errors.append("Oops! Looks like you forgot an image!")

  #query the villain database to check and see if the villain the user is trying to add is already in the database
  villain = Villain.query.filter_by(name=name).first()
  if villain:
    errors.append("Oops! A villain with that name already exists!")
  if errors:
    render_template("addvillain.html", errors=errors)
  else:
    new_villain = Villain(name=name,description=description, interests=interests, url=url)
    db.session.add(new_villain)
    db.session.commit()
    return render_template("villain.html", villains=Villain.query.all())

@app.route("/delete", methods=["GET"])
def delete_villain():
  return render_template("deletevillain.html", errors=[])

@app.route("/deleteVillain", methods=["POST"])
def delete_user():
  name = request.form.get("name")
  villain = Villain.query.filter_by(name=name).first()
  if villain:
    db.session.delete(villain)
    db.session.commit()
    return render_template("villain.html", villains=Villain.query.all())
  else:
    return render_template("deletevillain.html", errors=["Oops! That villain doesn't exist!"])
  

app.run(host='0.0.0.0', port=8080)