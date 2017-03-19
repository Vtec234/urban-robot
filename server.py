from flask import Flask
from flask import request
from flask import jsonify

#from game import Game

#game = Game()

app = Flask(__name__)

@app.route("/world", methods = ["GET"])
def handleGetWorld():
    #return jsonify( { "player": game.get_player_pos(), "monsters": game.get_monsters(), "potions": game.get_potions() } )
    return jsonify( { "pos": (2, 4) } )

@app.route("/goals", methods = ["GET"])
def handleGetGoals():
    #return jsonify( { "playerGoal": game.get_player_goal(), "audienceGoal": game.get_audience_goal() } )
    return "OK"

@app.route("/spawnMonster", methods = ["POST"])
def handleSpawnMonster():
    if request.method == "POST":
        # read coords, spawn
        data = request.get_json()
        return jsonify(game.new_mon(data["pos"]))

@app.route("/spawnHealth", methods = ["POST"])
def handleSpawnHeal():
    if request.method == "POST":
        data = request.get_json()
        print(data["pos"])
        return "OK"
