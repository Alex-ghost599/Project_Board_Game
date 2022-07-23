#Liangyz
#2022/7/16  18:21

#deep q learning ai for othello
from copy import deepcopy

import numpy as np
import torch
import torch.nn
from AI.DQN.DQN_train import NET,DQN
from AI.DQN.game_train import Game
import main

def DQN_move(board,player,info):
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