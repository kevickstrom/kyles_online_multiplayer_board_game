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
        # sets player location to go using id 0
        for player in self.players:
            player.location = self.props[0]

        firstturn = random.randrange(0, len(self.players), 1)
        self.turn = self.players[firstturn].id

        self.players[firstturn].rolling = True
        d1 = random.randrange(0, 6)
        d2 = random.randrange(0, 6)
        self.players[firstturn].lastroll = (d1, d2)

    def play(self):
        """
        plays the game
        :return:
        """
        pass

    def add_player(self, player):
        self.players.append(player)
