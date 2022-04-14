import datetime
import json
import re
from dotenv import load_dotenv
from flask import Flask, make_response, request
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
import logging
from duveterAI import DuveterAI

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

# Tell that response cannot be cached unless endpoint explicitly says so
@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or { 'Cache-Control': 'no-store'})
    return resp

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
        gameVsAI = request.json.get('vsAI') or False
        
        if mongo.db.queue.find_one({ 'username': username }):
            return "User already in queue", 403
        
        if not gameVsAI:
            mongo.db.queue.insert_one({ 'username': username })

        if mongo.db.queue.count_documents({}) > 1 or gameVsAI:
            if not gameVsAI:
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
                            "username": username,
                            "patches": [],
                            "coins": 5,
                            "timeLeft": 53,
                        },
                        { 
                            "username": player2["username"] if not gameVsAI else DuveterAI.USERNAME,
                            "patches": [],
                            "coins": 5,
                            "timeLeft": 53,
                        },
                    ],
                    "forcePlayer": username,
                    "vsAI": gameVsAI, 
                    "aiType": random.randint(0, 4) if gameVsAI else None
                })
            
            socketio.emit(f'lobby-{username}', json_util.dumps(game.inserted_id))
            if not gameVsAI:
                socketio.emit(f'lobby-{player2["username"]}', json_util.dumps(game.inserted_id))

        return 'OK', 200

    @jwt_required()
    def delete(self):
        username = get_jwt_identity()
        mongo.db.queue.find_one_and_delete({ 'username': username})
        return 'OK', 200

class Game(Resource):
    def __get_active_player(self, game):
        if game['forcePlayer'] is not None:
            return game['forcePlayer']
        if game['players'][0]['timeLeft'] > game['players'][1]['timeLeft']:
            return game['players'][0]['username']
        return game['players'][1]['username']

    def __add_bonus_patch_if_applicable(self, game, user, time_before):
        if len(game['bonusPatchFields']):
            if user['timeLeft'] <= game['bonusPatchFields'][-1] < time_before:
                game['bonusPatchFields'].pop()
                game['patchesList'].insert(0, {
                    "name": f"special{len(game['bonusPatchFields'])}",
                    "arrangement_table": [[1]],
                    "price_coins": 0, # TODO: Unify casing
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

    def __end_game_if_applicable(self, game):
        if game['players'][0]['timeLeft'] <= 0 and game['players'][1]['timeLeft'] <= 0:
            mongo.db.gameResults.insert_one({
                'players': [
                    {
                    'username': game['players'][0]['username'],
                    'score': -162 + 2 * sum([i for sub in [i for sub in map(lambda x: x['arrangement_table'], game['players'][0]['patches']) for i in sub] for i in sub]) + game['players'][0]['coins']
                    }, 
                    {
                    'username': game['players'][1]['username'],
                    'score': -162 + 2 * sum([i for sub in [i for sub in map(lambda x: x['arrangement_table'], game['players'][1]['patches']) for i in sub] for i in sub]) + game['players'][1]['coins']
                    }
                ],
                'date': datetime.datetime.now()
            })

            mongo.db.games.delete_one({'_id': game['_id']})

    def __save_game_and_emit(self, game):
        if mongo.db.games.find_one({ "_id": game["_id"] }):
            mongo.db.games.replace_one({ "_id": game["_id"] }, game)
            socketio.emit(str(game["_id"]), json.loads(json_util.dumps(game)))

    def __trigger_ai_move_if_applicable(self, game):
        if game["vsAI"]:
            ai_player = next((u for u in game['players'] if u['username'] == DuveterAI.USERNAME), None)

            while self.__get_active_player(game) == DuveterAI.USERNAME:
                if ai_player['timeLeft'] <= 0:
                    break
                game['forcePlayer'] = None
                time_before = ai_player['timeLeft']
                DuveterAI.make_move(game)
                self.__add_money_if_applicable(game, ai_player, time_before)
                self.__add_bonus_patch_if_applicable(game, ai_player, time_before)
                self.__set_force_player_if_applicable(game, ai_player)
                self.__end_game_if_applicable(game)
            
            self.__save_game_and_emit(game)

    @jwt_required()
    def get(self):
        if not request.args.get("id"):
            username = get_jwt_identity()
            games = mongo.db.games.find({ "players.username": username })
            return { "games": json.loads(json_util.dumps(games)) }
        game = mongo.db.games.find_one({ "_id": ObjectId(request.args.get('id')) })
        return { "game": json.loads(json_util.dumps(game)) }

    @jwt_required()
    def put(self):
        if not request.args.get("id"):
            return 'Bad request', 400

        username = get_jwt_identity()
        game = mongo.db.games.find_one({ "_id": ObjectId(request.args.get('id')) })

        if game is None:
            return 'Bad request', 400

        user = next((u for u in game['players'] if u['username'] == username), None)
        if user is None:
            return 'Bad request', 400
        
        # Check if user has time left, allow if special patch is available
        if user['timeLeft'] <= 0 and 'special' not in game['patchesList'][0]['name']:
            return 'Bad request', 400

        if self.__get_active_player(game) != username:
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
            self.__save_game_and_emit(game)
            self.__trigger_ai_move_if_applicable(game)
            self.__end_game_if_applicable(game)
            return 'OK', 200

        elif time_balance:
            # Force player to pick bonus patch if available
            if 'special' in game['patchesList'][0]['name']:
                return 'Bad request', 400

            time_before = user['timeLeft']
            user['timeLeft'] -= time_balance
            user['coins'] += time_balance

            self.__add_money_if_applicable(game, user, time_before)
            self.__add_bonus_patch_if_applicable(game, user, time_before)
            self.__set_force_player_if_applicable(game, user)
            self.__save_game_and_emit(game)
            self.__trigger_ai_move_if_applicable(game)
            self.__end_game_if_applicable(game)
            return 'OK', 200
        
        return 'Bad request', 400

class Leaderboards(Resource):
    @jwt_required()
    def get(self):
        results = json.loads(json_util.dumps(mongo.db.gameResults.find()))
        scores = []
        for game in results:
            for player in game['players']:
                scores.append({
                    'username': player['username'],
                    'score': player['score'],
                    'date': game['date']
                    })
        scores.sort(reverse=True, key=lambda x: x['score'])
        return scores[:10]

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Queue, '/queue')
api.add_resource(Game, '/game')
api.add_resource(Leaderboards, '/leaderboards')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
