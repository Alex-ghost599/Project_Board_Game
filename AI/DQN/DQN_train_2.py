#Liangyz
#2022/7/21  11:08
import datetime
import os
import random
import sys
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
# from reverse import *
# import game_train as gt
from AI.DQN import game_train as gt
BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

BOARD_SIZE = 8
N_STATE = pow(BOARD_SIZE, 2)
N_ACTION = pow(BOARD_SIZE, 2) + 1

LR = 0.001
EPISODE = 100000
BATCH_SIZE = 32
GAMMA = 0.7
ALPHA = 0.8
TRANSITIONS_CAPACITY = 5000
UPDATE_DELAY = 10

evaluation = [
    [120,2,20,10,10,20,2,120],
    [2,1,3,3,3,3,1,2],
    [20,3,15,5,5,15,3,20],
    [10,3,5,5,5,5,3,10],
    [10,3,5,5,5,5,3,10],
    [20,3,15,5,5,15,3,20],
    [2,1,3,3,3,3,1,2],
    [120,2,20,10,10,20,2,120]
]
evaluation=np.array(evaluation)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print('device:', device)


class NET(nn.Module):


    def __init__(self):
        super(NET, self).__init__()

        self.linear1 = nn.Sequential(
            nn.Linear(N_STATE, 64),
            nn.LeakyReLU()
        )
        # self.linear1.weight.data.normal_(0, 0.1)
        self.conv1 = nn.Sequential(
            nn.Conv1d(1, 64, 3, 1, 1),
            nn.LeakyReLU(inplace=True)
        )

        self.conv2 = nn.Sequential(
            nn.Conv1d(64, 64, 3, 1, 1),
            nn.LeakyReLU()
        )

        self.conv3 = nn.Sequential(
            nn.Conv1d(64, 128, 3, 1, 1),
            nn.LeakyReLU()
        )

        self.conv4 = nn.Sequential(
            nn.Conv1d(128, 128, 3, 1, 1),
            nn.LeakyReLU()
        )

        self.conv5 = nn.Sequential(
            nn.Conv1d(128, 256, 3, 1, 1),
            nn.LeakyReLU()
        )

        self.conv6 = nn.Sequential(
            nn.Conv1d(256, 256, 3, 1, 1),
            nn.LeakyReLU()
        )

        self.conv7 = nn.Sequential(
            nn.Conv1d(256, 256, 3, 1, 1),
            nn.LeakyReLU()
        )

        self.conv8 = nn.Sequential(
            nn.Conv1d(256, 128, 3, 1, 1),
            nn.LeakyReLU()
        )

        self.linear2_val = nn.Sequential(
            nn.Linear(128 * 64, 128),
            nn.LeakyReLU()
        )

        self.linear2_adv = nn.Sequential(
            nn.Linear(128 * 64, 128),
            nn.LeakyReLU()
        )

        self.linear3_adv = nn.Sequential(
            nn.Linear(128, N_ACTION)
        )

        self.linear3_val = nn.Sequential(
            nn.Linear(128, 1)
        )

    def forward(self, x):
        x = self.linear1(x)
        x = x.view(x.shape[0], 1, -1)
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.conv5(x)
        x = self.conv6(x)
        x = self.conv7(x)
        x = self.conv8(x)
        # x = x.flatten()
        x = x.view(x.shape[0], -1)
        # x = self.linear2(x)
        adv = self.linear2_adv(x)
        adv = self.linear3_adv(adv)

        val = self.linear2_val(x)
        val = self.linear3_val(val).expand(x.size(0), N_ACTION)

        res = val + adv - adv.mean(1).unsqueeze(1).expand(x.size(0), N_ACTION)

        return res


