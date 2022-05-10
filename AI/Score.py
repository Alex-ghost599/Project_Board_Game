#Liangyz
#2022/5/10  1:04

import main
import random

def get_possible_moves(board, player,info):
    possible_moves = []
    for [x,y] in info:
        if main.legal_move(board,player,x,y):
            possible_moves.append((x,y))
    return possible_moves

def move_score(board,player,info):
    possible_moves = get_possible_moves(board,player,info)
    conner=[(1,1),(1,8),(8,1),(8,8)]
    set_p=set(conner)&set(possible_moves)
    if set_p:
        return random.choice(list(set_p))
    tem_board=board.copy()
    for [x,y] in possible_moves:


