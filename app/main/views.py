

from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash
from . import main
from .. import db
from ..models import User, Audio

# creating routes for all users
@main.route('/user', methods=['GET'])
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
@main.route('/user/<public_id>', methods=['GET'])
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

# Create user here
@main.route('/user', methods=['POST'])
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
@main.route('/user/<public_id>', methods=['PUT'])
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
@main.route('/user/<public_id>', methods=['DELETE'])  
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

    
    #================JOE END =========#

    ##======Bernard=========##
    ##======Routes=========##

    #get all audio approute

@main.route('/audio', methods=['GET'])
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

@main.route('/audio/', methods=['POST'])
def create_audio():
    data=request.get_json()    
    new_audio=Audio(songName=data['songName'], artistName=data['artistName'],songDuration=data['songDuration'], songType=data['songType'], songDescription=data['songDescription'], songQuality=data['songQuality'])
    db.session.add(new_audio)
    db.session.commit()
    return jsonify({"message" : "New audio song  created successfully!"})  

#get individual songs

@main.route('/audio/<songName>', methods=['GET'])
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

@main.route('/audio/<songName>', methods=['PUT'])
def promote_song(songName):
    audio=Audio.query.filter_by(songName=songName).first()

    if not audio:
        return jsonify({'message' :'No song found'})
    audio.admin=True
    db.session.commit()   
    return jsonify({'message': 'The song has been promoted to be the most trending song '}) 

#delete the song audio

@main.route('/audio/<songName>', methods=['DELETE'])  
def delete_song(songName):
    audio=Audio.query.filter_by(songName=songName).first()

    if not audio:
        return jsonify({'message' :'No song  found'})
    db.session.delete(audio)
    db.session.commit()
    return jsonify({'message': 'The song has been deleted successfully'})  
