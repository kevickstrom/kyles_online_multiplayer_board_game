# player class

class Player:
    """
    Player in the monopoly game with name, color, money and property
    """
    def __init__(self, name, color):
        self._name = name
        self._color = color
        self._money = 1500
        self._property = []

