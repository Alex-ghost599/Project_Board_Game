#Liangyz
#2022/5/17  0:16

from copy import deepcopy

import main
import random
import numpy as np


path = r"AI/HASH/Alpha_beta_Hash.npy"
hash_board_map = np.load(path, allow_pickle=True).item()
tem_hash_board_map = deepcopy(hash_board_map)

# set hash function
def set_hash_board(board, current, depth, alpha, beta, score, move):
    tem_hash_board_map[tuple([tuple([0 if piece == 0 else (1 if piece == current else -1) for piece in line]) for line in board] + [depth, alpha, beta])] = (score, move)

def get_hash_board(board, current, depth, alpha, beta):
    key = tuple([tuple([0 if piece == 0 else (1 if piece == current else -1) for piece in line]) for line in board] + [depth, alpha, beta])
    return tem_hash_board_map.get(key)

# evaluate function and matrix
evaluation = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,120,2,20,10,10,20,2,120,0],
    [0,2,1,3,3,3,3,1,2,0],
    [0,20,3,15,5,5,15,3,20,0],
    [0,10,3,5,5,5,5,3,10,0],
    [0,10,3,5,5,5,5,3,10,0],
    [0,20,3,15,5,5,15,3,20,0],
    [0,2,1,3,3,3,3,1,2,0],
    [0,120,2,20,10,10,20,2,120,0],
    [0,0,0,0,0,0,0,0,0,0],
]
evaluation=np.array(evaluation)

def evaluate(board,player,info,eva=evaluation):
    #using evaluation matrix(black want positive_big, white want negative_small)
    x = deepcopy(board)
    x[x == 2] = -1
    xe = eva * x
    score = xe.sum() * 0.30

    #using mobility of opposite player(less mobility, more score)
    if player == 'black':
        mobility = 15 * len(main.get_possible_moves(board,player,info))
    else:
        mobility = -15 * len(main.get_possible_moves(board,player,info))
    mobility = mobility * 0.15

    #using the number of pieces of opposite player
    # (more pieces, more score) for fist 42 steps
    # (less pieces, more score) for last 18 steps
    number = 0
    b,w = main.score(board)
    if len(info) >18:
        if player == 'black':
            number = (b-w) * -12
        elif player == 'white':
            number = (w-b) * 12
    elif len(info) <=18:
        if player == 'black':
            number = (w-b) * -12
        elif player == 'white':
            number = (b-w) * 12
    number = number * 0.3

    # using the number of pieces at corner and near corner
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
            corner += board[corner_i][corner_j+dy]*-10
            corner += board[corner_i+dx][corner_j]*-10
            corner += board[corner_i+dx][corner_j+dy]*-15

            corner += board[corner_i][corner_j+(2*dy)]*10
            corner += board[corner_i+dx][corner_j+(2*dy)]*10
            corner += board[corner_i+(2*dx)][corner_j]*10
            corner += board[corner_i+(2*dx)][corner_j+dy]*10
            corner += board[corner_i+(2*dx)][corner_j+(2*dy)]*15

    corner = corner * 0.25
    return score + number + mobility + corner

