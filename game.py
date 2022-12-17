# game class

import random
from properties import *

class Game:
    def __init__(self, game_id: int):
        self.id = game_id
        self.started = False
        self.players = []
        self.ready = False
        self.props = [i for i in range(0, 32)]  # list of property id's
        self.propmap = PropertyMap()

        self.turn = None
        self.rolling = False
        self.endturn = False
        self.lastroll = (0, 0)
        self.goto_next = 0

    def start(self):
        """
        Starts the game if all 4 players press the ready button
        :return:
        """
        self.started = True

        firstturn = random.randrange(0, len(self.players))
        self.turn = self.players[firstturn].id
        firstturn = random.randrange(0, len(self.players))
        self.rolling = True
        d1 = random.randrange(0, 6)
        d2 = random.randrange(0, 6)
        self.lastroll = (d1, d2)
        print(f"first turn: {self.players[firstturn].color}, id {self.players[self.turn].id}, "
              f"roll: {(self.lastroll[0] + 1, self.lastroll[1] + 1)}")
        self.goto_next = self.players[self.turn].location + d1 + d2 + 2

    def play(self):
        """
        plays the game
        :return:
        """
        if self.turn == len(self.players) - 1:
            self.turn = 0
        else:
            self.turn += 1

        self.rolling = True
        self.endturn = False
        d1 = random.randrange(0, 6)
        d2 = random.randrange(0, 6)
        self.lastroll = (d1, d2)
        print(f"turn: {self.players[self.turn].color}, id {self.players[self.turn].id},"
              f" roll: {(self.lastroll[0] + 1, self.lastroll[1] + 1)}")
        nextloc = self.players[self.turn].location + d1 + d2 + 2
        if nextloc > 31:
            nextloc = nextloc - 32
            # self.players[self.turn]._money += 200
        self.goto_next = nextloc

    def add_player(self, player):
        self.players.append(player)
