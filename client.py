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
from properties import *

# initialize screen
pygame.init()
display_info = pygame.display.Info()
WIDTH = display_info.current_w
HEIGHT = display_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
fullscreen = True
pygame.display.set_caption("Monopoly but only Kyle can cheat")
base_font = pygame.font.Font(None, 32)

# dice load
faces = [pygame.image.load((os.path.join('dice-sheet', '1face.png'))),
         pygame.image.load((os.path.join('dice-sheet', '2face.png'))),
         pygame.image.load((os.path.join('dice-sheet', '3face.png'))),
         pygame.image.load((os.path.join('dice-sheet', '4face.png'))),
         pygame.image.load((os.path.join('dice-sheet', '5face.png'))),
         pygame.image.load((os.path.join('dice-sheet', '6face.png')))]

# game board
board = pygame.image.load(os.path.join('assets', "boardwprice.png"))
board = pygame.transform.smoothscale(board, (HEIGHT, HEIGHT))
boardrect = board.get_rect()

# button images
settingsimg = pygame.image.load(os.path.join('assets', "settings2.png"))
exitimg = pygame.image.load(os.path.join('assets', "exit.png"))
backimg = pygame.image.load(os.path.join('assets', "back.png"))
githubimg = pygame.image.load(os.path.join('assets', "github.png"))
notreadyimg = pygame.image.load(os.path.join('assets', "notready.png"))
readyimg = pygame.image.load(os.path.join('assets', "ready.png"))
endturnimg = pygame.image.load(os.path.join('assets', "endturn.png"))
notendturnimg = pygame.image.load(os.path.join('assets', "notendturn.png"))
buyimg = pygame.image.load(os.path.join('assets', "buy.png"))
lvlupimg = pygame.image.load(os.path.join('assets', "levelup.png"))

# property level images
lvlimg = [pygame.image.load(os.path.join('assets', "lvl0.png")), pygame.image.load(os.path.join('assets', "lvl1.png")),
          pygame.image.load(os.path.join('assets', "lvl2.png")), pygame.image.load(os.path.join('assets', "lvl3.png")),
          pygame.image.load(os.path.join('assets', "lvl4.png")), pygame.image.load(os.path.join('assets', "lvl5.png"))]
