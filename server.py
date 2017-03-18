from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

@app.route("/world")
def handleGetWorld():
    return "world"

@app.route("/spawnMonster", methods = ["POST"])
def handleSpawnMonster():
    if request.method == "POST":
        # read coords, spawn
        return "monster spawned"

@app.route("/spawnHealth", methods = ["POST"])
def handleSpawnHealth():
    if request.method == "POST":
        return "health spawned
