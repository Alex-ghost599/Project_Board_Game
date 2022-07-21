#Liangyz
#2022/7/21  12:29

import numpy as np
import random

class Game(object):
    def __init__(self):
        self.board = np.zeros((10,10))

        self.board[4][4]= 1
        self.board[5][5]= 1
        self.board[4][5]= 2
        self.board[5][4]= 2

        self.info=[]
        for x in range(1,9):
            for y in range(1,9):
                if [x,y] not in [[4,4],[4,5],[5,4],[5,5]]:
                    self.info.append([x,y])


        # # 更新期盘：1表示黑棋，-1表示白棋
        # for item in self.black_chess:
        #     self.board[item[0]][item[1]] = 1
        # for item in self.white_chess:
        #     self.board[item[0]][item[1]] = -1

    def gameover(self):
        if not self.info:
            return True
        game=0
        for p in ['black','white']:
            if not self.check_is_any_legal_move(p):
                game+=1
        if game==2:
            return True

    def reward(self):
        if self.gameover():
            black=0
            white=0
            for i in range(1,9):
                for j in range(1,9):
                    if self.board[i][j]==1:
                        black+=1
                    elif self.board[i][j]==2:
                        white+=1
            if black>white:
                return 100
            elif black<white:
                return -100
            else:
                return 0
        else:
            return 0

    def check_is_any_legal_move(self,player):
        for [x,y] in self.info:
            if self.legal_move(player,x,y):
                return True
        return False

    def legal_move(self,player,x,y):
        if not self.flip_pawn(player,x,y):
            return False
        else:
            return True

    def flip_pawn(self,player,x0,y0):
        flip=[]
        if player=='black':
            pawn=1
            other=2
        else:
            pawn=2
            other=1
        direction=[[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
        for xdirection,ydirection in direction:
            x=x0
            y=y0
            x+=xdirection
            y+=ydirection
            if not self.isonboard(x,y):
                continue
            while self.board[x][y]==other:
                x+=xdirection
                y+=ydirection
                if not self.isonboard(x,y):
                    break
            if not self.isonboard(x,y):
                continue
            if self.board[x][y]==pawn:
                while True:
                    x-=xdirection
                    y-=ydirection
                    if x==x0 and y==y0:
                        break
                    flip.append([x,y])
        return flip

    def isonboard(self,x,y):
        if x<1 or x>8 or y<1 or y>8:
            return False
        else:
            return True

    def get_possible_moves(self,player):
        possible_moves=[]
        for [x,y] in self.info:
            if self.legal_move(player,x,y):
                possible_moves.append([x,y])
        random.shuffle(possible_moves)
        return possible_moves

    def Reverse(self,action,player):
        x,y=action
        if [x,y] != [None,None]:
            if player=='black':
                self.board[x][y] = 1
                self.info.remove([x,y])
                for i,j in self.flip_pawn(player,x,y):
                    self.board[i][j] = 1

    def Get_State(self):
        return np.array(self.board, dytpe=np.int).flatten()