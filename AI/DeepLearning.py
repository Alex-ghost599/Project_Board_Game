#Liangyz
#2022/7/16  18:21

#deep learning ai for othello
import tensorflow as tf
import numpy as np
import random
import math
from copy import deepcopy
import time

class neurons:
    def __init__(self,input_size,output_size,hidden_size):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.W1 = tf.Variable(tf.random_normal([input_size,hidden_size]))
        self.b1 = tf.Variable(tf.random_normal([hidden_size]))
        self.W2 = tf.Variable(tf.random_normal([hidden_size,output_size]))
        self.b2 = tf.Variable(tf.random_normal([output_size]))
        self.x = tf.placeholder(tf.float32,[None,input_size])
        self.y = tf.placeholder(tf.float32,[None,output_size])
        self.z1 = tf.matmul(self.x,self.W1) + self.b1
        self.a1 = tf.nn.relu(self.z1)
        self.z2 = tf.matmul(self.a1,self.W2) + self.b2
        self.a2 = tf.nn.relu(self.z2)
        self.loss = tf.reduce_mean(tf.square(self.a2-self.y))
        self.train = tf.train.AdamOptimizer(0.001).minimize(self.loss)
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    def train_neurons(self,x,y):
        return self.sess.run([self.train,self.loss],feed_dict={self.x:x,self.y:y})

    def predict(self,x):
        return self.sess.run(self.a2,feed_dict={self.x:x})

    def close(self):
        self.sess.close()
