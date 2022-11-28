# class for properties that can be bought and sold

class Property:
    """
    property
    """
    def __init__(self, name, color, price, image, house_price, hotel_price):
        self.name = name
        self.color = color
        self.price = price
        self.image = image
        self.monopoly = False
        self.houses = 0
        self.house_price = house_price
        self.hotels = 0
        self.hotel_price = hotel_price
        self.mortgaged = False
        self.boardx = None  # holds the center x pos as it appears on the board
        self.boardy = None  # holds the center y pos as it appears on the bard

    def add_house(self):
        pass

    def sell_house(self):
        pass

    def add_hotel(self):
        pass

    def sell_hotel(self):
        pass


def main():
    """
    save properties to json file
    """
    pass
