from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

@app.route("/world", methods = ["GET"])
def handleGetWorld():
    return jsonify( { "player": (2, 4), "monsters": [(2, 4), (3, 7), (1, 0)], "healths": [()] } )

@app.route("/goals", methods = ["GET"])
def handleGetGoals():
    return jsonify( { "playerGoal": (2, 5), "audienceGoal": (45, 3) } )

@app.route("/spawnMonster", methods = ["POST"])
def handleSpawnMonster():
    if request.method == "POST":
        #return jsonify(game.get_monsters())
        # read coords, spawn
        print(request.form)
        return "OK"

@app.route("/spawnHealth", methods = ["POST"])
def handleSpawnHeal():
    if request.method == "POST":
        print(request.form)
        return "OK"
