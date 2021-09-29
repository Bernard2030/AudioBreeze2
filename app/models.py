from . import db


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