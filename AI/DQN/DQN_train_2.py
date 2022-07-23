#Liangyz
#2022/7/21  11:08

import os
import sys

BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
# from reverse import *
from AI.DQN import game_train as gt

BOARD_SIZE = 8
N_STATE = pow(BOARD_SIZE, 2)        # 1*64，表示棋盘
N_ACTION = pow(BOARD_SIZE, 2) + 1   # 1*65，表示动作（包括没有可下的位置）

LR = 0.00001
EPISODE = 10000000
BATCH_SIZE = 320
GAMMA = 0.3
ALPHA = 0.8
TRANSITIONS_CAPACITY = 2000
UPDATE_DELAY = 10

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print('device:', device)


class NET(nn.Module):
    """定义网络结构

    Returns:
        x [tensor] -- (batch, N_ACTION)，每一行表示各个action的分数
    """

    def __init__(self):
        super(NET, self).__init__()

        self.linear1 = nn.Sequential(
            nn.Linear(N_STATE, 128),
            nn.LeakyReLU()
        )
        # self.linear1.weight.data.normal_(0, 0.1)

        self.conv1 = nn.Sequential(
            nn.Conv1d(1, 4, 3, 1, 1),   # in_channel=1, out_channel=4, kernel_size卷积核大小=3, stride步长=1, padding=1
            nn.LeakyReLU(inplace=True)  # inplace=true，输出数据会覆盖输入数据，再求梯度时不可用。
        )

        # self.conv2 = nn.Sequential(
        #     nn.Conv1d(4, 8, 3, 1, 1),
        #     nn.LeakyReLU()
        # )

        self.conv3 = nn.Sequential(
            nn.Conv1d(4, 16, 3, 1, 1),
            nn.LeakyReLU()
        )

        self.linear2_val = nn.Sequential(
            nn.Linear(16 * 128, 512),
            nn.LeakyReLU()
        )

        self.linear2_adv = nn.Sequential(
            nn.Linear(16 * 128, 512),
            nn.LeakyReLU()
        )

        self.linear3_adv = nn.Sequential(
            nn.Linear(512, N_ACTION)
        )

        self.linear3_val = nn.Sequential(
            nn.Linear(512, 1)
        )

    def forward(self, x):
        x = self.linear1(x)
        x = x.view(x.shape[0], 1, -1)   # 将多行tensor拼接成一行
        x = self.conv1(x)
        # x = self.conv2(x)
        x = self.conv3(x)
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
        """
        color: 1表示先手；-1表示后手

        transitions : 存储状态的空间，格式为(state, action, reward, state_), state_为后继状态
        transitions_index : 记录当前使用存储空间的索引
        learn_iter : 当到达UPDATE_ITERS时，就更新预测网络 Q_ ，把Q的参数复制给它
        """
        self.transitions = np.zeros((TRANSITIONS_CAPACITY, 2 * N_STATE + 2))
        self.transitions_index = 0
        self.learn_iter = 0

        self.Q, self.Q_ = NET().to(device), NET().to(device)
        # ??
        if color == 1:
            # pass
            # self.Q.load_state_dict(torch.load('data/216000_dueling_offensive.pth', map_location='cpu'))
            self.Q.load_state_dict(torch.load('D:\\Durham\\Project\\code\\AI\\DQN\\model_offensive_2.pth'))
        elif color == -1:
            # pass
            # self.Q.load_state_dict(torch.load('data/216000_dueling_defensive.pth', map_location='cpu'))
            self.Q.load_state_dict(torch.load('D:\\Durham\\Project\\code\\AI\\DQN\\model_defensive_2.pth'))

        self.optimizer = torch.optim.Adam(self.Q.parameters(), lr=LR)
        self.criteria = nn.MSELoss().to(device)

    def Choose_Action_EpsilonGreedy(self, x, game_state, color, Epsilon=0.2):
        """ε-greedy算法选择下一个action。以ε概率随机选择一个action，否则就选择Q值最大的action

        Arguments:
            x [tensor] -- NET网络的输入值，即当前状态，在Q-Learning中，选择下一个动作应该是查表得到的，
                            在DQN中没有这个表，所以要先经过Q网络得到一个状态的Q值，然后选择这向量里概率最大的action
            game_state [class] -- 当前的游戏状态
            color int -- 1表示黑棋，-1表示白棋

        Returns:
            action [int] -- 0~64中的一个数，表示下棋的位置；64表示跳过
        """

        if color == 1:
            availiable_pos = game_state.get_possible_moves('black')
        elif color == -1:
            availiable_pos = game_state.get_possible_moves('white')

        availiable_pos = list(map(lambda a: 8 * a[0] + a[1], availiable_pos))  # 列表,表明合法位置
        if len(availiable_pos) == 0:
            return 64  # 表示这一步只能跳过

        if np.random.uniform() < Epsilon:  # random choose an action
            action = np.random.choice(availiable_pos, 1)[0]      # 从available_pos里面抽取1个数字，并返回数组
        else:  # choose the max Q-value action
            x = torch.tensor(x, dtype=torch.float).to(device)
            # print(x.shape)
            # print(x)
            x = x.view(1, -1)
            # print(x)
            actions_values = self.Q(x)[0]  # 65维tensor，各个action在各个位置的值（1*65维，经过NET的结果）
            # print(actions_values)

            # avai_actions = torch.tensor(actions_values[availiable_pos])   # actions_values是各个action的得分
            avai_actions = actions_values[availiable_pos].clone().detach().to(device)  # actions_values是各个action的得分
            # print(avai_actions)

            _, action_ind = torch.max(avai_actions, 0)
            action = availiable_pos[action_ind]
            # print(action)
        return action

    def Store_transition(self, s, a, r, s_):
        """把一组转移属性存储到transitions中

        Arguments:
            s {[type]} -- 当前状态
            a {[type]} -- 选择的动作
            r {[type]} -- reward值
            s_ {[type]} -- 后继状态
        """
        transition = np.hstack((s, a, r, s_))   # 拼接在一起
        self.transitions[self.transitions_index % TRANSITIONS_CAPACITY] = transition
        self.transitions_index += 1

    def Learn(self, oppo_Q_):
        for step in range(10):
            if self.learn_iter % UPDATE_DELAY == 0:  # update parameters of Q_ 每隔一段时间将Q的参数直接给到Q_
                self.Q_.load_state_dict(self.Q.state_dict())
            self.learn_iter += 1

            sample_index = np.random.choice(TRANSITIONS_CAPACITY,
                                            BATCH_SIZE)  # randomly choose BATCH_SIZE samples to learn 从经验池中随机选取进行训练，是数组
            batch_tran = self.transitions[sample_index, :]
            batch_s = batch_tran[:, :N_STATE]
            batch_a = batch_tran[:, N_STATE: N_STATE + 1]
            batch_r = batch_tran[:, N_STATE + 1: N_STATE + 2]
            batch_s_ = batch_tran[:, N_STATE + 2:]

            batch_s = torch.tensor(batch_s, dtype=torch.float).to(device)
            batch_s_ = torch.tensor(batch_s_, dtype=torch.float).to(device)
            batch_a = torch.tensor(batch_a, dtype=int).to(device)
            batch_r = torch.tensor(batch_r, dtype=torch.float).to(device)

            # gather函数
            batch_y = self.Q(batch_s).gather(1,
                                             batch_a)  # gather figure out which action actually is chosen 相当于从第一维取第batch_a位置的值
            batch_y_ = oppo_Q_(
                batch_s_).detach()  # detach return a new Variable which do not have gradient detach就是禁止梯度更新，这些图变量包含了梯度，在计算loss的时候会更新，因为Q_不用更新，因此禁止梯度。
            batch_y_ = batch_r - GAMMA * torch.max(batch_y_, 1)[0].view(-1,
                                                                        1)  # max(1) return (value,index) for each row

            loss = self.criteria(batch_y, batch_y_)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()


