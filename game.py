# game class

from properties import *
from player import Player


class Game:
    def __init__(self, game_id: int):
        self.id = game_id
        self.started = False
        self.players = []
        self.ready = False
        self.players = []
        self.props = PropertyMap()

    def play(self):
        """
        Starts the game if all 4 players press the ready button
        :return:
        """
        allready = False
        for player in self.players:
            if player.ready:
                allready = True
            else:
                allready = False

        if allready:
            for player in self.players:
                player.location = self.props.start

    def add_player(self, player):
        self.players.append(player)
