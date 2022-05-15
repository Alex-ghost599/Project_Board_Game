#Liangyz
#2022/5/3  3:53

import main
import random
import numpy as np


def move_eva(board,player,info):
    # make elvaluta matrix
    eva=np.zeros((8,8))
    for x,y in ((0,0),(0,7),(7,0),(7,7)):
        eva[x][y]=5
    for x,y in ((1,1),(0,1),(1,0),(0,6),(1,6),(1,7),(6,0),(6,1),(7,1),(6,6),(6,7),(7,6)):
        eva[x][y]=1
    for x,y in ((0,2),(0,3),(0,4),(0,5),(2,7),(3,7),(4,7),(5,7),(7,2),(7,3),(7,4),(7,5),(2,0),(3,0),(4,0),(5,0)):
        eva[x][y]=3
    for x,y in ((1,2),(1,3),(1,4),(1,5),(2,1),(3,1),(4,1),(5,1),(2,6),(3,6),(4,6),(5,6),(6,2),(6,3),(6,4),(6,5)):
        eva[x][y]=2
    for x,y in ((2,2),(2,3),(2,4),(2,5),(3,2),(4,2),(5,2),(5,3),(5,4),(3,5),(4,5),(5,5)):
        eva[x][y]=4
    # print(eva)
    possible_moves = main.get_possible_moves(board,player,info)
    result0 = 0
    move = [None,None]
    if len(possible_moves) != 0:
        for [x0,y0] in possible_moves:
            x = x0 - 1
            y = y0 - 1
            if result0 < eva[x][y]:
                result0 = eva[x][y]
                move = [x0,y0]
            elif result0 == eva[x][y]:
                move = random.choice([[x0,y0],[move[0],move[1]]])
            else:
                move = move
        return move
    else:
        return None,None



