
import socket
import pickle
from _thread import *
from game import *

server = "10.0.0.88"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    """
    One thread per connection
    :param conn: Socket connection
    :param p: number representing the player
    :param gameId: ID of the game the player is in
    :return: None
    """
    global idCount
    conn.send(str.encode(str(p)))
    selected = False
    while not selected:
        # receive filled out player class
        try:
            player = pickle.loads(conn.recv(2048 * 4))
            if gameId in games:
                game = games[gameId]

                conn.send(pickle.dumps(game))
                if player:
                    game.add_player(player)
                    selected = True
        except:
            pass

    while True:
        try:
            # receive data from client
            data = pickle.loads(conn.recv(2048 * 4))

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    # update player data
                    allready = False
                    for i in range(len(game.players)):
                        if game.players[i].id == data.id:
                            game.players[i] = data
                            break

                    # update game data
                    if not game.started:
                        for player in game.players:
                            if player.ready:
                                allready = True
                            else:
                                allready = False
                                break
                        if allready:
                            game.ready = True
                            game.start()
                            print("ready gamers")
                    # game is started
                    else:
                        if not game.endturn and game.players[game.turn].endturn:
                            game.endturn = True
                        for player in game.players:
                            player.endturn = False
                            if game.turn == player.id and not player.rolling:
                                if game.goto_next < 12 and player.location > 12 and not player.endturn:
                                    game.players[game.turn]._money += 200

                            if player.id == game.turn and game.endturn:
                                game.play()
                    # send updated game
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


p = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    gameId = (idCount - 1)//4
    if idCount % 4 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
        p = 0
    else:
        # games[gameId].ready = True
        p += 1

    start_new_thread(threaded_client, (conn, p, gameId))
