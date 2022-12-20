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
        self.spot = 0
        self.nextlocation = 99  # id of the next location
        self.nextspot = 0

        self.buy = False
        self.bought = False
        self.paid = False
        self.sell = False
        self.sold = False

        self.lvlup = False
        self.lvld = False

        self.endturn = True
        self.rolling = False
        self.showroll = False
        self.moving = False