if __name__ == "__main__":
    offensive = DQN(1)
    defensive = DQN(-1)

    for episode in range(EPISODE * 5):
        game_state = gt.Game()
        round_ = 0
        while True:
            # black
            # print(round_)
            round_ += 1
            # game_state.Display()    # 输出棋盘
            s = game_state.Get_State()
            a = offensive.Choose_Action_EpsilonGreedy(s, game_state, 1)
            game_state.Move(a,'black')
            r = game_state.reward()
            s_ = game_state.Get_State()

            offensive.Store_transition(s, a, r, s_)   # 先后手的经验池分开存
            # defensive.Store_transition(s, a, -r, s_)

            if r == 100 or r == -100 or game_state.gameover():  # 当这局游戏结束或双方下够了100次。经验池已经有很多样本，此时可以开始训练
                offensive.Learn(defensive.Q_) # 用对手的Q_网络来计算下一个状态
                print('Episode:{} | Reward:{}'.format(episode, r))
                break

            # white
            # game_state.Display()
            s = game_state.Get_State()
            a = defensive.Choose_Action_EpsilonGreedy(s, game_state, -1)
            game_state.Move(a,'white')
            r = game_state.reward()
            s_ = game_state.Get_State()

            # offensive.Store_transition(s, a, r, s_)
            defensive.Store_transition(s, a, -r, s_) # 先后手的经验池分开存

            if r == 100 or r == -100 or game_state.gameover():
                defensive.Learn(offensive.Q_) # 用对手的Q_网络来计算下一个状态
                print('Episode:{} | Reward:{}'.format(episode, r))
                break

        if (episode + 1) % 100 == 0:
            torch.save(offensive.Q.state_dict(), 'D:\\Durham\\Project\\code\\AI\\DQN\\model_offensive_2.pth')
            torch.save(defensive.Q.state_dict(), 'D:\\Durham\\Project\\code\\AI\\DQN\\model_defensive_2.pth')
            # break
