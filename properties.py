# class for properties that can be bought and sold

class Property:
    """
    property
    """
    def __init__(self, id: int, name: str, color: str, price: int):
        self.id = id
        self.name = name
        self.color = color
        self.price = price
        self.image = None
        self.monopoly = False
        self.houses = 0
        self.house_price = None
        self.hotels = 0
        self.hotel_price = None
        self.mortgaged = False
        self.boardx = None  # holds the center x pos as it appears on the board
        self.boardy = None  # holds the center y pos as it appears on the bard
        self.next = None

    def add_house(self):
        pass

    def sell_house(self):
        pass

    def add_hotel(self):
        pass

    def sell_hotel(self):
        pass


class PropertyMap:
    """
    Linked-list style map for each property on the board
    """


def main():
    """
    save properties to json file??
    """
    go = Property(0, "Go", "Go", 0)

