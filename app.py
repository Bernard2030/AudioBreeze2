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