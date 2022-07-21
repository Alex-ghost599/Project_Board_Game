#Liangyz
#2022/7/16  18:21

#deep learning ai for othello
import tensorflow as tf
import numpy as np
import random
import math
from copy import deepcopy
import time
import gym
import boardgame2
import keras

from keras.models import Sequential
from keras.layers import Dense,Activation,Flatten,BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

env = gym.make('CartPole-v0')
class NeuralNetwork:
    def __init__(self):
        self.input_shape = (1,64)
        self.output = (1,64)
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(64, input_shape=self.input_shape))
        model.add(Activation('relu'))
        model.add(Dense(128))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Dense(256))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Dense(128))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Dense(64))
        model.add(Activation('linear'))
        return model


a = NeuralNetwork()
a.build_model()
# print(a)

def DQN(a):
    memory = SequentialMemory(limit=50000, window_length=1)
    policy = EpsGreedyQPolicy(eps=0.1)
    dqn = DQNAgent(model=a, nb_actions=64, memory=memory, nb_steps_warmup=10,
                     target_model_update=1e-2, policy=policy)
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])

    return dqn

b = DQN(a)
b.fit(env, nb_steps=10, visualize=False, verbose=2)
b.test(env, nb_episodes=10, visualize=True)