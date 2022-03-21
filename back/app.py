import json
import re
from dotenv import load_dotenv
from flask import Flask, request
from flask_jwt_extended.utils import get_jwt_identity
from flask_pymongo import PyMongo
from flask_restful import Resource, Api
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
import os
from bson import json_util
from bson.objectid import ObjectId
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import bcrypt
import random

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("CONNECTION_STRING")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False  # TODO Change later
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["SECRET_KEY"] = os.getenv("SOCKET_SECRET_KEY")
jwt = JWTManager(app)
mongo = PyMongo(app)
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)


class Login(Resource):
    def post(self):
        username = request.json.get("username")
        password = request.json.get("password")

        retrieved_user = mongo.db.users.find_one({"username": username})
        if not retrieved_user or not bcrypt.checkpw(password.encode("utf-8"), retrieved_user["password"]):
            return "Incorrect username or password", 401

        return {"access_token": create_access_token(identity=username)}


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


class Queue(Resource):
    @jwt_required()
    def post(self):
        username = get_jwt_identity()
        # TODO: Check if user is already in queue
        mongo.db.queue.insert_one({ 'username': username })

        if mongo.db.queue.count_documents({}) > 1:
            player1 = mongo.db.queue.find_one_and_delete({ 'username': username })
            player2 = mongo.db.queue.find_one_and_delete({})
            
            with open("patches.json", 'r') as j:
                patches = json.loads(j.read())
                random.shuffle(patches)
                starter_index = patches.index(next(p for p in patches if p['name'] == "starter"))
                patches.append(patches.pop(starter_index))
                game = mongo.db.games.insert_one({
                    "patchesList": patches,
                    "coinFields": [0, 6, 12, 18, 24, 30, 36, 42, 48],
                    "bonusPatchFields": [3, 9, 15, 21, 27], 
                    "players": [
                        {
                            "username": player1["username"],
                            "score": 0,
                            "patches": [],
                            "coins": 5,
                            "timeLeft": 53,
                        },
                        { 
                            "username": player2["username"],
                            "score": 0,
                            "patches": [],
                            "coins": 5,
                            "timeLeft": 53,
                        },
                    ],
                    "forcePlayer": player1["username"],
                })
            
            socketio.emit(f'lobby-{player1["username"]}', json_util.dumps(game.inserted_id))
            socketio.emit(f'lobby-{player2["username"]}', json_util.dumps(game.inserted_id))

        return 'OK', 200

class Game(Resource):
    def __add_bonus_patch_if_applicable(self, game, user, time_before):
        if len(game['bonusPatchFields']):
            if user['timeLeft'] <= game['bonusPatchFields'][-1] < time_before:
                game['bonusPatchFields'].pop()
                game['patchesList'].insert(0, {
                    "name": f"special{len(game['bonusPatchFields'])}",
                    "arrangement_table": [[1]],
                    "price_coins": 0,
                    "price_time": 0,
                    "income_value": 0
                })
                game['forcePlayer'] = user['username']

    def __add_money_if_applicable(self, game, user, time_before):
        for coin_field in game['coinFields']:
            if user['timeLeft'] <= coin_field < time_before:
                user['coins'] += sum(p['income_value'] for p in user['patches'])

    def __set_force_player_if_applicable(self, game, user):
        # If both players have the same time left, current makes move again
        if game['players'][0]['timeLeft'] == game['players'][1]['timeLeft']:
            game['forcePlayer'] = user['username']

    @jwt_required()
    def get(self):
        if not request.args.get("id"):
            return 'Bad request', 400
        game = mongo.db.games.find_one({ "_id": ObjectId(request.args.get('id')) })
        return { "game": json.loads(json_util.dumps(game)) }

    @jwt_required()
    def put(self):
        if not request.args.get("id"):
            return 'Bad request', 400

        username = get_jwt_identity()
        game = mongo.db.games.find_one({ "_id": ObjectId(request.args.get('id')) })
        user = next((u for u in game['players'] if u['username'] == username), None)
        if user is None:
            return 'Bad request', 400
        
        # Check if it is this player move
        if game['forcePlayer'] is not None:
            if game['forcePlayer'] != user['username']:
                return 'Bad request', 400
        else:
            opponent = next((u for u in game['players'] if u['username'] != username), None)
            if user['timeLeft'] < opponent['timeLeft']:
                return 'Bad request', 400

        game['forcePlayer'] = None
        
        patch = request.json.get('patch')
        time_balance = request.json.get('timeBalance')

        if patch:
            original_patch = next((p for p in game['patchesList'] if p['name'] == patch['name']), None)
            if original_patch is None: 
                return 'Bad request', 400

            original_patch['flip'] = patch['flip']
            original_patch['position'] = patch['position']
            original_patch['rotate'] = patch['rotate']

            # TODO: Check collision

            # Remove used patch from game.patchesList and add to players[].patches
            patch_index = game['patchesList'].index(
                next((p for p in game['patchesList'] if p['name'] == patch['name']), None)
            )

            # Allow to choose only patches with 0, 1 or 2 index
            if patch_index > 2:
                return 'Bad request', 400

            # Allow to choose only special if it is available
            if patch_index > 0 and 'special' in game['patchesList'][0]['name']:
                return 'Bad request', 400
            
            # Add patch to user patches, remove from available
            game['patchesList'].pop(patch_index)
            user['patches'].append(original_patch)

            # Move patches (before taken one) to the end
            while patch_index:
                game['patchesList'].append(
                    game['patchesList'].pop(0)
                )
                patch_index -= 1
            
            # Pay for patch
            time_before = user['timeLeft']
            user['timeLeft'] -= original_patch['price_time']
            user['coins'] -= original_patch['price_coins']

            if user['coins'] < 0:
                return 'Bad request', 400

            self.__add_money_if_applicable(game, user, time_before)
            self.__add_bonus_patch_if_applicable(game, user, time_before)
            self.__set_force_player_if_applicable(game, user)

            mongo.db.games.replace_one({ "_id": ObjectId(request.args.get('id')) }, game)
            socketio.emit(request.args.get('id'), json.loads(json_util.dumps(game)))
            return 'OK', 200

        elif time_balance:
            time_before = user['timeLeft']
            user['timeLeft'] -= time_balance
            user['coins'] += time_balance

            self.__add_money_if_applicable(game, user, time_before)
            self.__add_bonus_patch_if_applicable(game, user, time_before)
            self.__set_force_player_if_applicable(game, user)

            mongo.db.games.replace_one({ "_id": ObjectId(request.args.get('id')) }, game)
            socketio.emit(request.args.get('id'), json.loads(json_util.dumps(game)))
            return 'OK', 200
        
        return 'Bad request', 400


api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Queue, '/queue')
api.add_resource(Game, '/game')


if __name__ == '__main__':
    socketio.run(app)
