import sys
import json

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from flask import Flask
from flask import request
from flask import jsonify
from flask_sockets import Sockets

import pygame
from game import Game

pygame.init()
pygame.mixer.music.load("./loop.ogg")
game = Game()
pygame.mixer.music.play(-1)

app = Flask(__name__)
sockets = Sockets(app)


@sockets.route("/spammer")
def spammer_socket(ws):
    while not ws.closed:
        try:
            result = game.update()
            if not result:
                pygame.quit()
                sys.exit()
        except:
            print("exception occurred", sys.exc_info())

        ws.receive()

@app.route("/spamTheHellOutOfTheServer")
def spam_handler():
    return """
    <head>
    </head>
    <body>
    <script>
    window.onload = function() {
        var spammer_link = "ws" + document.location.origin.substr(4) + "/spammer";
        var socket = new WebSocket(spammer_link);
        socket.onopen = function() {
            function recurse() {
                setTimeout(recurse, 250);
                socket.send(1);
            }

            recurse();
        };
    };
    </script>
    </body>"""

@sockets.route("/client")
def client_socket(ws):
    while not ws.closed:
        message = ws.receive()
        data = json.loads(message)
        if data["type"] == "spawnMonster":
            try:
                result = game.spawn_monster(data["pos"])
                reply = json.dumps( { "smResult": result } )
                ws.send(reply)
            except:
                print("error handling spawnMonster", sys.exc_info())
        elif data["type"] == "spawnPotion":
            try:
                result = game.spawn_potion(data["pos"])
                reply = json.dumps( { "spResult": result } )
                ws.send(reply)
            except:
                print("error handling spawnPotion", sys.exc_info())
        elif data["type"] == "world":
            reply = json.dumps( { "world": 1, "player": game.get_player_pos(), "monsters": game.get_monsters(), "potions": game.get_potions() } )
            ws.send(reply)
        elif data["type"] == "goals":
            reply = json.dumps( { "goals": 1, "playerGoal": game.get_player_goal(), "audienceGoal": game.get_audience_goal() } )
            ws.send(reply)

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
    <input id="monsterBox" type="checkbox">
    <script>
    window.onload = function() {
        var link = \"ws\" + document.location.origin.substr(4) + \"/client\";
        var socket = new WebSocket(link);
        socket.onopen = function() {
            var canvas = document.getElementById('map');
            var ctx = canvas.getContext('2d');
            var raf;

            var WIDTH = 121.0;
            var HEIGHT = 121.0;
            var monsters = [];
            var potions = [];
            var player = [0, 0];
            var pgoal = [0, 0];
            var agoal = [0, 0];

            socket.onmessage = function (msg) {
                var data = JSON.parse(msg.data);
                console.log(data);
                if (data.world) {
                    player = data.player;
                    monsters = data.monsters;
                    potions = data.potions;
                }
                else if (data.goals) {
                    pgoal = data.playerGoal;
                    agoal = data.audienceGoal;
                }
                else if (data.smResult) {
                    console.log("smResult");
                }
                else if (data.spResult) {
                    console.log("spResult");
                }
            };

            function reqGoals() {
                socket.send(JSON.stringify({"type": "goals"}));
            }

            function reqWorld() {
                socket.send(JSON.stringify({"type": "world"}));
            }

            function spawnMonster(pos) {
                var son = JSON.stringify({"type": "spawnMonster", "pos": pos});
                socket.send(son);
            }

            function spawnPotion(pos) {
                var son = JSON.stringify({"type": "spawnPotion", "pos": pos});
                socket.send(son);
            }

            var monsterNotPotion = false;
            function spawn(posX, posY) {
                if (monsterNotPotion) {
                    spawnMonster([posX, posY]);
                }
                else {
                    spawnPotion([posX, posY]);
                }
            }

            function convPos(pos) {
                return [pos[0]/WIDTH * canvas.width, pos[1]/HEIGHT * canvas.height];
            }

            function invertConvPos(pos) {
                return [Math.floor(pos[0] / canvas.width * WIDTH), Math.floor(pos[1] / canvas.height * HEIGHT)];
            }

            function draw() {
                ctx.fillStyle = 'rgb(0, 0, 0)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                for (ix=0;ix<6;ix++) {
                    var x = ix*(24/WIDTH*canvas.width);
                    ctx.fillStyle = 'rgb(255, 255, 255)';
                    ctx.fillRect(x,0,3,canvas.height);
                    if (ix > 0 && ix < 5) {
                        for (iy=0;iy<5;iy++) {
                        ctx.fillStyle = 'rgb(0, 0, 0)';
                            ctx.fillRect(x,(iy*24+12)/HEIGHT*canvas.height, 3, 7);
                        }
                    }
                }

                for (iy=0;iy<6;iy++) {
                    var y = iy*(24/HEIGHT*canvas.height);
                    ctx.fillStyle = 'rgb(255, 255, 255)';
                    ctx.fillRect(0,y,canvas.width,3);
                    if (iy > 0 && iy < 5) {
                        for (ix=0;ix<5;ix++) {
                        ctx.fillStyle = 'rgb(0, 0, 0)';
                            ctx.fillRect((ix*24+12)/WIDTH*canvas.width,y, 7, 3);
                        }
                    }
                }

                ctx.fillStyle = 'rgb(255, 0, 0)';
                for (i=0;i<monsters.length;i++) {
                    var pos = convPos(monsters[i]);
                    ctx.fillRect(pos[0], pos[1], 5, 5);
                }

                ctx.fillStyle = 'rgb(0, 255, 0)';
                for (i=0;i<potions.length;i++) {
                    var pos = convPos(potions[i]);
                    ctx.fillRect(pos[0], pos[1], 5, 5);
                }

                ctx.fillStyle = 'rgb(0, 0, 255)';
                {
                    var pos = convPos(player);
                    ctx.fillRect(pos[0], pos[1], 7, 7);
                }

                    ctx.fillStyle = 'rgb(255, 0, 255)';
                {
                    var pos = convPos(pgoal);
                    ctx.fillRect(pos[0], pos[1], 5, 5);
                }

                    ctx.fillStyle = 'rgb(255, 255, 0)';
                {
                    var pos = convPos(agoal);
                    ctx.fillRect(pos[0], pos[1], 5, 5);
                }

                raf = window.requestAnimationFrame(draw);
            }

            canvas.addEventListener('mouseover', function(e) {
                raf = window.requestAnimationFrame(draw);
            });

            canvas.addEventListener('click', function(e) {
                var x = e.pageX - canvas.offsetLeft;
                var y = e.pageY - canvas.offsetTop;
                var pos = invertConvPos([x, y]);
                spawn(pos[0], pos[1]);
            });

            function begin() {
                reqGoals();

                recurse();
            }

            function recurse() {
                reqWorld();

                var box = document.getElementById("monsterBox");
                if (box.checked) {
                    monsterNotPotion = true;
                }
                else {
                    monsterNotPotion = false;
                }

                setTimeout(recurse, 500);
            }

            begin();
        };
    };
    </script>
    </body>"""

server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
server.serve_forever()

#app.run()
