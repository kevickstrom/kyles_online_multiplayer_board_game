# game class

from properties import *
from player import Player
import random


class Game:
    def __init__(self, game_id: int):
        self.id = game_id
        self.started = False
        self.players = []
        self.ready = False
        self.props = [i for i in range(0, 32)]
        self.turn = None

    def start(self):
        """
        Starts the game if all 4 players press the ready button
        :return:
        """
        self.started = True

        firstturn = random.randrange(0, len(self.players))
        self.turn = self.players[firstturn].id
        # print(f"first turn: {self.players[firstturn].color}, id {self.players[self.turn].id}")

        self.players[self.turn].rolling = True
        self.players[self.turn].endturn = False
        d1 = random.randrange(0, 6)
        d2 = random.randrange(0, 6)
        self.players[self.turn].lastroll = (d1, d2)
        self.players[self.turn].nextlocation = self.players[firstturn].location + d1 + d2 + 2

    def play(self):
        """
        plays the game
        :return:
        """
        if self.turn == len(self.players) - 1:
            self.turn = 0
        else:
            self.turn += 1

        print(f"turn: {self.players[self.turn].color}, id {self.players[self.turn].id}")
        self.players[self.turn].rolling = True
        self.players[self.turn].endturn = False
        d1 = random.randrange(0, 6)
        d2 = random.randrange(0, 6)
        self.players[self.turn].lastroll = (d1, d2)
        nextloc = self.players[self.turn].location + d1 + d2 + 2
        if nextloc > 31:
            nextloc = nextloc - 32
        self.players[self.turn].nextlocation = nextloc

    def add_player(self, player):
        self.players.append(player)
