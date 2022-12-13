# game class

from properties import *
from player import Player


class Game:
    def __init__(self, game_id: int):
        self.id = game_id
        self.started = False
        self.players = []
        self.ready = False
        self.props = PropertyMap()

    def start(self):
        """
        Starts the game if all 4 players press the ready button
        :return:
        """
        self.started = True
        for player in self.players:
            player.location = self.props.start


    def play(self):
        """
        plays the game
        :return:
        """
        pass

    def add_player(self, player):
        self.players.append(player)
