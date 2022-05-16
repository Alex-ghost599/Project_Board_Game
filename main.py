# Liangyz
# 2022-04-26
# Basic visual interaction window


import pygame
import sys
import time
import random
import numpy as np
# import P_vs_P
# import P_vs_AI
# import AI_vs_AI


import menu

# parameters---------------------------------------------------------------------------------------------------------------------
board_size = (800,800)
window_size = (1200,900)
background_color = (13, 28, 45)
cell_size = (80,80)
pawn_size = (70,70)
space_size = (5,5)
fps = 60
number_of_win_black = 0
number_of_win_white = 0
Draw = 0
# load image

gameboard_origin = pygame.image.load("picture/board.png")
gameboard = pygame.transform.scale(gameboard_origin,board_size)

gamepawn_black_origin = pygame.image.load("picture/black.png")
gamepawn_black = pygame.transform.scale(gamepawn_black_origin,pawn_size)

gamepawn_white_origin = pygame.image.load("picture/white.png")
gamepawn_white = pygame.transform.scale(gamepawn_white_origin,pawn_size)

# initialize---------------------------------------------------------------------------------------------------------------------
pygame.init()
Runingclock = pygame.time.Clock()

surface = pygame.display.set_mode(window_size)

white = pygame.Surface(board_size)
white.fill((255,255,255))

socreboard = pygame.Surface((800,200))
socreboard.fill((130, 134, 136))

winnerboard_b = pygame.Surface((50,50))
winnerboard_b.fill((255,255,255))

winnerboard_w = pygame.Surface((50,50))
winnerboard_w.fill((255,255,255))

winnerboard_d = pygame.Surface((50,50))
winnerboard_d.fill((255,255,255))

font_stop = pygame.font.SysFont('arial',30)
font_resume = pygame.font.SysFont('arial',20)

stopbutton = pygame.Surface((80,80))
stopbutton.fill((52, 64, 235))
text_stop = font_stop.render("STOP",True,(0,0,0))

resumebutton = pygame.Surface((80,80))
resumebutton.fill((52, 235, 119))
text_resume = font_resume.render("RESUME",True,(0,0,0))

surface.blit(white,(375,50))
pygame.display.set_caption("Othello_lyz")

# Function---------------------------------------------------------------------------------------------------------------------
def restnewboard():
    newboard = np.zeros((10,10))

    newboard[4][4] = 1
    newboard[5][5] = 1
    newboard[4][5] = 2
    newboard[5][4] = 2

    return newboard

def exit_game():
    pygame.quit()
    sys.exit()

def isonboard(x,y):
    if x<1 or x>8 or y<1 or y>8:
        return False
    else:
        return True

def flip_pawn(board,player,x0,y0):
    flip = []
    if player == 'black':
        pawn = 1
        other = 2
    elif player == 'white':
        pawn = 2
        other = 1
    direction = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
    for xdirection,ydirection in direction:
        x= x0
        y= y0
        x += xdirection
        y += ydirection
        if not isonboard(x,y):
            continue
        while board[x][y] == other:
            x += xdirection
            y += ydirection
            if not isonboard(x,y):
                break
        if not isonboard(x,y):
            continue
        if board[x][y] == pawn:
            while True:
                x -= xdirection
                y -= ydirection
                if x == x0 and y == y0:
                    break
                flip.append([x,y])
    return flip

def legal_move(board,player,x,y):
    if not flip_pawn(board,player,x,y):
        return False
    else:
        return True

def check_is_any_legal_move(board,info,player):
    for [x,y] in info:
        if legal_move(board,player,x,y):
            return True
    return False

def get_possible_moves(board, player,info):
    possible_moves = []
    for [x,y] in info:
        if legal_move(board,player,x,y):
            possible_moves.append((x,y))
    random.shuffle(possible_moves)
    return possible_moves

def score(board):
    black = 0
    white = 0
    for i in range(1,9):
        for j in range(1,9):
            if board[i][j] == 1:
                black += 1
            elif board[i][j] == 2:
                white += 1
    return black,white

def gameover(board,info):
    if not info:
        return True
    game = 0
    for p in ['black','white']:
        if not check_is_any_legal_move(board,info,p):
            game += 1
    if game == 2:
        return True

def show_score(scoreboard,board):
    surface.blit(scoreboard,(375,350))
    # scoreboard_rect = scoreboard.get_rect()

    black,white = score(board)

    font = pygame.font.SysFont('arial',50)

    text1 = font.render("GAMEOVER",True,(0,0,0))
    text2 = font.render("Black:%d White:%d"%(black,white),True,(0,0,0))

    surface.blit(text1,(675,350))
    surface.blit(text2,(625,450))

    pygame.display.update()
    Runingclock.tick(fps)

def Scoreboard(number_of_win_black,
               number_of_win_white,
               Draw):
    black_rect=surface.blit(winnerboard_b,(50,600))
    draw_rect=surface.blit(winnerboard_d,(170,600))
    white_rect=surface.blit(winnerboard_w,(290,600))

    font=pygame.font.SysFont('arial',50)

    text_black=font.render(str(number_of_win_black),True,(0,0,0))
    text_black_rect=text_black.get_rect()
    text_black_rect.center=black_rect.center

    text_white=font.render(str(number_of_win_white),True,(0,0,0))
    text_white_rect=text_white.get_rect()
    text_white_rect.center=white_rect.center

    text_draw=font.render(str(Draw),True,(0,0,0))
    text_draw_rect=text_draw.get_rect()
    text_draw_rect.center=draw_rect.center

    surface.blit(text_black,(text_black_rect))
    surface.blit(text_white,(text_white_rect))
    surface.blit(text_draw,(text_draw_rect))

    pygame.display.update()
    Runingclock.tick(fps)



def main():
    running = True
    while running:
        # close window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()


        menu.main_menu()


# running---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()




