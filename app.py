from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo 
# from PyMongo import MongoClient
import os
from bson import json_util

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("CONNECTION_STRING")
mongo = PyMongo(app)

@app.route("/")
def helloworld():
    x = mongo.db.test.find_one({"t1": "123"})
    return json_util.dumps(x)