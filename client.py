# kyles online multiplayer board game client script
# written by Kyle Vickstrom
# vickskyl@oregonstate.edu
# https://github.com/kevickstrom/monopoly_butonlykylecancheat

# TODO: doubles
# TODO: jail
# TODO: tuition due
# TODO: corners
# TODO: starships
# TODO: ending / winning / losing sequence
# TODO: endgame statistics

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
pygame.display.set_caption("kyles online multiplayer board game")
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
logoimg = pygame.image.load(os.path.join('assets', "logo.png"))
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
sellimg = pygame.image.load(os.path.join('assets', "sell.png"))
almostlose_sellimg = pygame.image.load(os.path.join('assets', "almostlose_sell.png"))
notsellimg = pygame.image.load(os.path.join('assets', "notsell.png"))
leveldownimg = pygame.image.load(os.path.join('assets', "leveldown.png"))
notleveldownimg = pygame.image.load(os.path.join('assets', "notleveldown.png"))
mortgageimg = pygame.image.load(os.path.join('assets', "mortgage.png"))
notmortgageimg = pygame.image.load(os.path.join('assets', "notmortgage.png"))
confirmimg = pygame.image.load(os.path.join('assets', "confirm.png"))
cancelimg = pygame.image.load(os.path.join('assets', "cancel.png"))
notcancelimg = pygame.image.load(os.path.join('assets', "notcancel.png"))
auctionimg = pygame.image.load(os.path.join('assets', "auction.png"))
notauctionimg = pygame.image.load(os.path.join('assets', "notauction.png"))
selectimg = pygame.image.load(os.path.join('assets', "select.png"))
selectedimg = pygame.image.load(os.path.join('assets', "selected.png"))
notselectimg = pygame.image.load(os.path.join('assets', "notselect.png"))

# almostlose background
almostloseimg = pygame.image.load(os.path.join('assets', "almostlose.png"))
almostloseimg = pygame.transform.smoothscale(almostloseimg, (HEIGHT, HEIGHT))

# property level images
lvlimg = [pygame.image.load(os.path.join('assets', "lvl0.png")), pygame.image.load(os.path.join('assets', "lvl1.png")),
          pygame.image.load(os.path.join('assets', "lvl2.png")), pygame.image.load(os.path.join('assets', "lvl3.png")),
          pygame.image.load(os.path.join('assets', "lvl4.png")), pygame.image.load(os.path.join('assets', "lvl5.png"))]
