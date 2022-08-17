#Liangyz
#2022/7/25  14:48

import datetime
import sys
import os
import random
import math
import numpy as np
import pandas as pd
from copy import deepcopy


BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

"""Othello rules Function"""
def restnewboard():
    newboard = np.zeros((10,10))

    newboard[4][4] = 1
    newboard[5][5] = 1
    newboard[4][5] = 2
    newboard[5][4] = 2

    return newboard

def isonboard(x,y):
    if x<1 or x>8 or y<1 or y>8:
        return False
    else:
        return True

def flip_pawn(board,player,x0,y0):
    flip = []
    if player == 'black':
        pawn = 1
        other = 2
    elif player == 'white':
        pawn = 2
        other = 1
    direction = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
    for xdirection,ydirection in direction:
        x= x0
        y= y0
        x += xdirection
        y += ydirection
        if not isonboard(x,y):
            continue
        while board[x][y] == other:
            x += xdirection
            y += ydirection
            if not isonboard(x,y):
                break
        if not isonboard(x,y):
            continue
        if board[x][y] == pawn:
            while True:
                x -= xdirection
                y -= ydirection
                if x == x0 and y == y0:
                    break
                flip.append([x,y])
    return flip

def legal_move(board,player,x,y):
    if not flip_pawn(board,player,x,y):
        return False
    else:
        return True

def check_is_any_legal_move(board,info,player):
    for [x,y] in info:
        if legal_move(board,player,x,y):
            return True
    return False

def get_possible_moves(board, player,info):
    possible_moves = []
    for [x,y] in info:
        if legal_move(board,player,x,y):
            possible_moves.append([x,y])
    random.shuffle(possible_moves)
    return possible_moves

def score(board):
    black = 0
    white = 0
    for i in range(1,9):
        for j in range(1,9):
            if board[i][j] == 1:
                black += 1
            elif board[i][j] == 2:
                white += 1
    return black,white

def gameover(board,info):
    if not info:
        return True
    game = 0
    for p in ['black','white']:
        if not check_is_any_legal_move(board,info,p):
            game += 1
    if game == 2:
        return True
    return False


"""EVA"""
evaluation_eva = [
    [120,2,20,10,10,20,2,120],
    [2,1,3,3,3,3,1,2],
    [20,3,15,5,5,15,3,20],
    [10,3,5,5,5,5,3,10],
    [10,3,5,5,5,5,3,10],
    [20,3,15,5,5,15,3,20],
    [2,1,3,3,3,3,1,2],
    [120,2,20,10,10,20,2,120]
]
evaluation_eva=np.array(evaluation_eva)


def move_evaluation(board,player,info,eva=evaluation_eva):
    possible_moves = get_possible_moves(board,player,info)
    random.shuffle(possible_moves)
    result0 = 0
    move = [None,None]
    if len(possible_moves) != 0:
        for [x0,y0] in possible_moves:
            x = x0 - 1
            y = y0 - 1
            result0 = max(result0,eva[x][y])
            if result0 == eva[x][y]:
                move = [x0,y0]
            else:
                move = random.choice([[x0,y0],move])
        return move
    else:
        return None,None


"""MCTS"""
evaluation=[
        [0,0,0,0,0,0,0,0,0,0],
        [0,5,1,3,3,3,3,1,5,0],
        [0,1,1,2,2,2,2,1,1,0],
        [0,3,2,4,4,4,4,2,3,0],
        [0,3,2,4,1,1,4,2,3,0],
        [0,3,2,4,1,1,4,2,3,0],
        [0,3,2,4,4,4,4,2,3,0],
        [0,1,1,2,2,2,2,1,2,0],
        [0,5,1,3,3,3,3,1,5,0],
        [0,0,0,0,0,0,0,0,0,0],
    ]
