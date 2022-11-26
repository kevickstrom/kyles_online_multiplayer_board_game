# monopoly test script

import os
import random
import time
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

    # display text
    font = pygame.font.Font(None, 36)
    text = font.render("press space to roll dice", True, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery - 100
    background.blit(text, textpos)

    # blit to screen
    screen.blit(background, (0, 0))


def roll_dice():
    """
    Blits the dice and returns their result
    """
    num1 = random.randrange(0, 6)
    dice1 = faces[num1]
    dice1rect = dice1.get_rect()
    dice1rect.centerx = screen.get_rect().centerx - 25
    dice1rect.centery = screen.get_rect().centery
    screen.blit(dice1, dice1rect)

    num2 = random.randrange(0, 6)
    dice2 = faces[num2]
    dice2rect = dice2.get_rect()
    dice2rect.centerx = screen.get_rect().centerx + 25
    dice2rect.centery = screen.get_rect().centery
    screen.blit(dice2, dice2rect)

    result1 = num1 + 1
    result2 = num2 + 1

    return result1 + result2


def main():
    """
    Main game loop
    """
    draw()
    clock = pygame.time.Clock()
    roll = False
    stop_roll = True

    # event loop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not roll:
                    roll = True
                    stop_roll = False
                elif event.key == pygame.K_SPACE and roll:
                    stop_roll = True
            if event.type == pygame.QUIT:
                return

        draw()
        if roll:
            roll_result = roll_dice()
            if stop_roll:
                time.sleep(1)
                roll = False
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
