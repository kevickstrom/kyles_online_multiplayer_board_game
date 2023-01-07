# player class
import time

class Player:
    """
    Player in the monopoly game with name, color, money and property
    """
    def __init__(self, id: int):
        self.id = id
        self.name = ''
        self.color = 0
        self._money = 1500
        self._properties = []
        self.ready = False
        self.lost = False

        self.location = 0  # id of the current location
        self.spot = 0
        self.nextlocation = 99  # id of the next location
        self.nextspot = 0

        self.buy = False
        self.bought = False
        self.paid = False
        self.sell = False
        self.sold = False

        self.auction = False  # true if player is selecting property
        self.aucy = 0
        self.aucselect = None  # holds the id of the property to be auctioned for the player auction select menu
        self.aucstart = False
        self.bid = None  # will be list of bid entries if applicable
        self.aucround = 0

        self.almostlose = False
        self.tosell = []
        self.leveldown = {}
        self.confirm = False

        self.lvlup = False
        self.lvld = False

        self.endturn = False
        self.rolling = False
        self.rolled = False
        self.showroll = False
        self.moving = False
        self.showmoving = False

        self.timer = time.process_time()
