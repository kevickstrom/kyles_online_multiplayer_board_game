# button class for the game and menus
from game import screen
import time
import pygame


class Button:
    """
    button for monopoly game
    """

    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.smoothscale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        """
        draw button on screen
        returns true if clicked
        """
        if self.clicked:
            self.clicked = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return self.clicked
