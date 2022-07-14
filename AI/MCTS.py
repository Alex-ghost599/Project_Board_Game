#Liangyz
#2022/5/17  19:36
import time

import main
import numpy as np
import random
import math
from copy import deepcopy

#Monte Carlo tree search for othello
#evaluation function:
evaluation=[
        [0,0,0,0,0,0,0,0,0,0],
        [0,10,1,3,3,3,3,1,10,0],
        [0,1,1,2,2,2,2,1,1,0],
        [0,3,2,4,4,4,4,2,3,0],
        [0,3,2,4,0,0,4,2,3,0],
        [0,3,2,4,0,0,4,2,3,0],
        [0,3,2,4,4,4,4,2,3,0],
        [0,1,1,2,2,2,2,1,2,0],
        [0,10,1,3,3,3,3,1,10,0],
        [0,0,0,0,0,0,0,0,0,0],
    ]
evaluation=np.array(evaluation)

hype_parameter = 2

def evaluate(board,player,info,eva=evaluation):
    # socre of board
    x = deepcopy(board)
    x[x==2] = -1
    xsum =eva*x
    score = xsum.sum()*0.35

    #score of mobility of opposite player
    if player == 'black':
        mobility = -5*len(main.get_possible_moves(board,'white',info))
    else:
        mobility = 5*len(main.get_possible_moves(board,'black',info))
    mobility = mobility * 0.4

    #score of pieces
    number = 0
    b,w = main.score(board)
    if len(info)>18:
        if player == 'black':
            number = (b-w)*-10
        elif player == 'white':
            number = (w-b)*10
    elif len(info)<=18:
        if player == 'black':
            number = (b-w)*10
        elif player == 'white':
            number = (w-b)*-10
    number = number * 0.25



    return score + mobility + number

class Node:
    def __init__(self,board,player,info,move=None,parent=None):
        self.board = board
        self.player = player
        self.info = info
        self.parent = parent
        self.children = []
        self.move = move
        self.state_value = 0
        self.result_value = 0
        self.visit = 0

    def add_child(self,board,player,info,move):
        board = deepcopy(board)
        player = deepcopy(player)
        info = deepcopy(info)
        child = Node(board,player,info,move,self)
        self.children.append(child)
        return child

    def update_score(self,result_value):
        self.visit += 1
        self.result_value += result_value
        if self.parent:
            self.parent.update_score(result_value)

    def fully_expanded(self):
        return len(self.children) == len(main.get_possible_moves(self.board,self.player,self.info))

    def find_root(self):
        if self.parent:
            return self.parent.find_root()
        else:
            return self

    def best_child(self):
        for child in self.children:
            if child.player == 'black':
                return max(self.children,key=lambda x:((x.result_value)/(1+x.visit))+hype_parameter*math.sqrt(math.log(x.find_root().visit+1)/(1+x.visit)))
            else:
                return min(self.children,key=lambda x:((x.result_value)/(1+x.visit))-hype_parameter*math.sqrt(math.log(x.find_root().visit+1)/(1+x.visit)))


    def select_child(self):
        return max(self.children,key=lambda x:x.visit)

    def best_move(self):
        return self.select_child().move

    def __repr__(self):
        return 'Node({},{},{},{},{},{})'.format(self.board,self.player,self.info,self.parent,self.children,self.move)

def move_eva(board,player,info,eva=evaluation):
    possible_moves = main.get_possible_moves(board,player,info)
    result0 = 0
    move = [None,None]
    if len(possible_moves) != 0:
        for [x,y] in possible_moves:
            result0 = max(result0,eva[x][y])
            if result0 == eva[x][y]:
                move = [x,y]
            else:
                move = move
        return move
    else:
        return None,None

