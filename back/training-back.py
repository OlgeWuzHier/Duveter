import json
from dotenv import load_dotenv
from flask import Flask, request
from flask_pymongo import PyMongo
from flask_restful import Resource, Api
from flask_cors import CORS
import os
from bson import json_util
from bson.objectid import ObjectId
from flask_jwt_extended import JWTManager

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("CONNECTION_STRING")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False  # TODO Change later
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["SECRET_KEY"] = os.getenv("SOCKET_SECRET_KEY")
jwt = JWTManager(app)
mongo = PyMongo(app)
api = Api(app)
CORS(app)

class TrainingGame(Resource):
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

    def __add_money_if_applicable(self, game, user, time_before):
        for coin_field in game['coinFields']:
            if user['timeLeft'] <= coin_field < time_before:
                user['coins'] += sum(p['income_value'] for p in user['patches'])

    def get(self):
        if not request.args.get("id"):
            return 'Bad request 8', 400

        game = mongo.db.trainingGames.find_one({ "_id": ObjectId(request.args.get('id')) })
        return { "game": json.loads(json_util.dumps(game)) }

    def post(self):
        with open("patches.json", 'r') as j:
            game = mongo.db.trainingGames.insert_one({
                "patchesList": json.loads(j.read()),
                "coinFields": [0, 6, 12, 18, 24, 30, 36, 42, 48],
                "bonusPatchFields": [3, 9, 15, 21, 27], 
                "player": {
                    "patches": [],
                    "coins": 5,
                    "timeLeft": 53,
                }
            })
        return { "trainingGameId": json_util.dumps(game.inserted_id) }

    def put(self):
        if not request.args.get("id"):
            return 'Bad request 1', 400

        game = mongo.db.trainingGames.find_one({ "_id": ObjectId(request.args.get('id')) })
        user = game['player']

        if game is None:
            return 'Bad request 2', 400
        
        # Check if user has time left, allow if special patch is available
        if user['timeLeft'] <= 0 and 'special' not in game['patchesList'][0]['name']:
            return 'Bad request 3', 400
        
        patch = request.json.get('patch')
        time_balance = request.json.get('timeBalance')

        if patch:
            original_patch = next((p for p in game['patchesList'] if p['name'] == patch['name']), None)
            if original_patch is None: 
                return 'Bad request 4', 400

            original_patch['flip'] = patch['flip']
            original_patch['position'] = patch['position']
            original_patch['rotate'] = patch['rotate']

            # Remove used patch from game.patchesList and add to players[].patches
            patch_index = game['patchesList'].index(
                next((p for p in game['patchesList'] if p['name'] == patch['name']), None)
            )

            # Allow to choose only special if it is available
            if patch_index > 0 and 'special' in game['patchesList'][0]['name']:
                return 'Bad request 5', 400
            
            # Add patch to user patches, remove from available
            game['patchesList'].pop(patch_index)
            user['patches'].append(original_patch)
            
            # Pay for patch
            time_before = user['timeLeft']
            user['timeLeft'] -= original_patch['price_time']
            user['coins'] -= original_patch['price_coins']

            if user['coins'] < 0:
                return 'Bad request 6', 400

            self.__add_money_if_applicable(game, user, time_before)
            self.__add_bonus_patch_if_applicable(game, user, time_before)
            mongo.db.trainingGames.replace_one({ "_id": game["_id"] }, game)
            return { "game": json.loads(json_util.dumps(game)) }

        elif time_balance:
            time_before = user['timeLeft']
            user['timeLeft'] -= time_balance
            user['coins'] += time_balance

            self.__add_money_if_applicable(game, user, time_before)
            self.__add_bonus_patch_if_applicable(game, user, time_before)
            mongo.db.trainingGames.replace_one({ "_id": game["_id"] }, game)
            return { "game": json.loads(json_util.dumps(game)) }
        

        return 'Bad request 7', 400

    def delete(self):
        mongo.db.trainingGames.delete_one({'_id': ObjectId(request.args.get('id'))})
        return 'OK', 200

api.add_resource(TrainingGame, '/training-game')

if __name__ == '__main__':
    app.run(host='0.0.0.0')