
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
                        if game.players[game.turn].endturn and game.endturn:
                            game.play()
                        for player in game.players:
                            if game.turn == player.id and not player.rolling:
                                if player.location == player.nextlocation:
                                    game.rolling = False
                                if player.endturn:
                                    game.endturn = True
                                if game.collect_go:
                                    game.collect_go = False
                                    game.player_money[game.turn] += 200
                                landed_on = game.propmap.inorder[game.goto_next]
                                if landed_on.owned is not None and landed_on.owned != player.id and not player.paid:
                                    if not player.rolling and landed_on.owned > -1:
                                        game.rent_paid = True
                                        player.paid = True
                                        game.player_money[game.turn] -= landed_on.rent
                                        game.player_money[landed_on.owned] += landed_on.rent
                                # buying property and checking for monopoly
                                if player.buy and not player.bought:
                                    game.propmap.inorder[player.location].buy(player.id)
                                    game.player_money[game.turn] -= game.propmap.inorder[player.location].price
                                    color = game.propmap.inorder[player.location].color
                                    group = []
                                    monopolized = False
                                    for i in range(len(game.propmap.inorder)):
                                        if game.propmap.inorder[i].color == color:
                                            group.append(game.propmap.inorder[i])
                                    for prop in group:
                                        if prop is not None:
                                            if prop.owned == player.id:
                                                monopolized = True
                                            else:
                                                monopolized = False
                                                break
                                    if monopolized:
                                        for prop in group:
                                            if not prop.monopoly:
                                                prop.monopoly = True
                                                prop.level += 1
                                                prop.rent = 2*prop.rent
                                    player.bought = True
                                # level up property
                                if landed_on.owned is not None:
                                    if landed_on.owned == player.id:
                                        if landed_on.monopoly:
                                            if player.lvlup and not player.lvld:
                                                player.lvld = True
                                                landed_on.level += 1
                                                current = landed_on.rent
                                                landed_on.rent = 2 * current
                                                print(landed_on.rent)
                                                game.player_money[game.turn] -= landed_on.price
                                                game.leveled = True
                                        # selling property
                                        if player.sell and not player.sold:
                                            player.sold = True
                                            if landed_on.level == 0:
                                                game.player_money[game.turn] += landed_on.price
                                            else:
                                                game.player_money[game.turn] += landed_on.price * landed_on.level
                                            landed_on.owned = None
                                            landed_on.level = 0
                                            landed_on.rent = landed_on.price
                                            for samecolor in game.propmap.inorder:
                                                if samecolor.color == landed_on.color:
                                                    if samecolor.monopoly:
                                                        game.player_money[game.turn] += \
                                                            samecolor.price * (samecolor.level - 1)
                                                    samecolor.monopoly = False
                                                    samecolor.level = 0
                                # if player loses / almost loses
                                if game.player_money[player.id] < 0:
                                    playerprops = []
                                    for prop in game.propmap.inorder:
                                        if prop.owned == player.id:
                                            playerprops.append(prop)
                                    networth = 0
                                    for prop in playerprops:
                                        networth += prop.price * (prop.level + 1)
                                    if game.player_money[player.id] + networth < 0:
                                        # player loses game
                                        player.lost = True
                                        player.almostlose = False
                                        for prop in playerprops:
                                            prop.sell()
                                        game.player_money[player.id] = 0
                                    else:
                                        player.almostlose = True
                                    if player.confirm:
                                        print("confrim")
                                        for prop in player.leveldown.keys():
                                            print("in dict")
                                            game.propmap.inorder[prop].level_down(player.leveldown[prop])
                                            game.player_money[player.id] += prop.price * player.leveldown[prop]
                                        for propid in player.tosell:
                                            print("in tosell")
                                            prop = game.propmap.inorder[propid]
                                            game.player_money[player.id] += prop.price * (prop.level + 1)
                                            prop.sell()
                                            print(game.player_money[player.id])
                                        player.tosell = []
                                        player.leveldown = {}
                                        player.confirm = False
                                        player.almostlose = False

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
        p += 1

    start_new_thread(threaded_client, (conn, p, gameId))
