#Liangyz
#2022/5/17  19:36
import time

import main
import numpy as np
import random
import math
from copy import deepcopy

"""Monte Carlo tree search for othello"""
"""evaluation matrix"""
evaluation=[
        [0,0,0,0,0,0,0,0,0,0],
        [0,5,1,3,3,3,3,1,5,0],
        [0,1,1,2,2,2,2,1,1,0],
        [0,3,2,3,4,4,3,2,3,0],
        [0,3,2,4,5,5,4,2,3,0],
        [0,3,2,4,5,5,4,2,3,0],
        [0,3,2,3,4,4,3,2,3,0],
        [0,1,1,2,2,2,2,1,2,0],
        [0,5,1,3,3,3,3,1,5,0],
        [0,0,0,0,0,0,0,0,0,0],
    ]
evaluation=np.array(evaluation)

# hype_parameter = 3.2
"""evaluation function"""
def evaluate(board,player,info,eva=evaluation):
    """socre of board"""
    x = deepcopy(board)
    x[x==2] = -1
    xsum =eva*x
    score = xsum.sum() * 0.3

    """score of mobility of opposite player"""
    if player == 'black':
        mobility = -5*len(main.get_possible_moves(board,'white',info))
    else:
        mobility = 5*len(main.get_possible_moves(board,'black',info))
    mobility = mobility * 0.15

    """score of pieces"""
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
    number = number * 0.3

    """score of Corner"""
    corner = 0
    cor_map = [[1,1,1,1],
               [1,8,1,-1],
               [8,1,-1,1],
               [8,8,-1,-1]]
    for corner_i,corner_j,dx,dy in cor_map:
        if board[corner_i][corner_j] == 1:
            corner = corner + 10
        elif board[corner_i][corner_j] == -1:
            corner = corner - 10
        elif board[corner_i][corner_j] == 0:
            if player == 'black':
                corner += board[corner_i][corner_j+dy]*-10
                corner += board[corner_i+dx][corner_j]*-10
                corner += board[corner_i+dx][corner_j+dy]*-15

                corner += board[corner_i][corner_j+(2*dy)]*10
                corner += board[corner_i+dx][corner_j+(2*dy)]*10
                corner += board[corner_i+(2*dx)][corner_j]*10
                corner += board[corner_i+(2*dx)][corner_j+dy]*10
                corner += board[corner_i+(2*dx)][corner_j+(2*dy)]*15
            elif player == 'white':
                corner += board[corner_i][corner_j+dy]*10
                corner += board[corner_i+dx][corner_j]*10
                corner += board[corner_i+dx][corner_j+dy]*15

                corner += board[corner_i][corner_j+(2*dy)]*-10
                corner += board[corner_i+dx][corner_j+(2*dy)]*-10
                corner += board[corner_i+(2*dx)][corner_j]*-10
                corner += board[corner_i+(2*dx)][corner_j+dy]*-10
                corner += board[corner_i+(2*dx)][corner_j+(2*dy)]*-15

    corner = corner * 0.25

    """return value between 0 and 1"""
    z = score + mobility + number + corner

    z = 1.0/(1.0+math.exp(-z))



    return z


"""Monte Carlo Tree Structure"""
class Node:
    def __init__(self,board,player,info,hype_parameter,move=None,parent=None):
        self.board = board
        self.player = player
        self.info = info
        self.Init_value = 0
        self.result_value = []
        self.visit = 0
        self.children=[]
        self.move=move
        self.parent = parent
        self.hype_parameter = hype_parameter

    def add_child(self,board,player,info,hype_parameter,move):
        board = deepcopy(board)
        player = deepcopy(player)
        info = deepcopy(info)
        child = Node(board,player,info,hype_parameter,move,self)
        self.children.append(child)
        return child

    def update_score(self,reword):
        self.visit += 1
        a = self.result_value
        a.append(reword)
        self.result_value = a
        if self.parent:
            self.parent.update_score(reword)

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
                return max(self.children,key=lambda x:(np.mean(0 if x.result_value == [] else x.result_value) + x.hype_parameter * x.Init_value/(1+x.visit)))
                # return max(self.children,key=lambda x: (sum(x.result_value) + hype_parameter*math.sqrt(math.log(x.find_root().visit+1)/(1+x.visit))))
            else:
                return min(self.children,key=lambda x:(np.mean(0 if x.result_value == [] else x.result_value) + x.hype_parameter * x.Init_value/(1+x.visit)))
                # return min(self.children,key=lambda x: (sum(x.result_value)/(1+x.visit)+hype_parameter*x.Init_value))

    def select_child(self):
        return max(self.children,key=lambda x:x.visit)

    def best_move(self):
        return self.select_child().move

    def __repr__(self):
        return 'Node({},{},{},{},{},{})'.format(self.board,self.player,self.info,self.parent,self.children,self.move)


"""get moves in simulation"""
def move_random(board,player,info):
    """get moves"""
    possible_moves = main.get_possible_moves(board,player,info)
    if len(possible_moves) == 0:
        return None, None
    else:
        return random.choice(possible_moves)


