# monopoly test script

import os
import random
import pygame

WIDTH = 1600
HEIGHT = 900

# initialize screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rolling dice")

# dice load
face1 = pygame.image.load((os.path.join('dice-sheet', '1face.png')))
face2 = pygame.image.load((os.path.join('dice-sheet', '2face.png')))
face3 = pygame.image.load((os.path.join('dice-sheet', '3face.png')))
face4 = pygame.image.load((os.path.join('dice-sheet', '4face.png')))
face5 = pygame.image.load((os.path.join('dice-sheet', '5face.png')))
face6 = pygame.image.load((os.path.join('dice-sheet', '6face.png')))
faces = [face1, face2, face3, face4, face5, face6]


def draw():
    """
    drawing on the screen
    """
    # fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((10, 10, 10))

    # blank board
    board = pygame.image.load("classic.jpg")
    board = pygame.transform.scale(board, (900, 900))
    board = pygame.transform.rotate(board, 180)
    boardrect = board.get_rect()
    boardrect.centerx = background.get_rect().centerx
    boardrect.centery = background.get_rect().centery
    background.blit(board, boardrect)

    # load image
    # dice = pygame.image.load("giphy.gif")
    # if roll:
    #     # count += 1
    #     # if count == 15:
    #     #     count = 0
    #     num = random.randrange(0, 6)
    #     dice = faces[num]
    #
    #     dicerect = dice.get_rect()
    #     dicerect.centerx = background.get_rect().centerx
    #     dicerect.centery = background.get_rect().centery
    #     background.blit(dice, dicerect)

    # display text
    font = pygame.font.Font(None, 36)
    text = font.render("Some dice rolling", True, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)

    # blit to screen
    screen.blit(background, (0, 0))


def roll_dice():
    num = random.randrange(0, 6)
    dice = faces[num]

    dicerect = dice.get_rect()
    dicerect.centerx = screen.get_rect().centerx
    dicerect.centery = screen.get_rect().centery
    screen.blit(dice, dicerect)


def main():
    """
    Main game loop
    """
    draw()
    clock = pygame.time.Clock()
    roll = False

    # event loop
    while True:

        if pygame.key.get_pressed()[pygame.K_b] and not roll:
            roll = True
        elif roll and pygame.key.get_pressed()[pygame.K_b]:
            roll = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        draw()
        if roll:
            roll_dice()
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
