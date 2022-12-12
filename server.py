
import socket
import pickle
from _thread import *
from game import *
import player

server = "10.0.0.142"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    selected = False
    while not selected:
        # receive filled out player class
        try:
            player = pickle.loads(conn.recv(2048 * 2))
            if gameId in games:
                game = games[gameId]

                conn.send(pickle.dumps(game))
                if player:
                    game.add_player(player)
                    selected = True
        except:
            pass

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    # handle string data
                    if data == "reset":
                        pass
                        # game.resetWent()
                    elif data != "get":
                        pass
                        # game.play(p, data)

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
        games[gameId].ready = True
        p = len(games[gameId].players)

    start_new_thread(threaded_client, (conn, p, gameId))
