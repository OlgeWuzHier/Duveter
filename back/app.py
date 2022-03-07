import re
from dotenv import load_dotenv
from flask import Flask, request
from flask_jwt_extended.utils import get_jwt_identity
from flask_pymongo import PyMongo 
# from PyMongo import MongoClient
from flask_restful import Resource, Api
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
import os
from bson import json_util
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import bcrypt


load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("CONNECTION_STRING")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["SECRET_KEY"] = os.getenv("SOCKET_SECRET_KEY")
jwt = JWTManager(app)
mongo = PyMongo(app)
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

class Helloworld(Resource):
    def get(self):
        x = mongo.db.users.find_one({"username": "user"})
        return json_util.dumps(x)

class Login(Resource):
    def post(self):
        username = request.json.get("username")
        password = request.json.get("password")

        retrieved_user = mongo.db.users.find_one({"username": username})
        if not retrieved_user or not bcrypt.checkpw(password.encode("utf-8"), retrieved_user["password"]):
            return "Incorrect username or password", 401

        return {"access_token": create_access_token(identity=username)}


class Protected(Resource):
    @jwt_required()
    def get(self):
        # return json_util.dumps(get_jwt_identity())
        return {}
        

class Register(Resource):
    def post(self):
        username = request.json.get("username")
        password = request.json.get("password")
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        if mongo.db.users.find_one({"username": username}):
            return "User already exists", 403

        if not re.search("..*", password):
            return "Password too short", 403

        mongo.db.users.insert_one({"username": username, "password": hashed})
        
        return {"access_token": create_access_token(identity=username)}

class Room(Resource):
    def get(self):
        return { 'roomId': None }

api.add_resource(Helloworld, '/')
api.add_resource(Login, '/login')
api.add_resource(Protected, '/protected')
api.add_resource(Register, '/register')
api.add_resource(Room, '/room')

@socketio.on('connect')
def connect():
    emit('response', {"data": "connected"})

if __name__ == '__main__':
    socketio.run(app)