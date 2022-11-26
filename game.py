# monopoly test script

import os
import sys
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
    blits the board and text to the screen
    """
    # fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((10, 10, 10))

    # blank board
    board = pygame.image.load("board.png")
    board = pygame.transform.smoothscale(board, (900, 900))
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


def start_menu():
    """
    Starting menu when the game is launched
    Returns the name of the player
        FUTURE:
                has player fill out player class
                -name and character
    """
    base_font = pygame.font.Font(None, 32)
    user_text = ''
    input_rect = pygame.Rect(200, 200, 140, 32)

    # gets active when input box is clicked by user
    color_active = pygame.Color('lightskyblue3')
    # color of input box.
    color_passive = pygame.Color('grey')
    clock = pygame.time.Clock()
    menu = True
    active = False
    while menu:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    menu = False
                else:
                    user_text += event.unicode

        # color the screen and blit
        screen.fill((52, 78, 91))
        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(screen, color, input_rect)
        user_text_surface = base_font.render(user_text, True, (255, 255, 255))
        name_text_surface = base_font.render("Enter your name:", True, (255, 255, 255))
        screen.blit(user_text_surface, (input_rect.x + 5, input_rect.y + 5))
        screen.blit(name_text_surface, (input_rect.x, input_rect.y - name_text_surface.get_height()))
        input_rect.w = max(100, user_text_surface.get_width() + 10)
        pygame.display.flip()
        clock.tick(30)

    return user_text


def main():
    """
    Main game loop
    """
    draw()
    clock = pygame.time.Clock()
    roll = False
    stop_roll = True

    # event loop
    run = True
    firststart = True
    while run:
        # start menu
        if firststart:
            name = start_menu()
            firststart = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not roll:
                    roll = True
                    stop_roll = False
                elif event.key == pygame.K_SPACE and roll:
                    stop_roll = True
            if event.type == pygame.QUIT:
                run = False

        draw()
        if roll:
            if stop_roll:
                roll = False
                time.sleep(1)
            else:
                roll_result = roll_dice()
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
