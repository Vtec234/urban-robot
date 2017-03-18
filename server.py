from flask import Flask
from flask import request
from flask import jsonify

from game import Game

game = Game()

app = Flask(__name__)

@app.route("/world", methods = ["GET"])
def handleGetWorld():
    return jsonify( { "player": game.get_player_pos(), "monsters": game.get_monsters(), "potions": game.get_potions() } )

@app.route("/goals", methods = ["GET"])
def handleGetGoals():
    return jsonify( { "playerGoal": game., "audienceGoal": (45, 3) } )

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
