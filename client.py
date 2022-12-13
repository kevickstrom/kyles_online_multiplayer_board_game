# monopoly test script

import os
import sys
import random
import time
import webbrowser
import pygame
import button
from player import Player
from network import Network

# initialize screen
pygame.init()
display_info = pygame.display.Info()
WIDTH = display_info.current_w
HEIGHT = display_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
fullscreen = True
pygame.display.set_caption("Monopoly but only Kyle can cheat")
base_font = pygame.font.Font(None, 32)

# load images
# dice load
faces = [pygame.image.load((os.path.join('dice-sheet', '1face.png'))),
         pygame.image.load((os.path.join('dice-sheet', '2face.png'))),
         pygame.image.load((os.path.join('dice-sheet', '3face.png'))),
         pygame.image.load((os.path.join('dice-sheet', '4face.png'))),
         pygame.image.load((os.path.join('dice-sheet', '5face.png'))),
         pygame.image.load((os.path.join('dice-sheet', '6face.png')))]

# game board
board = pygame.image.load(os.path.join('assets', "board.png"))
board = pygame.transform.smoothscale(board, (HEIGHT, HEIGHT))
boardrect = board.get_rect()

# button images
settingsimg = pygame.image.load(os.path.join('assets', "settings2.png"))
exitimg = pygame.image.load(os.path.join('assets', "exit.png"))
backimg = pygame.image.load(os.path.join('assets', "back.png"))
githubimg = pygame.image.load(os.path.join('assets', "github.png"))
notreadyimg = pygame.image.load(os.path.join('assets', "notready.png"))
readyimg = pygame.image.load(os.path.join('assets', "ready.png"))


