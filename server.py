from flask import Flask
from flask import request
from flask import jsonify
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from game import Game
import json
import pygame

pygame.init()
game = Game()

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route("/spammer")
def spammer_socket(ws):
    while not ws.closed:
        game.update()
        ws.receive()

@sockets.route("/client")
def client_socket(ws):
    while not ws.closed:
        message = ws.receive()
        data = json.loads(message);
        if data["type"] == "spawnMonster":
            reply = json.dumps(game.spawn_monster(data["pos"]))
            print(data["pos"])
            ws.send(reply)
        elif data["type"] == "spawnPotion":
            reply = json.dumps(game.spawn_potion(data["pos"]))
            print(data["pos"])
            ws.send(reply)
        elif data["type"] == "world":
            reply = json.dumps( { "player": game.get_player_pos(), "monsters": game.get_monsters(), "potions": game.get_potions() } )
            ws.send(reply)
        elif data["type"] == "goals":
            reply = json.dumps( { "playerGoal": game.get_player_goal(), "audienceGoal": game.get_audience_goal() } )
            ws.send(reply)

        ws.send(message)

@app.route("/spamTheHellOutOfTheServer")
def spam_handler():
    return """
    <head>
    </head>
    <body>
    <script>
    var spammer_link = "ws" + document.location.origin.substr(4) + "/spammer";
    var socket = new WebSocket(spammer_link);

    function recurse() {
        setTimeout(recurse, 200);
        socket.send(1);
    }

    recurse();
    </script>
    </body>"""

@app.route("/view")
def handler():
    return """
    <head>
    <style>
    body {
        font-family: "Lucida Console", Monaco, monospace;
    }
    </style>
    </head>
    <body>
    <canvas id="map" width="800" height="800"></canvas>
    <script>
    var link = \"ws\" + document.location.origin.substr(4) + \"/client\";
    var socket = new WebSocket(link);
    socket.onmessage = function (msg) {
        console.log(JSON.parse(msg.data));
    };

    function reqWorld() {
        socket.send(JSON.stringify({"type":"world"}));
    }

    function reqGoals() {
        socket.send(JSON.stringify({"type":"goals"}));
    }

    function spawnMonster(pos) {
        socket.send(JSON.stringify({"type":"spawnMonster","pos":pos}));
    }

    function spawnPotion(pos) {
        socket.send(JSON.stringify({"type":"spawnPotion","pos":pos}));
    }
    var monsterNotPotion = false;

    function s(posX, posY) {
        if (monsterNotPotion) {
            spawnMonster([posX, posY]);
        }
        else {
            spawnPotion([posX, posY]);
        }
    }

    var map = document.getElementById('map');
    var ctx = map.getContext('2d');

    ctx.fillStyle = 'rgb(0,0,0)';
    ctx.fillRect(0,0,800,800);

    /*
    var contents = [];
    String.prototype.replaceAt = function(index, character) {
        return this.substr(0, index) + character + this.substr(index+character.length);
    }

    contents.push("+");
    for (i=0;i<119;i++) {
        contents[0] += "-";
    }
    contents[0] += "+";

    for (line=1;line<=119;line++) {
        contents.push("");
        for (room=0;room<5;room++) {
            if (line % 24 == 12 && room != 0) {
                contents[line] += "/";
            }
            else {
                contents[line] += "|";
            }
            for (x=0;x<23;x++) {
                if (line % 24 == 0) {
                    if (x % 24 == 12) {
                    contents[line] += "/";
                    }
                    else {
                    contents[line] += "-";
                    }
                }
                else {
                    contents[line] += "<a onClick=\\"s(" + (room * 24 + x + 1) + "," + line + ")\\">O</a>";
                }
            }
        }
        contents[line] += "|";
    }

    contents.push("+");
    for (i=0;i<119;i++) {
        contents[120] += "-";
    }
    contents[120] += "+";
    */

    for (i=0;i<121;i++) {
        //document.body.innerHTML+=contents[i];
        //document.body.innerHTML+="<br>";
    }
    </script>
    </body>"""

server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
server.serve_forever()

#app.run()