class DQN(object):
    def __init__(self, color):

        self.transitions = np.zeros((TRANSITIONS_CAPACITY, 2 * N_STATE + 2))
        self.transitions_index = 0
        self.learn_iter = 0

        self.Q, self.Q_ = NET().to(device), NET().to(device)
        # ??
        if color == 1:
            # pass
            # self.Q.load_state_dict(torch.load('D:\\Durham\\Project\\code\\AI\\DQN\\216000_dueling_offensive.pth', map_location='cpu'))
            self.Q.load_state_dict(torch.load('D:\\Durham\\Project\\code\\AI\\DQN\\model_offensive_3_new.pth'))
        elif color == -1:
            # pass
            # self.Q.load_state_dict(torch.load('D:\\Durham\\Project\\code\\AI\\DQN\\216000_dueling_defensive.pth', map_location='cpu'))
            self.Q.load_state_dict(torch.load('D:\\Durham\\Project\\code\\AI\\DQN\\model_defensive_3_new.pth'))

        self.optimizer = torch.optim.Adam(self.Q.parameters(), lr=LR)
        self.criteria = nn.MSELoss().to(device)

    def Choose_Action_EpsilonGreedy(self, x, game_state, color, Epsilon=0):


        if color == 1:
            availiable_pos = game_state.get_possible_moves('black')
        elif color == -1:
            availiable_pos = game_state.get_possible_moves('white')

        availiable_pos = list(map(lambda a: 8 * a[0] + a[1], availiable_pos))
        if len(availiable_pos) == 0:
            return 64

        if np.random.uniform() < Epsilon:  # random choose an action
            action = np.random.choice(availiable_pos, 1)[0]
        else:  # choose the max Q-value action
            x = torch.tensor(x, dtype=torch.float).to(device)
            # print(x.shape)
            # print(x)
            x = x.view(1, -1)
            # print(x)
            actions_values = self.Q(x)[0]
            # print(actions_values)

            # avai_actions = torch.tensor(actions_values[availiable_pos])
            avai_actions = actions_values[availiable_pos].clone().detach().to(device)
            # print(avai_actions)

            _, action_ind = torch.max(avai_actions, 0)
            action = availiable_pos[action_ind]
            # print(action)
        return action

    def Store_transition(self, s, a, r, s_):

        transition = np.hstack((s, a, r, s_))
        self.transitions[self.transitions_index % TRANSITIONS_CAPACITY] = transition
        self.transitions_index += 1

    def Learn(self, oppo_Q_):
        for step in range(10):
            if self.learn_iter % UPDATE_DELAY == 0:
                self.Q_.load_state_dict(self.Q.state_dict())
            self.learn_iter += 1

            sample_index = np.random.choice(TRANSITIONS_CAPACITY,
                                            BATCH_SIZE)
            batch_tran = self.transitions[sample_index, :]
            batch_s = batch_tran[:, :N_STATE]
            batch_a = batch_tran[:, N_STATE: N_STATE + 1]
            batch_r = batch_tran[:, N_STATE + 1: N_STATE + 2]
            batch_s_ = batch_tran[:, N_STATE + 2:]

            batch_s = torch.tensor(batch_s, dtype=torch.float).to(device)
            batch_s_ = torch.tensor(batch_s_, dtype=torch.float).to(device)
            batch_a = torch.tensor(batch_a, dtype=int).to(device)
            batch_r = torch.tensor(batch_r, dtype=torch.float).to(device)


            batch_y = self.Q(batch_s).gather(1,
                                             batch_a)
            batch_y_ = oppo_Q_(
                batch_s_).detach()
            batch_y_ = ALPHA * (batch_r - GAMMA * torch.max(batch_y_, 1)[0].view(-1,
                                                                        1))

            loss = self.criteria(batch_y, batch_y_)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()


def move_eva(game,player,eva=evaluation):
    possible_moves = game.get_possible_moves(player)
    result0 = 0
    move = [None,None]
    if len(possible_moves) != 0:
        for [x,y] in possible_moves:
            result0 = max(result0,eva[x][y])
            if result0 == eva[x][y]:
                move = [x,y]
            else:
                move = random.choice([[x,y],move])
        return move
    else:
        # pass
        return print('something wrong')


def mkcsv(path,data):
    file = os.path.exists(path)
    columns=['Episode', 'DQN_win','DQN_lose','Draw','DQN_win_rate','DQN_lose_rate','Draw_rate']
    if not file:
        df = pd.DataFrame(data=[data],columns=columns)
        df.to_csv(path,index=False)
    else:
        df = pd.DataFrame(data=[data],columns=columns)
        df.to_csv(path,index=False,mode='a',header=False)