def simulation(node,eva=evaluation):
    board = node.board
    player = node.player
    info = node.info
    # v=deepcopy(board)
    # v[v==2]=-1
    # vsum=eva*v
    if player == 'white':
        player = 'black'
    else:
        player = 'white'
    while not main.gameover(board,info):
        x,y = move_eva(board,player,info,eva)
        if [x,y]!=[None,None]:
            if player == 'black':
                board[x][y] = 1
                info.remove([x,y])
                for i,j in main.flip_pawn(board,player,x,y):
                    board[i][j] = 1
                player = 'white'
            else:
                board[x][y] = 2
                info.remove([x,y])
                for i,j in main.flip_pawn(board,player,x,y):
                    board[i][j] = 2
                player = 'black'

        if player=='black':
            if not main.check_is_any_legal_move(board,info,'black'):
                player='white'
        elif player=='white':
            if not main.check_is_any_legal_move(board,info,'white'):
                player='black'

    b,w = main.score(board)

    if b>w:
        return 20
    elif b<w:
        return -20
    else:
        # if node.player == 'black':
        #     return 1
        # else:
        #     return -1
        return 0


def move_MCTS(in_board,in_player,in_info,max_iter=200):
    board = deepcopy(in_board)
    player = deepcopy(in_player)
    info = deepcopy(in_info)
    root = Node(board,player,info)
    #start mcts
    for i in range(max_iter):
        # add all possible moves to root
        if not root.fully_expanded():
            possible_moves = main.get_possible_moves(root.board,root.player,root.info)
            for move in possible_moves:
                root.add_child(root.board,root.player,root.info,move)
            for child in root.children:
                if child.player == 'black':
                    child.board[child.move[0]][child.move[1]] = 1
                    child.info.remove(child.move)
                    for i,j in main.flip_pawn(child.board,child.player,child.move[0],child.move[1]):
                        child.board[i][j] = 1
                else:
                    child.board[child.move[0]][child.move[1]] = 2
                    child.info.remove(child.move)
                    for i,j in main.flip_pawn(child.board,child.player,child.move[0],child.move[1]):
                        child.board[i][j] = 2
            # initialized state_value of child
            # for child in root.children:
            #     child.state_value = evaluate(child.board,child.player,child.info)/(child.visit+1)
            #     # child.score = hype_parameter * child.state_value
        # select best child
        best_child_selected = root.best_child()
        # expand child
        if best_child_selected.player=='black':
            opposite_player='white'
        else:
            opposite_player='black'
        if not main.gameover(best_child_selected.board,best_child_selected.info) and \
        main.check_is_any_legal_move(best_child_selected.board,best_child_selected.info,opposite_player):
            if not len(best_child_selected.children) == len(main.get_possible_moves(best_child_selected.board,opposite_player,best_child_selected.info)):
                possible_moves_opposite = main.get_possible_moves(best_child_selected.board,opposite_player,best_child_selected.info)
                for move in possible_moves_opposite:
                    best_child_selected.add_child(best_child_selected.board,opposite_player,best_child_selected.info,move)
                for child in best_child_selected.children:
                    if child.player == 'black':
                        child.board[child.move[0]][child.move[1]] = 1
                        child.info.remove(child.move)
                        for i,j in main.flip_pawn(child.board,child.player,child.move[0],child.move[1]):
                            child.board[i][j] = 1
                    else:
                        child.board[child.move[0]][child.move[1]] = 2
                        child.info.remove(child.move)
                        for i,j in main.flip_pawn(child.board,child.player,child.move[0],child.move[1]):
                            child.board[i][j] = 2
                # initialized state_value of child
                # for child in best_child_selected.children:
                #     child.state_value = evaluate(child.board,child.player,child.info)/(child.visit+1)
                #     # child.score = hype_parameter * child.state_value
            best_expanded_child = best_child_selected.best_child()
            # simulate
            reward = simulation(best_expanded_child)
            # backpropagate
            best_expanded_child.update_score(reward)
        else:
            return best_child_selected.move
    # return best move
    print('state_value:',root.select_child().state_value)
    print('reward:',root.select_child().result_value)
    print('visit:',root.select_child().visit)
    return root.best_move()
