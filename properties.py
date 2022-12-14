# class for all squares on the board

class Property:
    """
    property
    """
    def __init__(self, id: int, name: str, color: str, price: int):
        self.id = id
        self.name = name
        self.color = color
        self.price = price
        self.rent = self.price
        self.price_pos = None

        self.image = None
        self.monopoly = False
        self.level = 0
        self.level_up_price = self.price
        self.leveldown = 0

        self.owned = None  # stores id of who owns the property. None for bank owned, -1 means cannot be owned
        self.mortgaged = False
        self.spots = []  # holds (x,y) location of spots for the client to fill in
        self.next = None
        self.back = None

    def buy(self, owner_id: int):
        self.owned = owner_id
        self.rent = self.price // 4

    def sell(self):
        self.owned = None
        self.rent = self.price
        self.level = 0
        self.leveldown = 0

    def level_up(self):
        self.level += 1
        self.rent = 2 * self.rent

    def level_down(self, levels: int):
        self.level -= levels
        self.rent = self.price * (self.level + 1)

    def __repr__(self):
        return repr(f"Property({self.id}, {self.name}, {self.color}, {self.price})")


class PropertyMap:
    """
    Linked-list style inorder for each property on the board
    Also has list of all properties in order of board appearance
    """
    def __init__(self):
        """
        Initializes board inorder
        """
        self.inorder = []
        self.start = None
        self.initmap()
        self.colors = {
            "brown": (143, 86, 59),
            "bus": (255, 255, 255),
            "blue": (99, 155, 255),
            "pink": (215, 123, 186),
            "orange": (223, 113, 38),
            "red": (172, 50, 50),
            "yellow": (251, 242, 54),
            "green": (55, 148, 110),
            "purple": (63, 63, 116)
        }

    def initmap(self):
        """
        Adds all the properties to the inorder list
        """
        go = Property(0, "Go", "Go", 0)
        go.owned = -1
        brown1 = Property(1, "Brown 1", "brown", 100)
        brown2 = Property(2, "Brown 2", "brown", 120)
        brown3 = Property(3, "Brown 3", "brown", 120)
        bus1 = Property(4, "Bus 1", "bus", 200)
        blue1 = Property(5, "Blue 1", "blue", 140)
        blue2 = Property(6, "Blue 2", "blue", 140)
        blue3 = Property(7, "Blue 3", "blue", 160)
        jail = Property(8, "Jail", "jail", 200)
        jail.owned = -1
        pink1 = Property(9, "Pink 1", "pink", 180)
        pink2 = Property(10, "Pink 2", "pink", 180)
        pink3 = Property(11, "Pink 3", "pink", 200)
        star1 = Property(12, "Starship 1", "starship", 0)
        star1.owned = -1
        orange1 = Property(13, "Orange 1", "orange", 220)
        bus2 = Property(15, "Bus 2", "bus", 200)
        orange2 = Property(15, "Orange 2", "orange", 220)
        corner2 = Property(16, "Corner 2", "corner", 0)
        corner2.owned = -1
        red1 = Property(17, "Red 1", "red", 240)
        bus3 = Property(18, "Bus 3", "bus", 200)
        red2 = Property(19, "Red 2", "red", 240)
        star2 = Property(20, "Starship 2", "starship", 0)
        star2.owned = -1
        yellow1 = Property(21, "Yellow 1", "yellow", 260)
        yellow2 = Property(22, "Yellow 2", "yellow", 280)
        yellow3 = Property(23, "Yellow 3", "yellow", 300)
        corner3 = Property(24, "Corner 3", "corner", 0)
        corner3.owned = -1
        bus4 = Property(25, "Bus 4", "bus", 200)
        green1 = Property(26, "Green 1", "green", 320)
        green2 = Property(27, "Green 2", "green", 360)
        star3 = Property(28, "Starship 3", "starship", 0)
        star3.owned = -1
        purple1 = Property(29, "Purple 1", "purple", 380)
        tuition = Property(30, "Tuition Due", "tuition", 500)
        purple2 = Property(31, "Purple 2", "purple", 400)

        self.inorder.append(go)
        self.inorder.append(brown1)
        self.inorder.append(brown2)
        self.inorder.append(brown3)
        self.inorder.append(bus1)
        self.inorder.append(blue1)
        self.inorder.append(blue2)
        self.inorder.append(blue3)
        self.inorder.append(jail)
        self.inorder.append(pink1)
        self.inorder.append(pink2)
        self.inorder.append(pink3)
        self.inorder.append(star1)
        self.inorder.append(orange1)
        self.inorder.append(bus2)
        self.inorder.append(orange2)
        self.inorder.append(corner2)
        self.inorder.append(red1)
        self.inorder.append(bus3)
        self.inorder.append(red2)
        self.inorder.append(star2)
        self.inorder.append(yellow1)
        self.inorder.append(yellow2)
        self.inorder.append(yellow3)
        self.inorder.append(corner3)
        self.inorder.append(bus4)
        self.inorder.append(green1)
        self.inorder.append(green2)
        self.inorder.append(star3)
        self.inorder.append(purple1)
        self.inorder.append(tuition)
        self.inorder.append(purple2)

        # assign next property
        for i in range(31):
            self.inorder[i].next = self.inorder[i + 1]
        self.inorder[-1].next = self.inorder[0]

        # assign last property
        for i in range(1, 32):
            self.inorder[i].back = self.inorder[i - 1]
        self.inorder[0].back = self.inorder[-1]

        # assign head of 'circular' ll
        self.start = self.inorder[0]

    def getinorder(self) -> list:
        return self.inorder


def main():
    """
    save properties to json file??
    """
    default = PropertyMap()
    print(default.inorder)
    first = default.start
    print(first)
    print(f"next:{first.next}")
    print(f"last:{first.back}")


if __name__ == "__main__":
    main()
