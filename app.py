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

# creating routes for all users
@app.route('/user', methods=['GET'])
# @token_required  
def get_all_users():
    # giving user authentification to update the content

    # if not current_user.admin:
    #     return jsonify({'message': "You cannot perform that action"})


    users = User.query.all()
    output = []
    for user in users:
        user_data ={}
        user_data['public_id']=user.public_id
        user_data['name']=user.name
        user_data['password']=user.password
        user_data['admin']=user.admin
        output.append(user_data)
    return jsonify({'users' : output})

# getting one user at a time
@app.route('/user/<public_id>', methods=['GET'])
# @token_required
def get_one_user(public_id):
    # giving user authentification to update the content

    # if not current_user.admin:
    #     return jsonify({'message': "You cannot perform that action"})

    user=User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' :'No user found with that name'})
    user_data={}
    user_data['public_id']=user.public_id
    user_data['name']=user.name
    user_data['password']=user.password
    user_data['admin']=user.admin    
    return jsonify({'user': user_data})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing for authentication'}), 401


        # if token is there 
        try:
            data =jwt(token, app.config['SECRET_KEY']) 
            current_user =User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return  f(current_user, *args , **kwargs)  
    return decorated         

# Create user here
@app.route('/user/', methods=['POST'])
# @token_required
def create_user():
    # giving user authentification to update the content

    # if not current_user.admin:
    #     return jsonify({'message': "You cannot perform that action"})
    data=request.get_json()
    hashed_password=generate_password_hash(data['password'], method='sha256')
    new_user=User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message" : "New user created successfully!"})

# put user 
@app.route('/user/<public_id>', methods=['PUT'])
# @token_required
def promote_user(public_id):
    # giving user authentification to update the content

    # if not current_user.admin:
    #     return jsonify({'message': "You cannot perform that action"})
    user=User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' :'No user found'})
    user.admin=True
    db.session.commit()   
    return jsonify({'message': 'The user has been promoted1 to Admin'})


    #delete method
@app.route('/user/<public_id>', methods=['DELETE'])  
# @token_required
def delete_user( public_id):
    # giving user authentification to update the content

    # if not current_user.admin:
    #     return jsonify({'message': "You cannot perform that action"})
    user=User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' :'No user found'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})  

# =============authentication goes here for the user===========================
@app.route('/login')
def login():
    auth=request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
    user=User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
    if check_password_hash(user.password, auth.password):
        token= jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=20)}, app.config['SECRET_KEY'])

        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
   
    #================JOE END =========#

    ##======Bernard=========##
    ##======Routes=========##

    #get all audio approute

@app.route('/audio', methods=['GET'])
def get_all_audios():
    audios = Audio.query.all()
    output = []
    for audio in audios:
        audio_data ={}
        audio_data['songName']=audio.songName
        audio_data['artistName']=audio.artistName
        audio_data['songDuration']=audio.songDuration
        audio_data['songType']=audio.songType
        audio_data['songDescription']=audio.songDescription
        audio_data['songQuality']=audio.songQuality
        output.append(audio_data)
    return jsonify({'audios' : output})

#3create individual soings in the database

@app.route('/audio/', methods=['POST'])
def create_audio():
    data=request.get_json()    
    new_audio=Audio(songName=data['songName'], artistName=data['artistName'],songDuration=data['songDuration'], songType=data['songType'], songDescription=data['songDescription'], songQuality=data['songQuality'])
    db.session.add(new_audio)
    db.session.commit()
    return jsonify({"message" : "New audio song  created successfully!"})  

#get individual songs

@app.route('/audio/<songName>', methods=['GET'])
def get_one_audio(songName):

    audio=Audio.query.filter_by(songName=songName).first()

    if not audio:
        return jsonify({'message' :'No song found with that name'})
    audio_data={}
    audio_data['songName']=audio.songName
    audio_data['artistName']=audio.artistName
    audio_data['songDuration']=audio.songDuration
    audio_data['songType']=audio.songType    
    audio_data['songDescription']=audio.songDescription    
    audio_data['songQuality']=audio.songQuality    
    return jsonify({'audio': audio_data}) 

    ## put a song here

@app.route('/audio/<songName>', methods=['PUT'])
def promote_song(songName):
    audio=Audio.query.filter_by(songName=songName).first()

    if not audio:
        return jsonify({'message' :'No song found'})
    audio.admin=True
    db.session.commit()   
    return jsonify({'message': 'The song has been promoted to be the most trending song '}) 

#delete the song audio

@app.route('/audio/<songName>', methods=['DELETE'])  
def delete_song(songName):
    audio=Audio.query.filter_by(songName=songName).first()

    if not audio:
        return jsonify({'message' :'No song  found'})
    db.session.delete(audio)
    db.session.commit()
    return jsonify({'message': 'The song has been deleted successfully'})  

#run the application
if __name__ == '__main__':
    app.run()           