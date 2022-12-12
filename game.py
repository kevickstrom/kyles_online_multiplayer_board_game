from player import Player


class Game:
    def __init__(self, game_id: int):
        self.id = game_id
        self.started = False
        self.players = []
        self.ready = False
        self.players = []
        self.properties = []

    def play(self):
        """
        Starts the game if all 4 players press the ready button
        :return:
        """
        for player in self.players:
            if player.ready:
                pass
            else:
                pass

    def add_player(self, player):
        self.players.append(player)
