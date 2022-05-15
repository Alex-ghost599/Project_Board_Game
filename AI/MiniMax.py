#Liangyz
#2022/5/10  2:02

import main
import random

def move_minimax(board, depth, player,info):
    if depth == 0 or main.gameover(board, info):
        return
    possible_moves = main.get_possible_moves(board,player,info)
    conner = [(1,1),(1,8),(8,1),(8,8)]
    set_p = set(conner) & set(possible_moves)
    if set_p:
        return random.choice(list(set_p))
    tem_board = board.copy()
    tem_info = info.copy()
    score_0 = -1
    move = []

    while depth > 0:
        depth -= 1
        for [x, y] in possible_moves:
            if player == 'black':
                tem_board[x][y] = 1
                for i,j in main.flip_pawn(tem_board, 'black', x, y):
                    tem_board[i][j] = 1
                tem_score = main.score(tem_board)
                if score_0 < tem_score[0]:
                    score_0 = tem_score[0]
                    move = [x,y]
                elif score_0 == tem_score[0]:
                    move = random.choice([[x,y],[move[0],move[1]]])
                elif score_0 > tem_score[0]:
                    pass
                player = 'white'
                move_minimax(tem_board,depth,player,tem_info)


