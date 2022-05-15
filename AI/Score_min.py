#Liangyz
#2022/5/15  17:00

import main
import random


def move_score(board,player,info):
    possible_moves = main.get_possible_moves(board,player,info)
    conner = [(1,1),(1,8),(8,1),(8,8)]
    set_p = set(conner) & set(possible_moves)
    if set_p:
        return random.choice(list(set_p))
    tem_board = board.copy()
    score_0 = -1
    move = []
    for [x,y] in possible_moves:
        if player == 'black':
            tem_board[x][y] = 1
            for i,j in main.flip_pawn(board,'black',x,y):
                tem_board[i][j] = 1
            tem_score = main.score(tem_board)
            if score_0 > tem_score[0]:
                score_0 = tem_score[0]
                move = [x,y]
            elif score_0 == tem_score[0]:
                move = random.choice([[x,y],[move[0],move[1]]])
            elif score_0 < tem_score[0]:
                pass

        elif player == 'white':
            tem_board[x][y] = 2
            for i,j in main.flip_pawn(board,'white',x,y):
                tem_board[i][j] = 2
            tem_score = main.score(tem_board)
            if score_0 < tem_score[1]:
                score_0 = tem_score[1]
                move = [x,y]
            elif score_0 == tem_score[1]:
                move = random.choice([[x,y],[move[0],move[1]]])
            elif score_0 > tem_score[1]:
                pass
    return move
