#Liangyz
#2022/7/21  12:29

import numpy as np
import random

class Game(object):
    def __init__(self):
        self.board = np.zeros((8,8))

        self.board[3][3]= 1
        self.board[4][4]= 1
        self.board[3][4]= -1
        self.board[4][3]= -1

        self.info=[]
        for x in range(0,8):
            for y in range(0,8):
                if [x,y] not in [[3,3],[3,4],[4,3],[4,4]]:
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
            for i in range(0,8):
                for j in range(0,8):
                    if self.board[i][j]==1:
                        black+=1
                    elif self.board[i][j]==-1:
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
            other=-1
        else:
            pawn=-1
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
        if x<0 or x>7 or y<0 or y>7:
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

    def Move(self,action,player):
        action = [action//8, action%8]
        x,y=action
        if [x,y] != [8,0]:
            if player=='black':
                self.board[x][y] = 1
                self.info.remove([x,y])
                for i,j in self.flip_pawn(player,x,y):
                    self.board[i][j] = 1
            else:
                self.board[x][y] = -1
                self.info.remove([x,y])
                for i,j in self.flip_pawn(player,x,y):
                    self.board[i][j] = -1
        else:
            pass

    def Get_State(self):
        return self.board.flatten()


# def legal_move(board,player,x,y):
#     if not flip_pawn(board,player,x,y):
#         return False
#     else:
#         return True
#
# def flip_pawn(board,player,x0,y0):
#     flip=[]
#     if player=='black':
#         pawn=1
#         other=-1
#     else:
#         pawn=-1
#         other=1
#     direction=[[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
#     for xdirection,ydirection in direction:
#         x=x0
#         y=y0
#         x+=xdirection
#         y+=ydirection
#         if not isonboard(x,y):
#             continue
#         while board[x][y]==other:
#             x+=xdirection
#             y+=ydirection
#             if not isonboard(x,y):
#                 break
#         if not isonboard(x,y):
#             continue
#         if board[x][y]==pawn:
#             while True:
#                 x-=xdirection
#                 y-=ydirection
#                 if x==x0 and y==y0:
#                     break
#                 flip.append([x,y])
#     return flip
#
# def isonboard(x,y):
#     if x<0 or x>7 or y<0 or y>7:
#         return False
#     else:
#         return True
#
# def get_possible_moves(board,player,info):
#     possible_moves=[]
#     for [x,y] in info:
#         if legal_move(board,player,x,y):
#             possible_moves.append([x,y])
#     random.shuffle(possible_moves)
#     return possible_moves