def draw_board():
    """
    Draws the board
    """
    # fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((10, 10, 10))

    boardrect.right = background.get_rect().right
    boardrect.centery = background.get_rect().centery
    background.blit(board, boardrect)

    # display text
    font = pygame.font.Font(None, 36)
    text = font.render("press space to roll dice", True, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = boardrect.centerx
    textpos.centery = boardrect.centery - 100
    background.blit(text, textpos)

    # blit to screen
    screen.blit(background, (0, 0))


def draw_players(game, myself: Player):
    """
    Draws everything left of the board
    """
    settings = button.Button(96, 16, settingsimg, 0.5)
    exit_button = button.Button(32, 16, exitimg, 0.5)
    notready_button = button.Button(boardrect.left - 96, HEIGHT - 50, notreadyimg)
    ready_button = button.Button(boardrect.left - 96, HEIGHT - 50, readyimg)
    border = pygame.Rect(0, 0, WIDTH - boardrect.width, exit_button.rect.height + 2)
    pygame.draw.rect(screen, (52, 78, 91), border)
    if settings.draw():
        settings_menu()
    if exit_button.draw():
        pygame.quit()
        sys.exit()
    if not game.ready:
        if not myself.ready:
            if notready_button.draw():
                myself.ready = True
                time.sleep(0.05)
        else:
            if ready_button.draw():
                myself.ready = False
                time.sleep(0.05)

    i = 0
    for player in game.players:

        # blit color
        pygame.draw.circle(screen, player.color, (20, i + 50), 10)

        # blit name
        player_name = base_font.render(player.name, True, (255, 255, 255))
        player_namerect = player_name.get_rect()
        player_namerect.centery = i + 50
        screen.blit(player_name, (40, player_namerect.centery))

        # blit money
        money = str(player._money)
        player_money = base_font.render(f"${money}", True, (255, 255, 255))
        player_moneyrect = player_money.get_rect()
        player_moneyrect.centery = player_moneyrect.height + player_namerect.centery
        screen.blit(player_money, (40, player_moneyrect.centery))
        i += 100


def roll_dice() -> (int, int):
    """
    Blits the dice and returns their result
    """
    num1 = random.randrange(0, 6)
    dice1 = faces[num1]
    dice1rect = dice1.get_rect()
    dice1rect.centerx = boardrect.centerx - 25
    dice1rect.centery = boardrect.centery
    screen.blit(dice1, dice1rect)

    num2 = random.randrange(0, 6)
    dice2 = faces[num2]
    dice2rect = dice2.get_rect()
    dice2rect.centerx = boardrect.centerx + 25
    dice2rect.centery = boardrect.centery
    screen.blit(dice2, dice2rect)

    result1 = num1 + 1
    result2 = num2 + 1

    return result1 + result2


def start_menu(playernum: int) -> Player:
    """
    Starting menu when the game is launched
    initializes and returns player - name, color
    """
    user_text = ''
    input_rect = pygame.Rect(200, 200, 140, 32)

    # gets active when input box is clicked by user
    color_active = pygame.Color('lightskyblue3')
    # color of input box.
    color_passive = pygame.Color('grey')
    clock = pygame.time.Clock()

    choice = 0
    left_button = button.Button(WIDTH//2 - 250, HEIGHT//2, faces[choice], 1)
    right_button = button.Button(WIDTH//2 + 250, HEIGHT//2, faces[choice + 1], 1)
    color_choices = ["RED", "GREEN", "BLUE", "YELLOW", "CYAN", "MAGENTA"]

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

        # enter color
        if choice > 0:
            if left_button.draw():
                choice -= 1
                left_button.image = faces[choice - 1]
                right_button.image = faces[choice + 1]
                time.sleep(0.2)
        if choice < 5:
            if right_button.draw():
                choice += 1
                left_button.image = faces[choice - 1]
                if choice < 5:
                    right_button.image = faces[choice + 1]
                time.sleep(0.2)
        color_text_surface = base_font.render("Choose a color:", True, (255, 255, 255))
        screen.blit(color_text_surface, (WIDTH//2 - color_text_surface.get_width()//2, HEIGHT//2 - 100))
        pygame.draw.circle(screen, color_choices[choice], (WIDTH//2, HEIGHT//2), 50)

        # enter name
        pygame.draw.rect(screen, color, input_rect)
        user_text_surface = base_font.render(user_text, True, (255, 255, 255))
        name_text_surface = base_font.render("Enter your name:", True, (255, 255, 255))
        screen.blit(user_text_surface, (input_rect.x + 5, input_rect.y + 5))
        screen.blit(name_text_surface, (input_rect.x, input_rect.y - name_text_surface.get_height()))
        input_rect.w = max(100, user_text_surface.get_width() + 10)

        pygame.display.flip()
        clock.tick(30)
    me = Player(playernum)
    me.name = user_text
    me.color = color_choices[choice]
    return me


def settings_menu():
    """
    Settings menu with buttons
    """

    # buttons
    back_button = button.Button(WIDTH // 2, HEIGHT // 2 - 100, backimg, 1)
    exit_button = button.Button(WIDTH // 2, HEIGHT // 2, exitimg, 1)
    github = button.Button(WIDTH // 2, HEIGHT // 2 + 100, githubimg, 1)

    clock = pygame.time.Clock()
    menu = True
    while menu:
        global screen
        screen.fill((52, 78, 91))
        if back_button.draw():
            menu = False
        if exit_button.draw():
            pygame.quit()
            sys.exit()
        if github.draw():
            webbrowser.open(r"https://github.com/kevickstrom/monopoly_butonlykylecancheat")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        clock.tick(30)


def main():
    """
    Main game loop
    """
    n = Network()
    playernum = int(n.getP())
    draw_board()
    clock = pygame.time.Clock()
    roll = False
    stop_roll = True

    # event loop
    run = True
    firststart = True
    while run:
        # start menu
        if firststart:
            firststart = False
            myself = start_menu(playernum)
            n.update(myself)

        # update game
        try:
            game = n.update(myself)
            for player in game.players:
                if player.id == playernum:
                    myself = player
        except:
            run = False
            print("Couldn't get game")
            break

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not roll:
                    roll = True
                    stop_roll = False
                elif event.key == pygame.K_SPACE and roll:
                    stop_roll = True
            if event.type == pygame.QUIT:
                run = False

        # drawing to screen
        draw_board()
        draw_players(game, myself)
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