for i in range(len(lvlimg)):
    lvlimg[i] = pygame.transform.smoothscale(lvlimg[i], ((boardrect.width // 11)//4, (boardrect.width // 11)//4))

# properties load
properties = PropertyMap()
propwidth = boardrect.width // 11
propheight = propwidth * 2
# assign property's player screen locations
xshift1 = 2 * (propwidth // 3)
xshift2 = 1 * (propwidth // 3)
# bottom row including go
for i in range(0, 8):
    properties.inorder[i].spots.append(
        (WIDTH - (2 * propwidth) - (i * propwidth) + xshift2, HEIGHT - propheight // 2))
    properties.inorder[i].spots.append(
        (WIDTH - (2 * propwidth) - (i * propwidth) + xshift2, HEIGHT - propheight // 2 + 30))
    properties.inorder[i].spots.append(
        (WIDTH - (2 * propwidth) - (i * propwidth) + xshift1, HEIGHT - propheight // 2))
    properties.inorder[i].spots.append(
        (WIDTH - (2 * propwidth) - (i * propwidth) + xshift1, HEIGHT - propheight // 2 + 30))
    if i != 0 and i != 4:
        properties.inorder[i].price_pos = (WIDTH - (3 * propwidth) // 2 - (i * propwidth), HEIGHT - propheight // 6)
# jail corner
properties.inorder[8].spots.append((WIDTH - (10 * propwidth) - 20, HEIGHT - propheight // 2))
properties.inorder[8].spots.append((WIDTH - (10 * propwidth) - 20 + xshift1, HEIGHT - propheight // 2))
properties.inorder[8].spots.append((WIDTH - (10 * propwidth) - 20, HEIGHT - propheight // 2 + 20))
properties.inorder[8].spots.append((WIDTH - (10 * propwidth) - 20, HEIGHT - propheight // 2 + 20))
# left side including top left corner
inc = 0
for i in range(9, 17):
    properties.inorder[i].spots.append(
        (WIDTH - (10 * propwidth) - 20, HEIGHT - propheight - (inc * propwidth) - xshift1))
    properties.inorder[i].spots.append(
        (WIDTH - (10 * propwidth) + 20, HEIGHT - propheight - (inc * propwidth) - xshift1))
    properties.inorder[i].spots.append(
        (WIDTH - (10 * propwidth) - 20, HEIGHT - propheight - (inc * propwidth) - xshift2))
    properties.inorder[i].spots.append(
        (WIDTH - (10 * propwidth) + 20, HEIGHT - propheight - (inc * propwidth) - xshift2))
    if i != 12 and i != 14 and i != 16:
        properties.inorder[i].price_pos = (WIDTH - (11 * propwidth) + propheight // 2,
                                           HEIGHT - propheight - (inc * propwidth) - propwidth // 4)
    inc += 1
# top side including right corner
inc = 0
for i in range(17, 25):
    properties.inorder[i].spots.append(
        (WIDTH - (9 * propwidth) + (inc * propwidth) + xshift1, HEIGHT - (5 * propheight) - 20))
    properties.inorder[i].spots.append(
        (WIDTH - (9 * propwidth) + (inc * propwidth) + xshift1, HEIGHT - (5 * propheight) + 20))
    properties.inorder[i].spots.append(
        (WIDTH - (9 * propwidth) + (inc * propwidth) + xshift2, HEIGHT - (5 * propheight) - 20))
    properties.inorder[i].spots.append(
        (WIDTH - (9 * propwidth) + (inc * propwidth) + xshift2, HEIGHT - (5 * propheight) + 20))
    if i != 18 and i != 20 and i != 24:
        properties.inorder[i].price_pos = (WIDTH - (9 * propwidth) + (inc * propwidth) + propwidth // 2,
                                           HEIGHT - (5 * propheight) + propheight // 8)
    inc += 1
# right side not including any corners
inc = 0
for i in range(25, 32):
    properties.inorder[i].spots.append(
        (WIDTH - propwidth - 20, propheight + propwidth // 2 + (inc * propwidth) + xshift2))
    properties.inorder[i].spots.append(
        (WIDTH - propwidth + 20, propheight + propwidth // 2 + (inc * propwidth) + xshift2))
    properties.inorder[i].spots.append(
        (WIDTH - propwidth - 20, propheight + propwidth // 2 + (inc * propwidth) - xshift2))
    properties.inorder[i].spots.append(
        (WIDTH - propwidth + 20, propheight + propwidth // 2 + (inc * propwidth) - xshift2))
    if i != 25 and i != 28:
        properties.inorder[i].price_pos = (WIDTH - propheight // 2,
                                           propheight + propwidth // 2 + (inc * propwidth) + propwidth // 3)
    inc += 1


def draw_board(game=None) -> None:
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

    # blit to screen
    screen.blit(background, (0, 0))
    if game:
        for i in range(len(game.propmap.inorder)):
            # draw price and rent on each property
            if properties.inorder[i].price_pos:
                font = pygame.font.Font(None, 36)
                text = font.render(f"{game.propmap.inorder[i].rent}", True, (10, 10, 10))
                textpos = text.get_rect()
                textpos.centerx = properties.inorder[i].price_pos[0]
                textpos.centery = properties.inorder[i].price_pos[1]
                screen.blit(text, textpos)
            locationlvl = game.propmap.inorder[i].level
            if game.propmap.inorder[i].owned is not None and game.propmap.inorder[i].owned > -1:
                color = game.players[game.propmap.inorder[i].owned].color
                # browns
                if 1 <= i <= 3:
                    pygame.draw.rect(screen, color, pygame.Rect(WIDTH - 2 * propwidth - i * propwidth,
                                                                HEIGHT - propheight, propwidth, propheight // 4))
                    screen.blit(lvlimg[locationlvl], (WIDTH - 2 * propwidth - i * propwidth, HEIGHT - propheight))
                # blues
                if 5 <= i <= 7:
                    pygame.draw.rect(screen, color, pygame.Rect(WIDTH - 2 * propwidth - i * propwidth,
                                                                HEIGHT - propheight, propwidth, propheight // 4))
                    screen.blit(lvlimg[locationlvl], (WIDTH - 2 * propwidth - i * propwidth, HEIGHT - propheight))
                # pinks
                if 9 <= i <= 11:
                    pygame.draw.rect(screen, color, pygame.Rect(WIDTH - 9 * propwidth - propheight // 4,
                                                                HEIGHT - propheight - (i - 8) * propwidth,
                                                                propheight // 4, propwidth))
                    screen.blit(lvlimg[locationlvl], (WIDTH - 9 * propwidth - propheight // 4,
                                                     HEIGHT - propheight - (i - 8) * propwidth))
                # oranges
                if i == 13 or i == 15:
                    pygame.draw.rect(screen, color, pygame.Rect(WIDTH - 9 * propwidth - propheight // 4,
                                                                HEIGHT - propheight - (i - 8) * propwidth,
                                                                propheight // 4, propwidth))
                    screen.blit(lvlimg[locationlvl], (WIDTH - 9 * propwidth - propheight // 4,
                                                     HEIGHT - propheight - (i - 8) * propwidth))
                # reds
                if i == 17 or i == 19:
                    pygame.draw.rect(screen, color, pygame.Rect(WIDTH - 9 * propwidth + (i - 17) * propwidth,
                                                                propheight - propheight // 4,
                                                                propwidth, propheight // 4))
                    screen.blit(lvlimg[locationlvl], (WIDTH - 9 * propwidth + (i - 17) * propwidth,
                                                     propheight - propheight // 4))
                # yellows
                if 20 <= i <= 23:
                    pygame.draw.rect(screen, color, pygame.Rect(WIDTH - 9 * propwidth + (i - 17) * propwidth,
                                                                propheight - propheight // 4,
                                                                propwidth, propheight // 4))
                    screen.blit(lvlimg[locationlvl], (WIDTH - 9 * propwidth + (i - 17) * propwidth,
                                                     propheight - propheight // 4))
                # greens and purples
                if i == 26 or i == 27 or i == 29 or i == 31:
                    pygame.draw.rect(screen, color, pygame.Rect(WIDTH - propheight,
                                                                3 * propwidth + (i - 26) * propwidth,
                                                                propheight // 4, propwidth))
                    screen.blit(lvlimg[locationlvl], (WIDTH - propheight,
                                                     3 * propwidth + (i - 26) * propwidth))


def draw_ui(game, myself: Player) -> Player:
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
        if game.started:
            money = str(game.player_money[player.id])
            player_money = base_font.render(f"${money}", True, (255, 255, 255))
            player_moneyrect = player_money.get_rect()
            player_moneyrect.centery = player_moneyrect.height + player_namerect.centery
            screen.blit(player_money, (40, player_moneyrect.centery))
        i += 100

    return myself


def draw_players(game, myself: Player) -> None:
    """
    Draws the players on the board
    """
    global screen
    showroll = False
    if game.started:
        if game.rolling and game.turn == myself.id:
            font = pygame.font.Font(None, 36)
            text = font.render("press space to roll dice", True, (10, 10, 10))
            textpos = text.get_rect()
            textpos.centerx = boardrect.centerx
            textpos.centery = boardrect.centery - 100
            screen.blit(text, textpos)
    for player in game.players:
        if player.rolling and player.showroll and player.id != myself.id:
            showroll = True
            roll_dice()
        elif player.rolling and player.id != myself.id and showroll:
            roll_dice(game.lastroll[0], game.lastroll[1])
            showroll = False
        if player.moving:
            player.nextspot = 0
            for otherplayer in game.players:
                if otherplayer.location == player.nextlocation and otherplayer.id != player.id:
                    player.nextspot = otherplayer.spot + 1
            curr_square = player.location
            next_square = game.goto_next
            lastx = properties.inorder[player.location].spots[player.spot][0]
            lasty = properties.inorder[player.location].spots[player.spot][1]
            finalx = properties.inorder[game.goto_next].spots[player.nextspot][0]
            finaly = properties.inorder[game.goto_next].spots[player.nextspot][1]
            nextxy = player.nextspot
            color = player.color
            readyfornext = True
            move = True
            clock = pygame.time.Clock()
            drawing = True
            while drawing:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                check = (abs(finalx - lastx) < 15) and (abs(finaly - lasty) < 15)
                if curr_square == next_square and check:
                    drawing = False
                else:
                    if readyfornext:
                        move = True
                        readyfornext = False
                        if curr_square == 31:
                            curr_square = 0
                        else:
                            curr_square += 1
                    goto_square = curr_square
                    if move:
                        howclosex = properties.inorder[goto_square].spots[nextxy][0] - lastx
                        howclosey = properties.inorder[goto_square].spots[nextxy][1] - lasty
                        # need to move right
                        if howclosex > 0:
                            x = lastx + 10
                        # need to move left
                        else:
                            x = lastx - 10
                        # need to move up
                        if howclosey < 0:
                            y = lasty - 10

                        # need to move down
                        else:
                            y = lasty + 10
                        if abs(howclosex) < 15 and abs(howclosey) < 15:
                            move = False
                            readyfornext = True
                        else:
                            pygame.draw.circle(screen, color, (x, y), 10)
                            lastx = x
                            lasty = y
                    draw_turn(game, myself)
                    if not player.rolling:
                        roll_dice(game.lastroll[0], game.lastroll[1])
                pygame.display.flip()
                clock.tick(60)
            # note that each client can't actually change instance attributes of other players
            # ths is just used client side to facilitate correct animations
            player.rolling = False
            player.moving = False
            player.location = player.nextlocation
            player.spot = player.nextspot
        else:
            pygame.draw.circle(screen, player.color, properties.inorder[player.location].spots[player.spot], 10)


def draw_turn(game, myself: Player) -> None:
    """
    Buttons on the board to end turn and buy property
    """
    global screen
    buy = button.Button(boardrect.centerx + 160, (9 * propwidth) - 64, buyimg)
    endturn = button.Button(boardrect.centerx - 160, (9 * propwidth) - 64, endturnimg)
    notendturn = button.Button(boardrect.centerx - 160, (9 * propwidth) - 64, notendturnimg)
    lvlup = button.Button(boardrect.centerx + 160, (9 * propwidth) - 64, lvlupimg)

    if game.started:
        font = pygame.font.Font(None, 36)
        text = font.render(f"Turn: {game.players[game.turn].name}", True, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = boardrect.centerx
        textpos.centery = boardrect.centery - 250
        screen.blit(text, textpos)
        if game.turn == myself.id:
            # buy property
            if game.propmap.inorder[myself.location].owned is None:
                if not myself.buy and game.player_money[myself.id] > game.propmap.inorder[myself.location].price:
                    if game.player_money[myself.id] >= game.propmap.inorder[myself.location].price:
                        if myself.location == myself.nextlocation:
                            if buy.draw():
                                myself.buy = True
            # level up property
            elif game.propmap.inorder[myself.location].owned is not None:
                if game.propmap.inorder[myself.location].owned == myself.id and not myself.buy:
                    if not myself.lvld and game.player_money[myself.id] >= game.propmap.inorder[myself.location].price:
                        if myself.location == myself.nextlocation and game.propmap.inorder[myself.location].monopoly:
                            if game.propmap.inorder[myself.location].level <= 5:
                                font = pygame.font.Font(None, 32)
                                lvltext = font.render(
                                    f"for -${game.propmap.inorder[myself.location].price}?", True, (255, 0, 0))
                                lvltextpos = text.get_rect()
                                lvltextpos.centerx = lvlup.rect.centerx
                                lvltextpos.centery = lvlup.rect.centery - 2 * lvltextpos.height
                                screen.blit(lvltext, lvltextpos)
                                if lvlup.draw():
                                    myself.lvlup = True
        # show player transactions
        if game.rent_paid:
            landed_on = game.propmap.inorder[game.goto_next]
            font = pygame.font.Font(None, 64)
            renttext = font.render(
                f"{game.players[game.turn].name}"
                f" paid"
                f" {game.players[landed_on.owned].name}"
                f" ${landed_on.rent}", True, (255, 0, 0))
            renttextpos = text.get_rect()
            renttextpos.centerx = boardrect.centerx - 200
            renttextpos.centery = boardrect.centery - 150
            screen.blit(renttext, renttextpos)
        # show players leveling up properties
        if game.leveled:
            font = pygame.font.Font(None, 32)
            lvltext = font.render(
                f" {game.players[game.turn].name}"
                f" leveled up {game.propmap.inorder[game.goto_next].name}"
                f" to lvl {game.propmap.inorder[game.goto_next].level}"
                f" for ${game.propmap.inorder[game.goto_next].price}", True, (255, 0, 0))
            lvltextpos = text.get_rect()
            lvltextpos.centerx = boardrect.centerx - 200
            lvltextpos.centery = boardrect.centery - 150
            screen.blit(lvltext, lvltextpos)
        # end turn buttons
        if not myself.endturn and myself.location == myself.nextlocation and not myself.rolling:
            if endturn.draw():
                myself.endturn = True
        else:
            if notendturn.draw():
                pass


def roll_dice(x: int = -1, y: int = -1) -> None:
    """
    Draws the dice
    """
    global screen
    if x == -1:
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
    else:
        dice1 = faces[x]
        dice2 = faces[y]
        dice1rect = dice1.get_rect()
        dice1rect.centerx = boardrect.centerx - 25
        dice1rect.centery = boardrect.centery

        dice2rect = dice2.get_rect()
        dice2rect.centerx = boardrect.centerx + 25
        dice2rect.centery = boardrect.centery

        screen.blit(dice1, dice1rect)
        screen.blit(dice2, dice2rect)


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
    left_button = button.Button(WIDTH // 2 - 250, HEIGHT // 2, faces[choice], 1)
    right_button = button.Button(WIDTH // 2 + 250, HEIGHT // 2, faces[choice + 1], 1)
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
        screen.blit(color_text_surface, (WIDTH // 2 - color_text_surface.get_width() // 2, HEIGHT // 2 - 100))
        pygame.draw.circle(screen, color_choices[choice], (WIDTH // 2, HEIGHT // 2), 50)

        # enter name
        pygame.draw.rect(screen, color, input_rect)
        user_text_surface = base_font.render(user_text, True, (255, 255, 255))
        name_text_surface = base_font.render("Enter your name:", True, (255, 255, 255))
        screen.blit(user_text_surface, (input_rect.x + 5, input_rect.y + 5))
        screen.blit(name_text_surface, (input_rect.x, input_rect.y - name_text_surface.get_height()))
        input_rect.w = max(100, user_text_surface.get_width() + 10)

        pygame.display.flip()
        clock.tick(60)
    me = Player(playernum)
    me.name = user_text
    me.color = color_choices[choice]
    me.location = 0
    me.spot = me.id
    print(f"my id is {me.id}")
    return me


def settings_menu() -> None:
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
        clock.tick(60)


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
                if myself.rolling:
                    if event.key == pygame.K_SPACE and not roll:
                        roll = True
                        myself.showroll = True
                        stop_roll = False
                    elif event.key == pygame.K_SPACE and roll:
                        stop_roll = True
            if event.type == pygame.QUIT:
                run = False

        # drawing to screen
        draw_board(game)
        myself = draw_ui(game, myself)
        draw_players(game, myself)
        draw_turn(game, myself)
        if roll:
            if stop_roll:
                roll = False
                myself.rolling = False
                myself.showroll = False
                roll_dice(game.lastroll[0], game.lastroll[1])
                myself.moving = True
            else:
                roll_dice()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
