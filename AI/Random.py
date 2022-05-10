#Liangyz
#2022/5/3  2:38

import main
import random

def get_possible_moves(board, player,info):
    possible_moves = []
    for [x,y] in info:
        if main.legal_move(board,player,x,y):
            possible_moves.append((x,y))
    return possible_moves

def move_random(board, player, info):
    possible_moves = get_possible_moves(board, player,info)
    conner = [(1,1),(1,8),(8,1),(8,8)]
    set_p = set(conner) & set(possible_moves)
    if len(possible_moves) == 0:
        return None, None
    elif set_p:
        return random.choice(list(set_p))
    else:
        return random.choice(possible_moves)