for i in range(len(lvlimg)):
    lvlimg[i] = pygame.transform.smoothscale(lvlimg[i], ((boardrect.width // 11) // 4, (boardrect.width // 11) // 4))

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
    elif i == 4:
        properties.inorder[i].price_pos = (WIDTH - (3 * propwidth) // 2 - (i * propwidth), HEIGHT - propheight // 15)

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
    # bus 2
    if i == 14:
        properties.inorder[i].price_pos = (WIDTH - (11 * propwidth) + 30,
                                           HEIGHT - propheight - (inc * propwidth) - (13 * propwidth) // 16)
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
    # bus 3
    elif i == 18:
        properties.inorder[i].price_pos = (WIDTH - (9 * propwidth) + (inc * propwidth) + propwidth // 2,
                                           HEIGHT - (5 * propheight) + propheight // 2 - 15)
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
    elif i == 25:
        properties.inorder[i].price_pos = (WIDTH - 30,
                                           propheight + propwidth // 6)

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
                # bus 1
                elif i == 4:
                    # bottom line
                    pygame.draw.line(screen, color, (WIDTH - 5 * propwidth, HEIGHT),
                                     (WIDTH - 6 * propwidth, HEIGHT), 10)
                    # left line
                    pygame.draw.line(screen, color, (WIDTH - 6 * propwidth, HEIGHT),
                                     (WIDTH - 6 * propwidth, HEIGHT - propheight - 2), 10)
                    # top line
                    pygame.draw.line(screen, color, (WIDTH - 6 * propwidth, HEIGHT - propheight),
                                     (WIDTH - 5 * propwidth, HEIGHT - propheight), 10)
                    # right line
                    pygame.draw.line(screen, color, (WIDTH - 5 * propwidth, HEIGHT - propheight - 2),
                                     (WIDTH - 5 * propwidth, HEIGHT), 10)
                # blues
                elif 5 <= i <= 7:
                    pygame.draw.rect(screen, color, pygame.Rect(WIDTH - 2 * propwidth - i * propwidth,
                                                                HEIGHT - propheight, propwidth, propheight // 4))
                    screen.blit(lvlimg[locationlvl], (WIDTH - 2 * propwidth - i * propwidth, HEIGHT - propheight))
                # pinks
                elif 9 <= i <= 11:
                    pygame.draw.rect(screen, color, pygame.Rect(WIDTH - 9 * propwidth - propheight // 4,
                                                                HEIGHT - propheight - (i - 8) * propwidth,
                                                                propheight // 4, propwidth))
                    screen.blit(lvlimg[locationlvl], (WIDTH - 9 * propwidth - propheight // 4,
                                                      HEIGHT - propheight - (i - 8) * propwidth))
                # oranges
                elif i == 13 or i == 15:
                    pygame.draw.rect(screen, color, pygame.Rect(WIDTH - 9 * propwidth - propheight // 4,
                                                                HEIGHT - propheight - (i - 8) * propwidth,
                                                                propheight // 4, propwidth))
                    screen.blit(lvlimg[locationlvl], (WIDTH - 9 * propwidth - propheight // 4,
                                                      HEIGHT - propheight - (i - 8) * propwidth))
                # bus 2
                elif i == 14:
                    # bottom line
                    pygame.draw.line(screen, color, (WIDTH - boardrect.width + propheight, HEIGHT - 7 * propwidth),
                                     (WIDTH - boardrect.width, HEIGHT - 7 * propwidth), 10)
                    # left line
                    pygame.draw.line(screen, color, (WIDTH - boardrect.width, HEIGHT - 7 * propwidth),
                                     (WIDTH - boardrect.width, HEIGHT - 8 * propwidth), 10)
                    # top line
                    pygame.draw.line(screen, color, (WIDTH - boardrect.width, HEIGHT - 8 * propwidth),
                                     (WIDTH - boardrect.width + propheight, HEIGHT - 8 * propwidth), 10)
                    # right line
                    pygame.draw.line(screen, color, (WIDTH - boardrect.width + propheight, HEIGHT - 8 * propwidth),
                                     (WIDTH - boardrect.width + propheight, HEIGHT - 7 * propwidth), 10)
                # reds
                elif i == 17 or i == 19:
                    pygame.draw.rect(screen, color, pygame.Rect(WIDTH - 9 * propwidth + (i - 17) * propwidth,
                                                                propheight - propheight // 4,
                                                                propwidth, propheight // 4))
                    screen.blit(lvlimg[locationlvl], (WIDTH - 9 * propwidth + (i - 17) * propwidth,
                                                      propheight - propheight // 4))
                # bus 3
                elif i == 18:
                    # bottom line
                    pygame.draw.line(screen, color, (WIDTH - boardrect.width + 4 * propwidth,
                                                     HEIGHT - boardrect.height + propheight),
                                     (WIDTH - boardrect.width + 3 * propwidth,
                                      HEIGHT - boardrect.height + propheight), 10)
                    # left line
                    pygame.draw.line(screen, color,
                                     (WIDTH - boardrect.width + 3 * propwidth, HEIGHT - boardrect.height + propheight),
                                     (WIDTH - boardrect.width + 3 * propwidth, HEIGHT - boardrect.height), 10)
                    # top line
                    pygame.draw.line(screen, color,
                                     (WIDTH - boardrect.width + 3 * propwidth, HEIGHT - boardrect.height),
                                     (WIDTH - boardrect.width + 4 * propwidth, HEIGHT - boardrect.height), 10)
                    # right line
                    pygame.draw.line(screen, color,
                                     (WIDTH - boardrect.width + 4 * propwidth, HEIGHT - boardrect.height),
                                     (WIDTH - boardrect.width + 4 * propwidth, HEIGHT - boardrect.height + propheight),
                                     10)
                # yellows
                elif 20 <= i <= 23:
                    pygame.draw.rect(screen, color, pygame.Rect(WIDTH - 9 * propwidth + (i - 17) * propwidth,
                                                                propheight - propheight // 4,
                                                                propwidth, propheight // 4))
                    screen.blit(lvlimg[locationlvl], (WIDTH - 9 * propwidth + (i - 17) * propwidth,
                                                      propheight - propheight // 4))
                # bus 4
                elif i == 25:
                    # bottom line
                    pygame.draw.line(screen, color, (WIDTH, HEIGHT - boardrect.height + propheight + propwidth),
                                     (WIDTH - propheight, HEIGHT - boardrect.height + propheight + propwidth), 10)
                    # left line
                    pygame.draw.line(screen, color,
                                     (WIDTH - propheight, HEIGHT - boardrect.height + propheight + propwidth),
                                     (WIDTH - propheight, HEIGHT - boardrect.height + propheight), 10)
                    # top line
                    pygame.draw.line(screen, color, (WIDTH - propheight, HEIGHT - boardrect.height + propheight),
                                     (WIDTH, HEIGHT - boardrect.height + propheight), 10)
                    # right line
                    pygame.draw.line(screen, color, (WIDTH, HEIGHT - boardrect.height + propheight),
                                     (WIDTH, HEIGHT - boardrect.height + propheight + propwidth), 10)
                # greens and purples
                elif i == 26 or i == 27 or i == 29 or i == 31:
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
        pygame.draw.circle(screen, player.color, (WIDTH - boardrect.width - 20, i + 50), 10)

        # blit name
        player_name = base_font.render(player.name, True, (255, 255, 255))
        player_namerect = player_name.get_rect()
        player_namerect.centery = i + 50
        player_namewidth = player_namerect.width
        screen.blit(player_name, (WIDTH - boardrect.width - player_namewidth - 40, player_namerect.centery))

        # blit money
        if game.started:
            money = str(game.player_money[player.id])
            player_money = base_font.render(f"${money}", True, (255, 255, 255))
            player_moneyrect = player_money.get_rect()
            player_moneyrect.centery = player_moneyrect.height + player_namerect.centery
            moneywidth = player_moneyrect.width
            screen.blit(player_money,
                        (WIDTH - boardrect.width - player_namewidth - moneywidth - 40, player_moneyrect.centery))
        i += 100

    return myself


def draw_players(game, myself: Player) -> None:
    """
    Draws the players on the board and their movement animations
    """
    if game.started:
        player = game.players[game.turn]
        if game.turn == myself.id and not myself.rolled:
            myself.rolling = True

        if myself.rolling and player.id == myself.id:
            font = pygame.font.Font(None, 36)
            text = font.render("press space to roll dice", True, (10, 10, 10))
            textpos = text.get_rect()
            textpos.centerx = boardrect.centerx
            textpos.centery = boardrect.centery - 100
            screen.blit(text, textpos)
        if player.rolling and player.showroll:
            roll_dice()
            myself.showmoving = True
        elif player.rolled:
            roll_dice(game.lastroll[0], game.lastroll[1])
        if player.moving and myself.showmoving:
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
                pygame.display.flip()
                clock.tick(60)
            # note that each client can't actually change instance attributes of other players
            # ths is just used client side to facilitate correct animations
            player.rolling = False
            player.rolled = True
            player.moving = False
            myself.showmoving = False
            player.nextlocation = game.goto_next
            player.location = player.nextlocation
            player.spot = player.nextspot
        else:
            for player in game.players:
                if not player.lost:
                    pygame.draw.circle(screen, (0, 0, 0), properties.inorder[player.location].spots[player.spot], 12)
                    pygame.draw.circle(screen, player.color, properties.inorder[player.location].spots[player.spot], 10)


def draw_turn(game, myself: Player) -> None:
    """
    Buttons on the board to end turn and buy / sell property
    Also displays transaction texts
    """
    buy = button.Button(boardrect.centerx + 160, (9 * propwidth) - 64, buyimg)
    endturn = button.Button(boardrect.centerx - 160, (9 * propwidth) - 64, endturnimg)
    notendturn = button.Button(boardrect.centerx - 160, (9 * propwidth) - 64, notendturnimg)
    lvlup = button.Button(boardrect.centerx + 160, (9 * propwidth) - 64, lvlupimg)
    sell = button.Button(boardrect.centerx, (9 * propwidth) - 64, sellimg)
    auction = button.Button(boardrect.centerx - 160, (9 * propwidth) - 135, auctionimg)
    notauction = button.Button(boardrect.centerx - 160, (9 * propwidth) - 135, notauctionimg)

    if game.started:
        # display who's turn it is
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
            # level up / sell property
            elif game.propmap.inorder[myself.location].owned is not None:
                if game.propmap.inorder[myself.location].owned == myself.id and not myself.buy:
                    if not myself.lvld and game.player_money[myself.id] >= game.propmap.inorder[myself.location].price:
                        if myself.location == myself.nextlocation and game.propmap.inorder[myself.location].monopoly:
                            if game.propmap.inorder[myself.location].level < 5:
                                font = pygame.font.Font(None, 32)
                                lvltext = font.render(
                                    f"for ${game.propmap.inorder[myself.location].price}?", True, (255, 0, 0))
                                lvltextpos = text.get_rect()
                                lvltextpos.centerx = lvlup.rect.centerx
                                lvltextpos.centery = lvlup.rect.centery - 2 * lvltextpos.height
                                screen.blit(lvltext, lvltextpos)
                                if lvlup.draw():
                                    myself.lvlup = True
                    if not myself.sell and not myself.sold and myself.location == myself.nextlocation:
                        if sell.draw():
                            myself.sell = True
        # show player to player transactions
        if game.rent_paid and not game.players[game.turn].rolling:
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
        # show other players leveling up properties
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
        # end turn buttons and auction
        rolled = not myself.endturn and myself.location == myself.nextlocation and not myself.rolling
        eligible = not myself.lost and not game.aucstart
        if rolled and eligible:
            if myself.auction is not True:
                if endturn.draw():
                    myself.endturn = True
                    myself.showroll = False
                # auction
                if not game.auctioned:
                    if auction.draw():
                        myself.auction = True
        else:
            if notendturn.draw():
                pass
            if notauction.draw():
                pass


def draw_almostlose(game, myself, events) -> None:
    """
    Draws the selling / mortgage property tab because you almost lost
    TODO: make more like auction menu
    """
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                myself.aly = min(myself.aly + 15, 0)
            if event.button == 5:
                myself.aly = max(myself.aly - 15, -1 * HEIGHT // 2)
    menuwid = WIDTH - boardrect.width
    almostlose = pygame.surface.Surface((menuwid, HEIGHT * 2))
    # almostlosebckgrnd = button.Button(WIDTH // 2, HEIGHT // 2, almostloseimg)
    # almostlosebckgrnd.draw()
    confirmbutton = button.Button(menuwid//2 + 64, 32, confirmimg)
    cancelbutton = button.Button(menuwid//2 - 64, 32, cancelimg)
    font = pygame.font.Font(None, 32)
    headerfont = pygame.font.Font(None, 64)
    header = headerfont.render("Wow! You almost lost...", True, (255, 255, 255))
    headerpos = header.get_rect()
    headerpos.centerx = menuwid // 2
    headerpos.centery = propwidth
    almostlose.blit(header, headerpos)
    footer = pygame.surface.Surface((menuwid, 64))
    footer.fill((15, 0, 0))
    # # used to tally all sold / level down $$$ to make sure it pays off debt
    networth = 0
    # find all owned properties
    myprops = []
    for props in game.propmap.inorder:
        if props.owned == myself.id:
            myprops.append(props)
    # list all properties and their level
    for i in range(len(myprops)):
        owned_prop = font.render(f"{myprops[i].name}    lvl:{myprops[i].level}", True,
                                 game.propmap.colors[myprops[i].color])
        owned_prop_pos = owned_prop.get_rect()
        owned_prop_pos.x = 10
        owned_prop_pos.centery = (2 * propwidth) + i * (propwidth // 2)

        # list the price they will sell for
        sellprice = font.render(f"+${myprops[i].price * (myprops[i].level + 1)}", True, (60, 179, 113))
        sellprice_pos = sellprice.get_rect()
        sellprice_pos.centerx = menuwid // 2 + 32
        sellprice_pos.centery = (2 * propwidth) + i * (propwidth // 2)

        almostlose.blit(owned_prop, owned_prop_pos)
        almostlose.blit(sellprice, sellprice_pos)
        # list the price for one level down if applicable
        # show the leveling down button

        if myprops[i].id in myself.leveldown.keys():
            # show button if we can still level down
            if myprops[i].level - myself.leveldown[myprops[i].id] > 1:
                lvldownbutton = button.Button(menuwid // 2 - 64, (2 * propwidth) + i * (propwidth // 2), leveldownimg)
                lvldownprice = font.render(f"+${myprops[i].price}", True, (60, 179, 113))
                lvldownprice_pos = lvldownprice.get_rect()
                lvldownprice_pos.x = menuwid // 2 - 64 - 2 * lvldownprice_pos.width
                lvldownprice_pos.centery = (2 * propwidth) + i * (propwidth // 2)

                almostlose.blit(lvldownprice, lvldownprice_pos)
                if lvldownbutton.blit(almostlose):
                    myself.leveldown[myprops[i].id] = myself.leveldown[myprops[i].id] + 1
                    time.sleep(0.2)
            # show how many levels to drop
            lvls = font.render(f"-{myself.leveldown[myprops[i].id]} lvls", True, (60, 179, 113))
            lvls_pos = lvls.get_rect()
            lvls_pos.centerx = menuwid - (3 * lvls.get_width())
            lvls_pos.centery = (2 * propwidth) + i * (propwidth // 2)
            almostlose.blit(lvls, lvls_pos)
            # show $$$ from leveling down on the right side
            addprice = font.render(f"+${myprops[i].price * myself.leveldown[myprops[i].id]}", True, (60, 179, 113))
            newpos = addprice.get_rect()
            newpos.centerx = menuwid - addprice.get_width()
            newpos.centery = (2 * propwidth) + i * (propwidth // 2)

            almostlose.blit(addprice, newpos)
            # tally $$$
            networth += myprops[i].price * myself.leveldown[myprops[i].id]

        elif myprops[i].level > 1:
            # show level down button
            lvldownbutton = button.Button(menuwid // 2 - 64, (2 * propwidth) + i * (propwidth // 2), leveldownimg)
            lvldownprice = font.render(f"+${myprops[i].price}", True, (60, 179, 113))
            lvldownprice_pos = lvldownprice.get_rect()
            lvldownprice_pos.x = menuwid // 2 - 64 - 2 * lvldownprice_pos.width
            lvldownprice_pos.centery = (2 * propwidth) + i * (propwidth // 2)
            almostlose.blit(lvldownprice, lvldownprice_pos)
            if lvldownbutton.blit(almostlose, myself.aly):
                myself.leveldown[myprops[i].id] = 1
                if myprops[i].id in myself.sell:
                    myself.sell.remove(myprops[i].id)
                time.sleep(0.2)

        else:
            # show the grayed out button
            notlvldownbutton = button.Button(menuwid // 2 - 64, (2 * propwidth) + i * (propwidth // 2),
                                             notleveldownimg)
            if notlvldownbutton.blit(almostlose):
                pass
        # check if current items are enough to remain in the game
        # show grayed sell button
        if myprops[i].id in myself.tosell:
            notsellbutton = button.Button(menuwid // 2 + 128, (2 * propwidth) + i * (propwidth // 2), notsellimg)
            if notsellbutton.blit(almostlose):
                pass
            addprice = font.render(f"+${myprops[i].price * (myprops[i].level + 1)}", True, (60, 179, 113))
            newpos = addprice.get_rect()
            newpos.centerx = menuwid - addprice.get_width()
            newpos.centery = (2 * propwidth) + i * (propwidth // 2)

            almostlose.blit(addprice, newpos)
            networth += myprops[i].price * (myprops[i].level + 1)
        else:
            # show sell button
            sellbutton = button.Button(menuwid // 2 + 128, (2 * propwidth) + i * (propwidth // 2), almostlose_sellimg)
            if sellbutton.blit(almostlose, myself.aly):
                myself.tosell.append(myprops[i].id)
                if myprops[i].id in myself.leveldown.keys():
                    myself.leveldown.__delitem__(myprops[i].id)
        # if $ is enough show total in green ( $ > 0 )
    if game.player_money[myself.id] + networth > 0:
        newtotal = font.render(f"New Total: ${game.player_money[myself.id] + networth}", True, (60, 179, 113))
        # allow player to confirm
        if confirmbutton.blit(footer, HEIGHT - 64):
            myself.confirm = True
    else:
        # show total in red ( < $0 )
        newtotal = font.render(f"New Total: ${game.player_money[myself.id] + networth}", True, (255, 0, 0))
    newtotalpos = newtotal.get_rect()
    newtotalpos.centerx = menuwid - newtotal.get_width()
    newtotalpos.centery = 32

    footer.blit(newtotal, newtotalpos)

    # restart selling / leveling down
    if cancelbutton.blit(footer, HEIGHT - 64):
        myself.tosell = []
        myself.leveldown = {}
    screen.blit(almostlose, (0, myself.aly))
    screen.blit(footer, (0, HEIGHT - 64))


def draw_auction(game, myself: Player, events) -> None:
    """
    Auction property select menu with scrolling
    Sets myself.auction to the id of the prop
    """
    # buttons
    confirmbutton = button.Button((WIDTH - boardrect.width)//2 + 64, HEIGHT - 32, confirmimg)
    cancelbutton = button.Button((WIDTH - boardrect.width)//2 - 64, HEIGHT - 32, cancelimg)
    exitbutton = button.Button((WIDTH - boardrect.width)//2 - 64, HEIGHT - 32, exitimg)
    font = pygame.font.Font(None, 32)
    headerfont = pygame.font.Font(None, 64)
    header = headerfont.render("Select the property to auction:", True, (255, 255, 255))
    headerpos = header.get_rect()
    headerpos.centerx = (WIDTH - boardrect.width)//2
    headerpos.centery = propwidth
    # check for scrolling
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                myself.aucy = min(myself.aucy + 15, 0)
            if event.button == 5:
                myself.aucy = max(myself.aucy - 15, -1*HEIGHT//2)
    # create background surface
    aucmenu = pygame.surface.Surface((WIDTH - boardrect.width, HEIGHT * 2))
    aucmenu.blit(header, headerpos)
    # draw properties with selection buttons on the menu
    i = 0
    for prop in game.propmap.inorder:
        if prop.owned == myself.id:
            # text
            owned_prop = font.render(f"{prop.name}    lvl:{prop.level}", True, game.propmap.colors[prop.color])
            if prop.level == 0:
                info = font.render(f"price: {prop.price}    invested: ${prop.price}", True, (40, 180, 99))
            else:
                info = font.render(f"price: ${prop.price}    invested: ${prop.price * prop.level}", True,
                                   (40, 180, 99))
            owned_prop_pos = owned_prop.get_rect()
            owned_prop_pos.x = 10
            owned_prop_pos.centery = (2 * propwidth) + i * (propwidth // 2)
            info_pos = info.get_rect()
            info_pos.x = owned_prop_pos.x + owned_prop_pos.width + 10
            info_pos.centery = (2 * propwidth) + i * (propwidth // 2)

            # selection buttons
            selectbutton = button.Button((WIDTH - boardrect.width) - 150, (2 * propwidth) + i * (propwidth // 2),
                                         selectimg)
            selectedbutton = button.Button((WIDTH - boardrect.width) - 150, (2 * propwidth) + i * (propwidth // 2),
                                           selectedimg)
            notselectbutton = button.Button((WIDTH - boardrect.width) - 150, (2 * propwidth) + i * (propwidth // 2),
                                            notselectimg)

            if myself.aucselect is None:
                if selectbutton.blit(aucmenu, myself.aucy) and (time.process_time() - myself.timer) > 0.15:
                    myself.aucselect = prop.id
                    myself.timer = time.process_time()
            elif myself.aucselect == prop.id:
                if selectedbutton.blit(aucmenu, myself.aucy) and (time.process_time() - myself.timer) > 0.15:
                    myself.aucselect = None
                    myself.timer = time.process_time()
            else:
                if notselectbutton.blit(aucmenu, myself.aucy):
                    pass

            aucmenu.blit(owned_prop, owned_prop_pos)
            aucmenu.blit(info, info_pos)
            i += 1
    # blit the menu and control buttons
    screen.blit(aucmenu, (0, myself.aucy))
    pygame.draw.rect(screen, (15, 0, 0), pygame.Rect(0, HEIGHT - 64, WIDTH - boardrect.width, 64))
    # if exitbutton.draw():
    #     myself.auction = False
    #     myself.aucselect = None
    if cancelbutton.draw():
        myself.auction = False
        myself.aucselect = None
    if myself.aucselect is not None:
        if confirmbutton.draw():
            myself.auction = False
            myself.aucstart = True
            # for testing
            myself.bid = ["", "", ""]


def draw_auction_prop(game, myself: Player, propid: int, events):
    """
    Draws and handles property auctions
    TODO: fix default value "" and "0"
    """
    confirmbutton = button.Button(200 + 64, HEIGHT - 200 + 64, confirmimg)
    menuwid = WIDTH - boardrect.width
    aucmenu = pygame.surface.Surface((menuwid, HEIGHT))
    headerfont = pygame.font.Font(None, 48)
    if game.aucstart and not myself.aucstart and game.auctioned:
        myself.bid = ["", "", ""]  # blank for each round to fill out bid
        myself.aucstart = True
        print("auc started")
    if myself.aucround != game.aucround:
        myself.confirm = False
        myself.aucround = game.aucround
    roundtime = round(30 - (time.time() - game.timer), 1)

    # headers
    forsale_obj = game.propmap.inorder[propid]
    forsale = headerfont.render(f"{forsale_obj.name}", True, game.propmap.colors[forsale_obj.color])
    forsalepos = forsale.get_rect()
    forsalepos.centerx = menuwid // 2
    forsalepos.centery = propwidth // 2
    aucmenu.blit(forsale, forsalepos)
    if game.aucround == 3:
        header = headerfont.render(f"Auction Time Left: {round(roundtime - 20, 1)}", True, (255, 255, 255))
    elif roundtime > 0:
        header = headerfont.render(f"Auction Time Left: {roundtime}", True, (255, 255, 255))
    else:
        header = headerfont.render(f"Auction Time Left: 0", True, (255, 255, 255))
    headerpos = header.get_rect()
    headerpos.centerx = (WIDTH - boardrect.width) // 2
    headerpos.centery = propwidth

    tablewid = (3*menuwid)//4
    tableleft = menuwid//4
    tableheader1 = headerfont.render(f"R1", True, (255, 255, 255))
    tableheader2 = headerfont.render(f"R2", True, (255, 255, 255))
    tableheader3 = headerfont.render(f"R3", True, (255, 255, 255))

    tableheader1pos = tableheader1.get_rect()
    tableheader1pos.centery = 150
    tableheader1pos.centerx = tableleft

    tableheader2pos = tableheader2.get_rect()
    tableheader2pos.centery = 150
    tableheader2pos.centerx = 2 * tableleft

    tableheader3pos = tableheader3.get_rect()
    tableheader3pos.centery = 150
    tableheader3pos.centerx = 3 * tableleft

    aucmenu.blit(tableheader1, tableheader1pos)
    aucmenu.blit(tableheader2, tableheader2pos)
    aucmenu.blit(tableheader3, tableheader3pos)

    i = 150
    for player in game.players:

        # blit color
        pygame.draw.circle(aucmenu, player.color, (10, i + 50), 10)

        # blit name
        player_name = base_font.render(player.name, True, (255, 255, 255))
        player_namerect = player_name.get_rect()
        player_namerect.centery = i + 50
        player_namewidth = player_namerect.width
        aucmenu.blit(player_name, (20, player_namerect.centery))

        # blit money
        money = str(game.player_money[player.id])
        player_money = base_font.render(f"${money}", True, (255, 255, 255))
        player_moneyrect = player_money.get_rect()
        player_moneyrect.centery = player_moneyrect.height + player_namerect.centery
        moneywidth = player_moneyrect.width
        aucmenu.blit(player_money, (20, player_moneyrect.centery))

        # blit betting
        if game.aucround > 0:
            bid1 = player.bid[0]
            if int(bid1) == game.highbid:
                bidcolor = (30, 132, 73)
            else:
                bidcolor = (255, 255, 255)
            player_bid = base_font.render(f"${bid1}", True, bidcolor)
            player_bidrect = player_bid.get_rect()
            player_bidrect.centerx = tableleft
            player_bidrect.centery = player_bidrect.height + player_namerect.centery
            aucmenu.blit(player_bid, player_bidrect)

            if game.aucround > 1:
                bid2 = player.bid[1]
                if int(bid2) == game.highbid:
                    bidcolor = (30, 132, 73)
                else:
                    bidcolor = (255, 255, 255)
                player_bid = base_font.render(f"${bid2}", True, bidcolor)
                player_bidrect = player_bid.get_rect()
                player_bidrect.centerx = 2*tableleft
                player_bidrect.centery = player_bidrect.height + player_namerect.centery
                aucmenu.blit(player_bid, player_bidrect)

            if game.aucround > 2:
                bid3 = player.bid[2]
                if int(bid3) == game.highbid:
                    bidcolor = (30, 132, 73)
                else:
                    bidcolor = (255, 255, 255)
                player_bid = base_font.render(f"${bid3}", True, bidcolor)
                player_bidrect = player_bid.get_rect()
                player_bidrect.centerx = 3*tableleft
                player_bidrect.centery = player_bidrect.height + player_namerect.centery
                aucmenu.blit(player_bid, player_bidrect)
        i += 100

    # if game.turn != myself.id:
    input_rect = pygame.Rect(200, HEIGHT - 200, 140, 32)

    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('grey')

    allowconfirm = True
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                myself.menucolor = 1
            else:
                myself.menucolor = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and not myself.confirm:
                myself.bid[game.aucround] = myself.bid[game.aucround][:-1]
            elif event.key == pygame.K_RETURN and allowconfirm:
                myself.confirm = True
            if not myself.confirm:
                # input can only be number
                # this is not ideal right now but it works
                if event.key == pygame.K_0:
                    myself.bid[game.aucround] += "0"
                elif event.key == pygame.K_1:
                    myself.bid[game.aucround] += "1"
                elif event.key == pygame.K_2:
                    myself.bid[game.aucround] += "2"
                elif event.key == pygame.K_3:
                    myself.bid[game.aucround] += "3"
                elif event.key == pygame.K_4:
                    myself.bid[game.aucround] += "4"
                elif event.key == pygame.K_5:
                    myself.bid[game.aucround] += "5"
                elif event.key == pygame.K_6:
                    myself.bid[game.aucround] += "6"
                elif event.key == pygame.K_7:
                    myself.bid[game.aucround] += "7"
                elif event.key == pygame.K_8:
                    myself.bid[game.aucround] += "8"
                elif event.key == pygame.K_9:
                    myself.bid[game.aucround] += "9"

    if myself.menucolor == 1:
        color = color_active
    else:
        color = color_passive
    if game.aucround < 3:
        try:
            if int(myself.bid[game.aucround]) > game.player_money[myself.id]:
                bidcolor = (231, 76, 60)
                allowconfirm = False
            else:
                bidcolor = (30, 132, 73)
        except ValueError:
            bidcolor = (30, 132, 73)

        if allowconfirm and not myself.confirm:
            if confirmbutton.blit(aucmenu):
                myself.confirm = True

        user_text_surface = base_font.render(myself.bid[game.aucround], True, bidcolor)
        dolla = base_font.render("$", True, bidcolor)
        name_text_surface = base_font.render("Enter your bid:", True, bidcolor)
        input_rect.w = max(100, user_text_surface.get_width() + 15)
        pygame.draw.rect(aucmenu, color, input_rect)
        aucmenu.blit(dolla, (input_rect.x, input_rect.y + 5))
        aucmenu.blit(user_text_surface, (input_rect.x + 15, input_rect.y + 5))
        aucmenu.blit(name_text_surface, (input_rect.x, input_rect.y - name_text_surface.get_height()))
    if myself.confirm:
        if myself.bid[game.aucround] == "" or not allowconfirm:
            myself.bid[game.aucround] = "1"

    aucmenu.blit(header, headerpos)
    screen.blit(aucmenu, (0, 0))


def roll_dice(x: int = -1, y: int = -1) -> None:
    """
    Draws the dice. Final faces (roll) are controlled server side
    """
    global screen
    # show random faces
    if x == -1:
        num1 = random.randrange(0, 6)
        dice1 = faces[num1]
        num2 = random.randrange(0, 6)
        dice2 = faces[num2]
    # show final faces
    else:
        dice1 = faces[x]
        dice2 = faces[y]

    dice1rect = dice1.get_rect()
    dice1rect.centerx = boardrect.centerx - 25
    dice1rect.centery = boardrect.centery
    screen.blit(dice1, dice1rect)

    dice2rect = dice2.get_rect()
    dice2rect.centerx = boardrect.centerx + 25
    dice2rect.centery = boardrect.centery
    screen.blit(dice2, dice2rect)


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

        logorect = logoimg.get_rect()
        logorect.centerx = WIDTH // 2
        logorect.centery = HEIGHT // 4
        screen.blit(logoimg, logorect)
        pygame.display.flip()
        clock.tick(60)


def draw_start_menu(game, myself: Player, events) -> bool:
    """
    Starting menu when the game is launched
    initializes and returns player - name, color
    """
    input_rect = pygame.Rect(200, 200, 140, 32)

    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('grey')

    color_choices = game.color_pick
    choice = myself.color
    if choice > len(color_choices) - 1:
        choice = len(color_choices) - 1
    if choice > 0:
        left_button = button.Button(WIDTH // 2 - 250, HEIGHT // 2, faces[choice - 1], 1)
    else:
        left_button = button.Button(WIDTH // 2 - 250, HEIGHT // 2, faces[choice], 1)
    if choice < 5:
        right_button = button.Button(WIDTH // 2 + 250, HEIGHT // 2, faces[choice + 1], 1)
    else:
        right_button = button.Button(WIDTH // 2 + 250, HEIGHT // 2, faces[choice], 1)

    menu = True
    # event handling
    for event in events:
        pass
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                myself.menucolor = 1
            else:
                myself.menucolor = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                myself.name = myself.name[:-1]
            elif event.key == pygame.K_RETURN:
                menu = False
            else:
                myself.name += event.unicode

        # color the screen and blit
        screen.fill((52, 78, 91))
        if myself.menucolor == 1:
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
        if choice < len(color_choices) - 1:
            if right_button.draw():
                choice += 1
                left_button.image = faces[choice - 1]
                if choice < len(color_choices) - 1:
                    right_button.image = faces[choice + 1]
                time.sleep(0.2)
        color_text_surface = base_font.render("Choose a color:", True, (255, 255, 255))
        screen.blit(color_text_surface, (WIDTH // 2 - color_text_surface.get_width() // 2, HEIGHT // 2 - 100))
        pygame.draw.circle(screen, color_choices[choice], (WIDTH // 2, HEIGHT // 2), 50)

        # enter name
        user_text_surface = base_font.render(myself.name, True, (255, 255, 255))
        name_text_surface = base_font.render("Enter your name:", True, (255, 255, 255))
        input_rect.w = max(100, user_text_surface.get_width() + 10)
        pygame.draw.rect(screen, color, input_rect)
        screen.blit(user_text_surface, (input_rect.x + 5, input_rect.y + 5))
        screen.blit(name_text_surface, (input_rect.x, input_rect.y - name_text_surface.get_height()))

    logorect = logoimg.get_rect()
    logorect.centerx = WIDTH // 2
    logorect.centery = 3*logorect.height // 4
    screen.blit(logoimg, logorect)
    if not menu:
        myself.color = color_choices[choice]
        myself.location = 0
        myself.spot = myself.id
        print(f"my id is {myself.id}")
    else:
        myself.color = choice
    return menu


def main():
    """
    Main game loop
    """
    n = Network()
    playernum = int(n.getP())
    myself = Player(playernum)
    draw_board()
    clock = pygame.time.Clock()
    roll = False
    stop_roll = True

    # event loop
    run = True
    firststart = True

    while run:

        # update game
        try:
            game = n.update(myself)
            if not firststart:
                for player in game.players:
                    if player.id == playernum:
                        myself = player
        except:
            run = False
            print("Couldn't get game")
            break

        # event handling
        events = pygame.event.get()
        for event in events:
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
        if firststart:
            firststart = draw_start_menu(game, myself, events)
        else:
            draw_board(game)
            myself = draw_ui(game, myself)
            draw_players(game, myself)
            draw_turn(game, myself)
        if myself.almostlose:
            draw_almostlose(game, myself, events)
        if myself.auction is True:
            draw_auction(game, myself, events)
        if game.started:
            if game.auctioned:
                if game.aucstart:
                    draw_auction_prop(game, myself, game.players[game.turn].aucselect, events)
                else:
                    myself.aucstart = False
        if roll:
            if stop_roll:
                roll = False
                myself.rolling = False
                myself.moving = True
                myself.showmoving = True
                myself.rolled = True

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
