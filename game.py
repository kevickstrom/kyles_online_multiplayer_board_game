# game class

import random
from properties import *


class Game:
    def __init__(self, game_id: int):
        self.id = game_id
        self.ready = False
        self.started = False

        self.players = []
        self.player_money = {}
        self.props = [i for i in range(0, 32)]  # list of property id's
        self.propmap = PropertyMap()
        self.leveled = False

        self.turn = None
        self.collect_go = False
        self.rolling = False
        self.moving = False
        self.moved = False
        self.endturn = False
        self.lastroll = (0, 0)
        self.double = 0
        self.goto_next = 0
        self.rent_paid = False

        self.color_pick = ["RED", "GREEN", "BLUE", "YELLOW", "CYAN", "MAGENTA"]

    def start(self):
        """
        Starts the game if all 4 players press the ready button
        :return:
        """
        self.started = True

        for player in self.players:
            self.player_money[player.id] = 1500

        firstturn = random.randrange(0, len(self.players))
        self.turn = self.players[firstturn].id
        firstturn = random.randrange(0, len(self.players))
        self.rolling = True
        d1 = random.randrange(0, 6)
        d2 = random.randrange(0, 6)
        if d1 == d2:
            self.double += 1
        self.lastroll = (d1, d2)
        print(f"first turn: {self.players[firstturn].color}, id {self.players[self.turn].id}, "
              f"roll: {(self.lastroll[0] + 1, self.lastroll[1] + 1)}")
        self.goto_next = self.players[self.turn].location + d1 + d2 + 2

        self.players[self.turn].endturn = False
        self.players[self.turn].rolling = True
        self.players[self.turn].nextlocation = self.goto_next

    def play(self):
        """
        plays the game
        :return:
        """
        self.players[self.turn].endturn = False
        if self.double == 3:
            self.double = 0
        # assign new turn
        if self.double == 0:
            if self.turn == len(self.players) - 1:
                self.turn = 0
            else:
                self.turn += 1

        if self.players[self.turn].lost:
            self.play()
            return

        self.rolling = True
        self.endturn = False
        self.rent_paid = False
        d1 = random.randrange(0, 6)
        d2 = random.randrange(0, 6)
        if d1 == d2:
            self.double += 1
        else:
            self.double = 0
        self.lastroll = (d1, d2)
        print(f"turn: {self.players[self.turn].color}, id {self.players[self.turn].id},"
              f" roll: {(self.lastroll[0] + 1, self.lastroll[1] + 1)}")
        nextloc = self.players[self.turn].location + d1 + d2 + 2
        if nextloc > 31:
            nextloc = nextloc - 32
            self.collect_go = True
        self.goto_next = nextloc

        # reset player daya
        self.leveled = False
        self.players[self.turn].endturn = False
        self.players[self.turn].rolling = True
        self.players[self.turn].nextlocation = self.goto_next
        self.players[self.turn].buy = False
        self.players[self.turn].bought = False
        self.players[self.turn].paid = False
        self.players[self.turn].lvlup = False
        self.players[self.turn].lvld = False
        self.players[self.turn].sell = False
        self.players[self.turn].sold = False
        self.players[self.turn].almostlose = False

    def add_player(self, player):
        self.players.append(player)
        self.color_pick.remove(player.color)