evaluation=np.array(evaluation)
"""evaluation function"""
def evaluate(board,player,info,eva=evaluation):
    """socre of board"""
    x = deepcopy(board)
    x[x==2] = -1
    xsum =eva*x
    scores = xsum.sum() * 0.3

    """score of mobility of opposite player"""
    if player == 'black':
        mobility = -5*len(get_possible_moves(board,'white',info))
    else:
        mobility = 5*len(get_possible_moves(board,'black',info))
    mobility = mobility * 0.15

    """score of pieces"""
    number = 0
    b,w = score(board)
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
    z = scores + mobility + number + corner

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
        return len(self.children) == len(get_possible_moves(self.board,self.player,self.info))

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
def move_eva(board,player,info,eva=evaluation):
    """get moves"""
    possible_moves = get_possible_moves(board,player,info)
    result0 = 0
    move = [None,None]
    """choose a move based on the evaluation matrix"""
    if len(possible_moves) != 0:
        for [x,y] in possible_moves:
            result0 = max(result0,eva[x][y])
            if result0 == eva[x][y]:
                move = [x,y]
            else:
                # move = random.choice([[x,y],move])
                move = move
                # flag = random.random()
                # if flag < 0.5:
                #     move = [x,y]
                # else:
                #     move = move

        return move
    else:
        return None,None


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
    while not gameover(board,info):
        x,y = move_eva(board,player,info,eva)
        if [x,y]!=[None,None]:
            if player == 'black':
                board[x][y] = 1
                info.remove([x,y])
                for i,j in flip_pawn(board,player,x,y):
                    board[i][j] = 1
                player = 'white'
            else:
                board[x][y] = 2
                info.remove([x,y])
                for i,j in flip_pawn(board,player,x,y):
                    board[i][j] = 2
                player = 'black'

        if player=='black':
            if not check_is_any_legal_move(board,info,'black'):
                player='white'
        elif player=='white':
            if not check_is_any_legal_move(board,info,'white'):
                player='black'
    """get the result"""
    b,w = score(board)
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
def move_MCTS(in_board,in_player,in_info,hype_parameter,max_iter=1000):
    """restore input data"""
    board = deepcopy(in_board)
    player = deepcopy(in_player)
    info = deepcopy(in_info)
    root = Node(board,player,info,hype_parameter)

    """some basic actions"""
    '''get the possible moves'''
    tem_moves = get_possible_moves(in_board,in_player,in_info)
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
            for i,j in flip_pawn(kill_board,player,x,y):
                kill_board[i][j]=1
            if gameover(kill_board,kill_info):
                b,w = score(kill_board)
                if b>w:
                    print('kill')
                    return [x,y]
        else:
            kill_board[x][y]=2
            kill_info.remove([x,y])
            for i,j in flip_pawn(kill_board,player,x,y):
                kill_board[i][j]=2
            if gameover(kill_board,kill_info):
                b,w = score(kill_board)
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
            for i,j in flip_pawn(skip_board,player,x,y):
                skip_board[i][j]=1
            if not check_is_any_legal_move(skip_board,skip_info,'white'):
                print('skip')
                return [x,y]
        else:
            skip_board[x][y]=2
            skip_info.remove([x,y])
            for i,j in flip_pawn(skip_board,player,x,y):
                skip_board[i][j]=2
            if not check_is_any_legal_move(skip_board,skip_info,'black'):
                print('skip')
                return [x,y]


    """start mcts"""
    for i in range(max_iter):
        """add all possible moves to root"""
        if not root.fully_expanded():
            possible_moves = get_possible_moves(root.board,root.player,root.info)
            random.shuffle(possible_moves)
            for move in possible_moves:
                root.add_child(root.board,root.player,root.info,hype_parameter,move)
            for child in root.children:
                if child.player == 'black':
                    child.board[child.move[0]][child.move[1]] = 1
                    child.info.remove(child.move)
                    for x,y in flip_pawn(child.board,child.player,child.move[0],child.move[1]):
                        child.board[x][y] = 1
                else:
                    child.board[child.move[0]][child.move[1]] = 2
                    child.info.remove(child.move)
                    for x,y in flip_pawn(child.board,child.player,child.move[0],child.move[1]):
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
        if not gameover(root.best_child().board,root.best_child().info) and \
                check_is_any_legal_move(root.best_child().board,root.best_child().info,opposite_player):
            if not len(root.best_child().children) == len(get_possible_moves(root.best_child().board,opposite_player,root.best_child().info)):
                possible_moves_opposite = get_possible_moves(root.best_child().board,opposite_player,root.best_child().info)
                random.shuffle(possible_moves_opposite)
                for move in possible_moves_opposite:
                    root.best_child().add_child(root.best_child().board,opposite_player,root.best_child().info,hype_parameter,move)
                for child in root.best_child().children:
                    if child.player == 'black':
                        child.board[child.move[0]][child.move[1]] = 1
                        child.info.remove(child.move)
                        for x,y in flip_pawn(child.board,child.player,child.move[0],child.move[1]):
                            child.board[x][y] = 1
                    else:
                        child.board[child.move[0]][child.move[1]] = 2
                        child.info.remove(child.move)
                        for x,y in flip_pawn(child.board,child.player,child.move[0],child.move[1]):
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
            if gameover(root.best_child().board,root.best_child().info):
                black_score,white_score = score(root.best_child().board)
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


