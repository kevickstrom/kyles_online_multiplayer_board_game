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

        self.location = None  # id of the current location
        self.spot = None
        self.nextlocation = None  # id of the next location
        self.nextspot = None
        self.midloc = None

        self.rolling = False
        self.moving = 0  # 0 represents not moving. Any other number indicates moving
        self.lastroll = (0, 0)

    def move(self, location):
        """
        Moves the player to next location
        """
        pass