# main function
def move_Alpha_beta_hash(board, depth, player,info,
                    end:bool,x=None,y=None,alpha=-99999999,beta=99999999,eva=evaluation):
    # print(hash_board_map)
    # set the current player as black = 1 or white = 2 for hash_board_map
    if player == 'black':
        current = 1
    else:
        current = 2
    # check if input information is calculated before as in hash_board_map
    hash_value = get_hash_board(board, current, depth, alpha, beta)
    # if yes, return the value
    if hash_value:
        if end:
            # print('use hash')
            return hash_value[1]
        else:
            return hash_value[0]
    # save the input information as for hash_board_map
    save_board = deepcopy(board)
    save_depth = depth
    save_alpha = alpha
    save_beta = beta

    # set temporary game board and info
    tem0_board = deepcopy(board)
    tem0_info = deepcopy(info)

    # make move if input has x,y coordinate
    if x != None and y != None:
        if player == 'white':
            tem0_board[x][y] = 1
            tem0_info.remove([x, y])
            for i,j in main.flip_pawn(tem0_board, 'black', x, y):
                tem0_board[i][j] = 1
        elif player == 'black':
            tem0_board[x][y] = 2
            tem0_info.remove([x, y])
            for i,j in main.flip_pawn(tem0_board, 'white', x, y):
                tem0_board[i][j] = 2

    # if reach the end of depth, return the evaluation
    if depth == 0 or main.gameover(tem0_board, tem0_info):

        # print(evaluate(tem0_board),player,'0')
        return evaluate(tem0_board,player,info)

    # get all possible
    tem_possible_moves = main.get_possible_moves(tem0_board,player,tem0_info)
    possible_moves = []
    # order the possible moves as high score to low score
    while len(tem_possible_moves) != 0:
        i = 0
        tem_max_possible = []
        for [x,y] in tem_possible_moves:
            i = max(i,eva[x][y])
            if i == eva[x][y]:
                tem_max_possible = [x,y]
            else:
                tem_max_possible = tem_max_possible

            #check if move can end the game, if yes, return the move
            kill_game_board = deepcopy(board)
            if end:
                if player == 'black':
                    kill_game_board[x][y] = 1
                    for i,j in main.flip_pawn(kill_game_board, 'black', x, y):
                        kill_game_board[i][j] = 1
                    if 2 in kill_game_board:
                        pass
                    else:
                        # print('use kill')
                        return [x,y]
                elif player == 'white':
                    kill_game_board[x][y] = 2
                    for i,j in main.flip_pawn(kill_game_board, 'white', x, y):
                        kill_game_board[i][j] = 2
                    if 1 in kill_game_board:
                        pass
                    else:
                        # print('use kill')
                        return [x,y]


        possible_moves.append(tuple(tem_max_possible))
        tem_possible_moves.remove(tem_max_possible)

    # check if the possible moves contains the corner, if yes, return the move
    conner = [(1,1),(1,8),(8,1),(8,8)]
    set_p = set(conner) & set(possible_moves)
    if set_p:
        if end:
            # print('use conner')
            return random.choice(list(set_p))

    # main loop
    move = [None, None]

    while depth > 0:
        depth -= 1
        if player == 'black':
            score= -99999
            for [x, y] in possible_moves:
                # print('thinking',x,y)
                tem_score = move_Alpha_beta_hash(tem0_board,depth,'white',tem0_info,False,x,y,alpha,beta)
                # print(tem_score)

                score = max(score,tem_score)
                if score == tem_score:
                    move = [x,y]
                else:
                    move = move

                alpha = max(alpha,tem_score)
                if beta <= alpha:
                    # print('pruned')
                    break


            if end:
                set_hash_board(save_board, current, save_depth, save_alpha, save_beta, score, move)
                # np.save(path,hash_board_map)
                return move
            else:
                # print(score,'black')
                return score



        elif player == 'white':
            score = 99999
            for [x, y] in possible_moves:
                # print('thinking',x,y)
                tem_score = move_Alpha_beta_hash(tem0_board,depth,'black',tem0_info,False,x,y,alpha,beta)

                score = min(score,tem_score)
                if score == tem_score:
                    move = [x,y]
                else:
                    move = move

                beta = min(beta,tem_score)
                if beta <= alpha:
                    # print('pruned')
                    break


            if end:
                # save the corresponding inputted information and outputted move to the hash table
                set_hash_board(save_board, current, save_depth, save_alpha, save_beta, score, move)
                # print(hash_board_map)
                # file=open(path,'w')
                # file.write(str(hash_board_map))
                # file.close()
                # np.save(path,hash_board_map)
                return move
            else:
                # print(score,'white')
                return score
