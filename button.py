# button class for the game and menus
from client import screen
import time
import pygame


class Button:
    """
    button for monopoly game
    """

    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.scale = scale
        self.image = pygame.transform.smoothscale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
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

    def blit(self, surface, offset=0):
        """
        same functionality as draw excecpt it blits to a surface instead of the screen
        """
        if self.clicked:
            self.clicked = False
        mouse = pygame.mouse.get_pos()
        pos = (mouse[0], mouse[1] - offset)
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return self.clicked

    def update_pos(self, x, y):
        """
        updates position
        """
        self.rect.topleft = (x, y)

    def changeimg(self, img):
        width = img.get_width()
        height = img.get_height()
        self.image = pygame.transform.smoothscale(img, (int(width * self.scale), int(height * self.scale)))
        self.rect = self.image.get_rect()