"""CSV File Function"""
def mkcsv(path,data):
    file = os.path.exists(path)
    columns=['Hype Parameter','MCTS Win','MCTS Lose','Draw']
    if not file:
        df = pd.DataFrame(data=[data],columns=columns)
        df.to_csv(path,index=False)
    else:
        df = pd.DataFrame(data=[data],columns=columns)
        df.to_csv(path,index=False,mode='a',header=False)

dirpath = 'D:\\Durham\\Project\\code\\AI\\MCTS_HP_TEST_DATA'
csv_path = dirpath + '\\MCTS_HP_TEST_DATA' + '_500_' +\
                      str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.csv'
"""loop HP"""
# aaa = list(np.arange(3.5,4,0.1))
# hype_parameter_list = []
# for iii in aaa:
#     hype_parameter_list.append(round(iii,1))
#     0.4,2.3,3.3,4.4
hype_parameter_list = [4.4]
"""test"""
for temp_HP in hype_parameter_list:
    print('HP:',temp_HP)
    MCTS_play ='black'
    EVA_play ='white'
    MCTS_win=0
    MCTS_lose=0
    Draw=0
    for iiiii in range(1000):
        print('Test round:',iiiii)
        print('MCTS_Win:',MCTS_win,'MCTS_Lose:',MCTS_lose,'Draw:',Draw)
        """set game"""
        test_board=restnewboard()
        test_info=[]
        for xxxx in range(1,9):
            for yyyy in range(1,9):
                if [xxxx,yyyy] not in [[4,4],[4,5],[5,4],[5,5]]:
                    test_info.append([xxxx,yyyy])

        """play game"""
        while True:
            if MCTS_play == 'black':
                """black turn"""
                if check_is_any_legal_move(test_board,test_info,'black'):
                    xx,yy=move_MCTS(test_board,'black',test_info,temp_HP)
                    if [xx,yy]!=[None,None]:
                        test_board[xx][yy]=1
                        test_info.remove([xx,yy])
                        for pp,qp in flip_pawn(test_board,'black',xx,yy):
                            test_board[pp][qp]=1

                    if gameover(test_board,test_info):
                        bb,ww = score(test_board)
                        if bb > ww:
                            MCTS_win += 1
                        elif bb < ww:
                            MCTS_lose += 1
                        else:
                            Draw += 1
                        break

                """white turn"""
                if check_is_any_legal_move(test_board,test_info,'white'):
                    xx,yy=move_evaluation(test_board,'white',test_info)
                    if [xx,yy]!=[None,None]:
                        test_board[xx][yy]=2
                        test_info.remove([xx,yy])
                        for pp,qp in flip_pawn(test_board,'white',xx,yy):
                            test_board[pp][qp]=2

                    if gameover(test_board,test_info):
                        bb,ww = score(test_board)
                        if bb > ww:
                            MCTS_win += 1
                        elif bb < ww:
                            MCTS_lose += 1
                        else:
                            Draw += 1
                        break

            else:
                """black turn"""
                if check_is_any_legal_move(test_board,test_info,'black'):
                    xx,yy=move_evaluation(test_board,'black',test_info)
                    if [xx,yy]!=[None,None]:
                        test_board[xx][yy]=1
                        test_info.remove([xx,yy])
                        for pp,qp in flip_pawn(test_board,'black',xx,yy):
                            test_board[pp][qp]=1

                    if gameover(test_board,test_info):
                        bb,ww = score(test_board)
                        if bb > ww:
                            MCTS_lose += 1
                        elif bb < ww:
                            MCTS_win += 1
                        else:
                            Draw += 1
                        break

                """white turn"""
                if check_is_any_legal_move(test_board,test_info,'white'):
                    xx,yy=move_MCTS(test_board,'white',test_info,temp_HP)
                    if [xx,yy]!=[None,None]:
                        test_board[xx][yy]=2
                        test_info.remove([xx,yy])
                        for pp,qp in flip_pawn(test_board,'white',xx,yy):
                            test_board[pp][qp]=2

                    if gameover(test_board,test_info):
                        bb,ww = score(test_board)
                        if bb > ww:
                            MCTS_lose += 1
                        elif bb < ww:
                            MCTS_win += 1
                        else:
                            Draw += 1
                        break

        MCTS_play,EVA_play = EVA_play,MCTS_play

    Data = [temp_HP,MCTS_win,MCTS_lose,Draw]
    mkcsv(csv_path,Data)
