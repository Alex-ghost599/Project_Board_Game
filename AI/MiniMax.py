#Liangyz
#2022/5/10  2:02

from copy import deepcopy

import main
import random
import numpy as np


evaluation = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,120,2,20,10,10,20,2,120,0],
    [0,2,1,3,3,3,3,1,2,0],
    [0,20,3,15,5,5,15,3,20,0],
    [0,10,3,5,5,5,5,3,10,0],
    [0,10,3,5,5,5,5,3,10,0],
    [0,20,3,15,5,5,15,3,20,0],
    [0,2,1,3,3,3,3,1,2,0],
    [0,120,2,20,10,10,20,2,120,0],
    [0,0,0,0,0,0,0,0,0,0],
]
evaluation=np.array(evaluation)

# def evaluate(board,player,eva=evaluation):
#     if player == 'black':
#         board[board == 2] = 0
#     else:
#         board[board == 1] = 0
#         board[board == 2] = 1
#     xsum = eva * board
#     return xsum.sum()


# def move_minimax(board, depth, player,info,end:bool):
#     if depth == 0 or main.gameover(board, info):
#         print(evaluate(board, player),player,'0')
#         return evaluate(board, player)
#
#     possible_moves = main.get_possible_moves(board,player,info)
#
#     conner = [(1,1),(1,8),(8,1),(8,8)]
#     set_p = set(conner) & set(possible_moves)
#     if set_p:
#         if end:
#             return random.choice(list(set_p))
#
#     tem0_board = deepcopy(board)
#     tem0_info = deepcopy(info)
#     score = 0
#     move = [None, None]
#
#     while depth > 0:
#         depth -= 1
#         if player == 'black':
#             for [x, y] in possible_moves:
#                 tem_board = deepcopy(tem0_board)
#                 tem_info = deepcopy(tem0_info)
#                 print('thinking',x,y)
#                 tem_board[x][y] = 1
#                 tem_info.remove([x, y])
#                 for i,j in main.flip_pawn(tem_board, 'black', x, y):
#                     tem_board[i][j] = 1
#
#                 tem_score = move_minimax(tem_board,depth,'white',tem_info,False)
#                 tem_score = -tem_score
#                 if score < tem_score:
#                     score = tem_score
#                     move = [x,y]
#                 elif score == tem_score:
#                     move = random.choice([[x,y],[move[0],move[1]]])
#                 elif score > tem_score:
#                     print('error')
#                     pass
#
#
#             if end:
#                 return move
#             else:
#                 print(score,'black')
#                 return score
#
#         elif player == 'white':
#             for [x, y] in possible_moves:
#                 tem_board=deepcopy(tem0_board)
#                 tem_info=deepcopy(tem0_info)
#                 print('thinking',x,y)
#                 tem_board[x][y] = 2
#                 tem_info.remove([x,y])
#                 for i,j in main.flip_pawn(tem_board, 'white', x, y):
#                     tem_board[i][j] = 2
#                 tem_score = move_minimax(tem_board,depth,'black',tem_info,False)
#                 tem_score = -tem_score
#                 if score < tem_score:
#                     score = tem_score
#                     move = [x,y]
#                 elif score == tem_score:
#                     move = random.choice([[x,y],[move[0],move[1]]])
#                 elif score > tem_score:
#                     print('error')
#                     pass
#
#             if end:
#                 return move
#             else:
#                 print(score,'white')
#                 return score

def evaluate(board,player,info,eva=evaluation):
    x = deepcopy(board)
    x[x == 2] = -1
    xe = eva * x
    score = xe.sum() * 0.30

    if player == 'black':
        mobility = 15 * len(main.get_possible_moves(board,player,info))
    else:
        mobility = -15 * len(main.get_possible_moves(board,player,info))
    mobility = mobility * 0.15

    number = 0
    b,w = main.score(board)
    if len(info) >18:
        if player == 'black':
            number = (b-w) * -12
        elif player == 'white':
            number = (w-b) * 12
    elif len(info) <=18:
        if player == 'black':
            number = (w-b) * -12
        elif player == 'white':
            number = (b-w) * 12
    number = number * 0.3

    corner = 0
    cor_map = [[1,1,1,1],
               [1,8,1,-1],
               [8,1,-1,1],
               [8,8,-1,-1]]
    for corner_i,corner_j,dx,dy in cor_map:
        if board[corner_i][corner_j] == 1:
            corner = corner + 10
        elif board[corner_i][corner_j] == -1:
            corner = corner - 10
        elif board[corner_i][corner_j] == 0:
            corner += board[corner_i][corner_j+dy]*-10
            corner += board[corner_i+dx][corner_j]*-10
            corner += board[corner_i+dx][corner_j+dy]*-15

            corner += board[corner_i][corner_j+(2*dy)]*10
            corner += board[corner_i+dx][corner_j+(2*dy)]*10
            corner += board[corner_i+(2*dx)][corner_j]*10
            corner += board[corner_i+(2*dx)][corner_j+dy]*10
            corner += board[corner_i+(2*dx)][corner_j+(2*dy)]*15

    corner = corner * 0.25
    return score + number + mobility + corner

def move_minimax(board, depth, player,info,end:bool,x=None,y=None):
    tem0_board = deepcopy(board)
    tem0_info = deepcopy(info)

    if x != None and y != None:
        if player == 'white':
            tem0_board[x][y] = 1
            tem0_info.remove([x, y])
            for i,j in main.flip_pawn(tem0_board, 'black', x, y):
                tem0_board[i][j] = 1
        elif player == 'black':
            tem0_board[x][y] = 2
            tem0_info.remove([x, y])
            for i,j in main.flip_pawn(tem0_board, 'white', x, y):
                tem0_board[i][j] = 2


    if depth == 0 or main.gameover(tem0_board, tem0_info):

        # print(evaluate(tem0_board),player,'0')
        return evaluate(tem0_board,player,info)

    possible_moves = main.get_possible_moves(tem0_board,player,tem0_info)
    for i in range(len(possible_moves)):
        possible_moves[i]=tuple(possible_moves[i])
    conner = [(1,1),(1,8),(8,1),(8,8)]
    set_p = set(conner) & set(possible_moves)
    if set_p:
        if end:
            return random.choice(list(set_p))


    move = [None, None]

    while depth > 0:
        depth -= 1
        if player == 'black':
            score= -99999
            for [x, y] in possible_moves:
                print('thinking',x,y)
                tem_score = move_minimax(tem0_board,depth,'white',tem0_info,False,x,y)
                print(tem_score)
                if tem_score > score:
                    score = tem_score
                    move = [x,y]
                elif tem_score == score:
                    move = random.choice([[x,y],[move[0],move[1]]])
                elif tem_score < score:
                    move=move


            if end:
                return move
            else:
                print(score,'black')
                return score



        elif player == 'white':
            score = 99999
            for [x, y] in possible_moves:
                print('thinking',x,y)
                tem_score = move_minimax(tem0_board,depth,'black',tem0_info,False,x,y)

                if tem_score < score:
                    score = tem_score
                    move = [x,y]
                elif tem_score == score:
                    move = random.choice([[x,y],[move[0],move[1]]])
                elif tem_score > score:
                    move = move


            if end:
                return move
            else:
                print(score,'white')
                return score