"""simulation state"""
def simulation(node,eva=evaluation):
    """get data"""
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
    """play a game until the end"""
    while not main.gameover(board,info):
        x,y = move_random(board,player,info)
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
    """get the result"""
    b,w = main.score(board)
    """based on the result, return the reword"""
    if b>w:
        return 1
    elif b<w:
        return -1
    else:
        # if node.player == 'black':
        #     return 1
        # else:
        #     return -1
        return -0.1


"""main function"""
def move_RMCTS(in_board,in_player,in_info,hype_parameter,max_iter=1000):
    """restore input data"""
    board = deepcopy(in_board)
    player = deepcopy(in_player)
    info = deepcopy(in_info)
    root = Node(board,player,info,hype_parameter)

    """some basic actions"""
    '''get the possible moves'''
    tem_moves = main.get_possible_moves(in_board,in_player,in_info)
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
        kill_board=deepcopy(in_board)
        kill_info=deepcopy(in_info)
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
        skip_board=deepcopy(in_board)
        skip_info=deepcopy(in_info)
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


    """start mcts"""
    for i in range(max_iter):
        """add all possible moves to root"""
        if not root.fully_expanded():
            possible_moves = main.get_possible_moves(root.board,root.player,root.info)
            random.shuffle(possible_moves)
            for move in possible_moves:
                root.add_child(root.board,root.player,root.info,hype_parameter,move)
            for child in root.children:
                if child.player == 'black':
                    child.board[child.move[0]][child.move[1]] = 1
                    child.info.remove(child.move)
                    for x,y in main.flip_pawn(child.board,child.player,child.move[0],child.move[1]):
                        child.board[x][y] = 1
                else:
                    child.board[child.move[0]][child.move[1]] = 2
                    child.info.remove(child.move)
                    for x,y in main.flip_pawn(child.board,child.player,child.move[0],child.move[1]):
                        child.board[x][y] = 2
            # initialized Init_value of child
            # Init_list = []
            # for child in root.children:
            #     Init_list.append(evaluate(child.board,child.player,child.info))
            # for child in root.children:
            #     child.Init_value = evaluate(child.board,child.player,child.info)/sum(map(abs,Init_list))
            for child in root.children:
                child.Init_value = evaluate(child.board,child.player,child.info)
                # child.score = hype_parameter * child.Init_value
        # select best child

        # print(root.best_child().result_value)
        # print(root.best_child().visit)
        # print(type(root.best_child().result_value))
        # expand child
        if root.best_child().player=='black':
            opposite_player='white'
        else:
            opposite_player='black'
        if not main.gameover(root.best_child().board,root.best_child().info) and \
                main.check_is_any_legal_move(root.best_child().board,root.best_child().info,opposite_player):
            if not len(root.best_child().children) == len(main.get_possible_moves(root.best_child().board,opposite_player,root.best_child().info)):
                possible_moves_opposite = main.get_possible_moves(root.best_child().board,opposite_player,root.best_child().info)
                random.shuffle(possible_moves_opposite)
                for move in possible_moves_opposite:
                    root.best_child().add_child(root.best_child().board,opposite_player,root.best_child().info,hype_parameter,move)
                for child in root.best_child().children:
                    if child.player == 'black':
                        child.board[child.move[0]][child.move[1]] = 1
                        child.info.remove(child.move)
                        for x,y in main.flip_pawn(child.board,child.player,child.move[0],child.move[1]):
                            child.board[x][y] = 1
                    else:
                        child.board[child.move[0]][child.move[1]] = 2
                        child.info.remove(child.move)
                        for x,y in main.flip_pawn(child.board,child.player,child.move[0],child.move[1]):
                            child.board[x][y] = 2
            # # initialized Init_value of child
                for child in root.best_child().children:
                    child.Init_value = evaluate(child.board,child.player,child.info)
                # child.score = hype_parameter * child.Init_value
            # best_expanded_child = root.best_child().best_child()
            # simulate
            # select_child = random.choice(root.best_child().children)
            weight = []
            for child in root.best_child().children:
                if opposite_player == 'black':
                    # print('black',child.Init_value)
                    if child.Init_value == 0:
                        weight.append(0.0000000000000001)
                    else:
                        weight.append(child.Init_value)
                else:
                    # print('white',child.Init_value)
                    if child.Init_value == 1:
                        weight.append(0.0000000000000001)
                    else:
                        weight.append(1-child.Init_value)
            # print(weight)
            select_child = random.choices(root.best_child().children,weights=weight)[0]
            reward = simulation(select_child)
            # print('simulation:', i)
            # backpropagate
            select_child.update_score(reward)
        else:
            if main.gameover(root.best_child().board,root.best_child().info):
                black_score,white_score = main.score(root.best_child().board)
                if in_player == 'black':
                    if black_score > white_score:
                        return root.best_child().move
                    else:
                        return root.best_child().undate_score(-1)
                else:
                    if white_score > black_score:
                        return root.best_child().move
                    else:
                        return root.best_child().undate_score(1)
            return root.best_child().move

    # return best move
    # print('Init_value:',root.select_child().Init_value)
    # print('reward:',root.select_child().result_value)
    print('visit:',root.select_child().visit)
    return root.best_move()
