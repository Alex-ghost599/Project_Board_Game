#Liangyz
#2022/7/16  18:21

#deep q learning ai for othello
from copy import deepcopy

import numpy as np
import random
# import torch
# import torch.nn
# from AI.DQN.DQN_train import DQN
from AI.DQN.DQN_train_2 import DQN
# from AI.DQN.DQN_train_3 import DQN
from AI.DQN.game_train import Game
import main

def DQN_move(board,player,info):
    """some basic actions"""
    '''get the possible moves'''
    tem_moves = main.get_possible_moves(board,player,info)
    random.shuffle(tem_moves)

    '''check if the possible moves contains the corner, if yes, return the corner move'''
    tup_moves=[]
    for i in tem_moves:
        tup_moves.append(tuple(i))
    conner=[(1,1),(1,8),(8,1),(8,8)]
    set_p=set(conner) & set(tup_moves)
    if set_p:
        print('corner')
        return random.choice(list(set_p))

    '''if the moves can win the game, return the move'''
    for [x,y] in tem_moves:
        kill_board=deepcopy(board)
        kill_info=deepcopy(info)
        if player=='black':
            kill_board[x][y]=1
            kill_info.remove([x,y])
            for i,j in main.flip_pawn(kill_board,player,x,y):
                kill_board[i][j]=1
            if main.gameover(kill_board,kill_info):
                b,w = main.score(kill_board)
                if b>w:
                    print('kill')
                    return [x,y]
        else:
            kill_board[x][y]=2
            kill_info.remove([x,y])
            for i,j in main.flip_pawn(kill_board,player,x,y):
                kill_board[i][j]=2
            if main.gameover(kill_board,kill_info):
                b,w = main.score(kill_board)
                if b<w:
                    print('kill')
                    return [x,y]

    '''if the moves can make other player skip next round, return the move'''
    for [x,y] in tem_moves:
        skip_board=deepcopy(board)
        skip_info=deepcopy(info)
        if player=='black':
            skip_board[x][y]=1
            skip_info.remove([x,y])
            for i,j in main.flip_pawn(skip_board,player,x,y):
                skip_board[i][j]=1
            if not main.check_is_any_legal_move(skip_board,skip_info,'white'):
                print('skip')
                return [x,y]
        else:
            skip_board[x][y]=2
            skip_info.remove([x,y])
            for i,j in main.flip_pawn(skip_board,player,x,y):
                skip_board[i][j]=2
            if not main.check_is_any_legal_move(skip_board,skip_info,'black'):
                print('skip')
                return [x,y]

    """start DQN"""
    temp_board = deepcopy(board)
    temp_board = np.array(temp_board)
    temp_board[temp_board==2] = -1
    temp_board = np.delete(temp_board,[0,9],axis=1)
    temp_board = np.delete(temp_board,[0,9],axis=0)
    temp_info = deepcopy(info)
    temp = 0
    for i in temp_info:
        temp_info[temp] = [i[0]-1,i[1]-1]
        temp+=1

    # temp_board = temp_board.flatten()
    # print(temp_board.shape)
    if player == 'black':
        game = Game()
        game.board = temp_board
        game.info = temp_info
        offensive = DQN(1)
        s = game.Get_State()
        action = offensive.Choose_Action_EpsilonGreedy(s,game,1)
        move = [action//8 + 1, action%8 + 1]
        # print(action)
        return move


    elif player == 'white':
        game = Game()
        game.board = temp_board
        game.info = temp_info
        defensive = DQN(-1)
        s = game.Get_State()
        action = defensive.Choose_Action_EpsilonGreedy(s,game,-1)
        move = [action//8 + 1, action%8 + 1]
        # print(action)
        return move