# imports 
import jwt 
from flask import Flask,jsonify,request,make_response
from flask.helpers import make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
from functools import wraps


# initializing the application

app=Flask(__name__)

app.config['SECRET_KEY']= 'A23bxsa7188sjksdc8u2cxcse23'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://moringa:Access@localhost/audiobreeze2'

# calling the db
db= SQLAlchemy(app)

# tables for user and audio

class User(db.Model):
  id=db.Column(db.Integer, primary_key=True)
  public_id=db.Column(db.String(250), unique=True)
  password = db.Column(db.String(250))
  name=db.Column(db.String(200))
  admin=db.Column(db.Boolean)

class Audio(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    songName=db.Column(db.String(100), unique=True)
    artistName=db.Column(db.String(50))
    songDuration=db.Column(db.Integer)
    songType=db.Column(db.String(50))
    songDescription=db.Column(db.String(100))
    songQuality=db.Column(db.String(100))