from flask import Flask
from flask import request
from flask import jsonify
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from game import Game

game = Game()
app = Flask(__name__)
sockets = Sockets(app)


@sockets.route("/client")
def client_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)

@app.route("/view")
def handler():
    return "<b>test</b>"

@app.route("/world", methods = ["GET"])
def handleGetWorld():
    return jsonify( { "player": game.get_player_pos(), "monsters": game.get_monsters(), "potions": game.get_potions() } )

@app.route("/goals", methods = ["GET"])
def handleGetGoals():
    return jsonify( { "playerGoal": game.get_player_goal(), "audienceGoal": game.get_audience_goal() } )

@app.route("/spawnMonster", methods = ["POST"])
def handleSpawnMonster():
    if request.method == "POST":
        data = request.get_json()
        print(data["pos"])
        return jsonify(game.spawn_monster(data["pos"]))

@app.route("/spawnPotion", methods = ["POST"])
def handleSpawnHeal():
    if request.method == "POST":
        data = request.get_json()
        print(data["pos"])
        return jsonify(game.spawn_potion(data["pos"]))


server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
server.serve_forever()

#app.run()
