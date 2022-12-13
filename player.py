# player class

class Player:
    """
    Player in the monopoly game with name, color, money and property
    """
    def __init__(self, id: int):
        self.id = id
        self.name = None
        self.color = (255, 255, 255)
        self._money = 1500
        self._properties = []
        self.ready = False
        self.location = None

