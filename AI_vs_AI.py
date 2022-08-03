#Liangyz
#2022/5/2  18:41
from copy import deepcopy

import os
import numpy as np
import pygame
import main
import time
from decimal import Decimal
import menu
import sys
# sys.path.append('/AI/')
import AI.Random
import AI.Evaluate
import AI.Score_max
import AI.Score_min
import AI.MiniMax
import AI.Alpha_beta
import AI.Alpha_beta_Hash
import AI.MCTS
import AI.DQN_run

BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
a_b_depth = 4
a_b_hash_depth = 5
hype_parameter = 2.7
def aivsai(player1,player2,number_of_rounds,data_collection,times=None):
    # background
    main.surface.blit(main.gameboard,(375,50))
    #stop button
    stop_rect = main.surface.blit(main.stopbutton,(375,770))
    text_stop_rect = main.text_stop.get_rect()
    text_stop_rect.center = stop_rect.center
    main.surface.blit(main.text_stop,text_stop_rect)


    #set new board and put pawn on board
    board = main.restnewboard()
    info = []
    for x in range(1,9):
        for y in range(1,9):
            if [x,y] not in [[4,4],[4,5],[5,4],[5,5]]:
                info.append([x,y])
            if board[x][y] == 1:
                main.surface.blit(main.gamepawn_black,
                                  (y*main.cell_size[0]+main.space_size[0]+375,
                                   x*main.cell_size[1]+main.space_size[1]+50))
            elif board[x][y] == 2:
                main.surface.blit(main.gamepawn_white,
                                  (y*main.cell_size[0]+main.space_size[0]+375,
                                   x*main.cell_size[1]+main.space_size[1]+50))

        pygame.display.update()
        main.Runingclock.tick(main.fps)
    #prameter
    turn = 'black'
    NOR = number_of_rounds
    game_over_flag = True
    #data_collection_parameter
    gametime_start=time.time()
    black_movetime_list = []
    white_movetime_list = []
    black_action_list = []
    white_action_list = []


    #main loop
    running = True
    while running:
        for event in pygame.event.get():
            #quit
            if event.type == pygame.QUIT:
                main.exit_game()
            #get mouse position
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     print(event.pos)

            # restart game
            if event.type == pygame.MOUSEBUTTONDOWN and \
                    event.pos[0] in range(1095, 1172) and \
                        event.pos[1] in range(50, 125):
                return aivsai(player1,player2,number_of_rounds,data_collection)

            # return to menu
            if event.type == pygame.MOUSEBUTTONDOWN and \
                event.pos[0] in range(1095, 1176) and \
                        event.pos[1] in range(770, 851):
                # menu.main_menu()
                main.number_of_win_black = 0
                main.number_of_win_white = 0
                main.Draw = 0
                return

            # stop game
            if event.type == pygame.MOUSEBUTTONDOWN and \
                    event.pos[0] in range(375, 456) and \
                        event.pos[1] in range(770, 851):
                #resume button
                resume_rect=main.surface.blit(main.resumebutton,(375,770))
                text_resume_rect=main.text_resume.get_rect()
                text_resume_rect.center=resume_rect.center
                main.surface.blit(main.text_resume,text_resume_rect)

                pygame.display.update()
                main.Runingclock.tick(main.fps)

                flag = True
                while flag:
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            main.exit_game()
                        # restart game
                        if event.type==pygame.MOUSEBUTTONDOWN and\
                                event.pos[0] in range(1095,1172) and\
                                event.pos[1] in range(50,125):
                            return aivsai(player1,player2,number_of_rounds,data_collection)
                        # return to menu
                        if event.type==pygame.MOUSEBUTTONDOWN and\
                                event.pos[0] in range(1095,1176) and\
                                event.pos[1] in range(770,851):
                            # menu.main_menu()
                            main.number_of_win_black=0
                            main.number_of_win_white=0
                            main.Draw=0
                            return
                        if event.type == pygame.MOUSEBUTTONDOWN and \
                                event.pos[0] in range(375, 456) and \
                                    event.pos[1] in range(770, 851):
                            flag = False

                            stop_rect=main.surface.blit(main.stopbutton,(375,770))
                            text_stop_rect=main.text_stop.get_rect()
                            text_stop_rect.center=stop_rect.center
                            main.surface.blit(main.text_stop,text_stop_rect)

                            pygame.display.update()
                            main.Runingclock.tick(main.fps)

                            break
                        else:
                            time.sleep(0.01)


        #show whose turn
        if turn=='black':
            main.surface.blit(main.gamepawn_black,(385,60))
        elif turn=='white':
            main.surface.blit(main.gamepawn_white,(385,60))

        pygame.display.update()
        main.Runingclock.tick(main.fps)



        # make move--------------------------------------------------------------------------------
        gameover = main.gameover(board,info)

        if not gameover:

            #for black:
            if turn == 'black':
                if player1 == 1:
                    black_move_time_start=time.time()
                    x,y = AI.Random.move_random(board,turn,info)
                    black_move_time_end=time.time()
                    if [x,y] != [None,None]:
                        black_action_list.append([x,y])
                        board[x][y] = 1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j] = 1
                        turn = 'white'

                elif player1 == 2:
                    black_move_time_start=time.time()
                    x,y = AI.Evaluate.move_eva(board,turn,info)
                    black_move_time_end=time.time()
                    if [x,y] != [None,None]:
                        black_action_list.append([x,y])
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=1
                        turn='white'

                elif player1 == 3:
                    black_move_time_start=time.time()
                    x,y=AI.Score_max.move_score(board,turn,info)
                    black_move_time_end=time.time()
                    if [x,y]!=[None,None]:
                        black_action_list.append([x,y])
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=1
                        turn='white'

                elif player1 == 4:
                    black_move_time_start=time.time()
                    x,y=AI.Score_min.move_score(board,turn,info)
                    black_move_time_end=time.time()
                    if [x,y]!=[None,None]:
                        black_action_list.append([x,y])
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=1
                        turn='white'

                elif player1 == 5:
                    black_move_time_start=time.time()
                    x,y=AI.MiniMax.move_minimax(board,4,turn,info,True)
                    black_move_time_end=time.time()
                    if [x,y]!=[None,None]:
                        black_action_list.append([x,y])
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=1
                        turn='white'

                elif player1 == 6:
                    black_move_time_start=time.time()
                    x,y=AI.Alpha_beta.move_Alpha_beta(board,a_b_depth,turn,info,True)
                    black_move_time_end=time.time()
                    if [x,y]!=[None,None]:
                        black_action_list.append([x,y])
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=1
                        turn='white'

                elif player1 == 7:
                    black_move_time_start=time.time()
                    x,y=AI.Alpha_beta_Hash.move_Alpha_beta_hash(board,a_b_hash_depth,turn,info,True)
                    black_move_time_end=time.time()
                    if [x,y]!=[None,None]:
                        black_action_list.append([x,y])
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=1
                        turn='white'

                elif player1 == 8:
                    black_move_time_start=time.time()
                    x,y=AI.MCTS.move_MCTS(board,turn,info,hype_parameter)
                    black_move_time_end=time.time()
                    if [x,y]!=[None,None]:
                        black_action_list.append([x,y])
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=1
                        turn='white'

                elif player1 == 9:
                    black_move_time_start=time.time()
                    x,y=AI.DQN_run.DQN_move(board,turn,info)
                    black_move_time_end=time.time()
                    if [x,y]!=[None,None]:
                        black_action_list.append([x,y])
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=1
                        turn='white'


                black_move_time_s = str(black_move_time_end - black_move_time_start)
                # print('black move time:',black_move_time_s)
                black_move_time_d = Decimal(black_move_time_s).quantize(Decimal('0.001'),rounding='ROUND_HALF_UP')
                # print('black move time:',black_move_time_d)
                # print(type(black_move_time_d))
                black_movetime_list.append(float(black_move_time_d))



            #for white
            elif turn == 'white':
                if player2 == 1:
                    white_move_time_start=time.time()
                    x,y = AI.Random.move_random(board,turn,info)
                    white_move_time_end=time.time()
                    if [x,y] != [None,None]:
                        white_action_list.append([x,y])
                        board[x][y] = 2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j] = 2
                        turn = 'black'

                elif player2 == 2:
                    white_move_time_start=time.time()
                    x,y = AI.Evaluate.move_eva(board,turn,info)
                    white_move_time_end=time.time()
                    if [x,y] != [None,None]:
                        white_action_list.append([x,y])
                        board[x][y] = 2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j] = 2
                        turn='black'

                elif player2 == 3:
                    white_move_time_start=time.time()
                    x,y=AI.Score_max.move_score(board,turn,info)
                    white_move_time_end=time.time()
                    if [x,y]!=[None,None]:
                        white_action_list.append([x,y])
                        board[x][y]=2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=2
                        turn='black'

                elif player2 == 4:
                    white_move_time_start=time.time()
                    x,y=AI.Score_min.move_score(board,turn,info)
                    white_move_time_end=time.time()
                    if [x,y]!=[None,None]:
                        white_action_list.append([x,y])
                        board[x][y]=2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=2
                        turn='black'

                elif player2 == 5:
                    white_move_time_start=time.time()
                    x,y=AI.MiniMax.move_minimax(board,4,turn,info,True)
                    white_move_time_end=time.time()
                    if [x,y]!=[None,None]:
                        white_action_list.append([x,y])
                        board[x][y]=2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=2
                        turn='black'

                elif player2 == 6:
                    white_move_time_start=time.time()
                    x,y=AI.Alpha_beta.move_Alpha_beta(board,a_b_depth,turn,info,True)
                    white_move_time_end=time.time()
                    if [x,y]!=[None,None]:
                        white_action_list.append([x,y])
                        board[x][y]=2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=2
                        turn='black'

                elif player2 == 8:
                    white_move_time_start=time.time()
                    x,y=AI.MCTS.move_MCTS(board,turn,info,hype_parameter)
                    white_move_time_end=time.time()
                    if [x,y]!=[None,None]:
                        white_action_list.append([x,y])
                        board[x][y]=2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=2
                        turn='black'

                elif player2 == 7:
                    white_move_time_start=time.time()
                    x,y=AI.Alpha_beta_Hash.move_Alpha_beta_hash(board,a_b_hash_depth,turn,info,True)
                    white_move_time_end=time.time()
                    if [x,y]!=[None,None]:
                        white_action_list.append([x,y])
                        board[x][y]=2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=2
                        turn='black'

                elif player2 == 9:
                    white_move_time_start=time.time()
                    x,y=AI.DQN_run.DQN_move(board,turn,info)
                    white_move_time_end=time.time()
                    if [x,y]!=[None,None]:
                        white_action_list.append([x,y])
                        board[x][y]=2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=2
                        turn='black'


                white_move_time_s = str(white_move_time_end - white_move_time_start)
                # print('white move time:',white_move_time_s)
                white_move_time_d = Decimal(white_move_time_s).quantize(Decimal('0.001'),rounding='ROUND_HALF_UP')
                # print('white move time:',white_move_time_d)
                white_movetime_list.append(float(white_move_time_d))




            #check is there any legal move for both player
            if turn == 'black':
                if not main.check_is_any_legal_move(board,info,'black'):
                    turn = 'white'
            elif turn == 'white':
                if not main.check_is_any_legal_move(board,info,'white'):
                    turn = 'black'


        else:
            main.show_score(main.socreboard,board)
            if number_of_rounds != 0:
                number_of_rounds -= 1
                black,white = main.score(board)
                if black > white:
                    main.number_of_win_black += 1
                elif black < white:
                    main.number_of_win_white += 1
                elif black == white:
                    main.Draw += 1

                main.Scoreboard(main.number_of_win_black,
                                main.number_of_win_white,
                                main.Draw)

                if player1==7:
                    if black-white>10:
                        AI.Alpha_beta_Hash.hash_board_map=deepcopy(AI.Alpha_beta_Hash.tem_hash_board_map)
                        np.save(AI.Alpha_beta_Hash.path,AI.Alpha_beta_Hash.hash_board_map)
                    else:
                        AI.Alpha_beta_Hash.tem_hash_board_map=deepcopy(AI.Alpha_beta_Hash.hash_board_map)
                if player2==7:
                    if white-black>10:
                        AI.Alpha_beta_Hash.hash_board_map=deepcopy(AI.Alpha_beta_Hash.tem_hash_board_map)
                        np.save(AI.Alpha_beta_Hash.path,AI.Alpha_beta_Hash.hash_board_map)
                    else:
                        AI.Alpha_beta_Hash.tem_hash_board_map=deepcopy(AI.Alpha_beta_Hash.hash_board_map)

                # black_rect = main.surface.blit(main.winnerboard_b,(50,600))
                # draw_rect = main.surface.blit(main.winnerboard_d,(170,600))
                # white_rect = main.surface.blit(main.winnerboard_w,(290,600))
                #
                # font = pygame.font.SysFont('arial',50)
                #
                # text_black = font.render(str(main.number_of_win_black),True,(0,0,0))
                # text_black_rect = text_black.get_rect()
                # text_black_rect.center = black_rect.center
                #
                # text_white = font.render(str(main.number_of_win_white),True,(0,0,0))
                # text_white_rect = text_white.get_rect()
                # text_white_rect.center = white_rect.center
                #
                # text_draw = font.render(str(main.Draw),True,(0,0,0))
                # text_draw_rect = text_draw.get_rect()
                # text_draw_rect.center = draw_rect.center
                #
                # main.surface.blit(text_black,(text_black_rect))
                # main.surface.blit(text_white,(text_white_rect))
                # main.surface.blit(text_draw,(text_draw_rect))
                #
                # pygame.display.update()
                # main.Runingclock.tick(main.fps)
                if number_of_rounds != 0:
                    return aivsai(player1,player2,number_of_rounds,data_collection)
                elif number_of_rounds == 0:
                    gametime_end = time.time()
                    sec = gametime_end - gametime_start
                    m,s=divmod(sec,60)
                    h,m=divmod(m,60)
                    time_hms = "%d:%02d:%02d"%(h,m,s)

                    time_rect=main.surface.blit(main.time_show,(90,850))
                    font=pygame.font.SysFont('arial',50)
                    time_text = font.render(time_hms,True,(0,0,0))
                    time_text_rect = time_text.get_rect()
                    time_text_rect.center = time_rect.center
                    main.surface.blit(time_text,(time_text_rect))

                    if player1 == 7:
                        if black - white > 10:
                            AI.Alpha_beta_Hash.hash_board_map = deepcopy(AI.Alpha_beta_Hash.tem_hash_board_map)
                            np.save(AI.Alpha_beta_Hash.path,AI.Alpha_beta_Hash.hash_board_map)
                        else:
                            AI.Alpha_beta_Hash.tem_hash_board_map = deepcopy(AI.Alpha_beta_Hash.hash_board_map)
                    if player2 == 7:
                        if white - black > 10:
                            AI.Alpha_beta_Hash.hash_board_map = deepcopy(AI.Alpha_beta_Hash.tem_hash_board_map)
                            np.save(AI.Alpha_beta_Hash.path,AI.Alpha_beta_Hash.hash_board_map)
                        else:
                            AI.Alpha_beta_Hash.tem_hash_board_map = deepcopy(AI.Alpha_beta_Hash.hash_board_map)

                    pygame.display.update()
                    main.Runingclock.tick(main.fps)

            elif NOR == 0 and \
                    game_over_flag:
                if data_collection == 0:
                    black,white=main.score(board)
                    if black>white:
                        main.number_of_win_black+=1
                    elif black<white:
                        main.number_of_win_white+=1
                    elif black==white:
                        main.Draw+=1

                    main.Scoreboard(main.number_of_win_black,
                                    main.number_of_win_white,
                                    main.Draw)
                    game_over_flag = False

                    if player1 == 7:
                        if black - white > 10:
                            AI.Alpha_beta_Hash.hash_board_map = deepcopy(AI.Alpha_beta_Hash.tem_hash_board_map)
                            np.save(AI.Alpha_beta_Hash.path,AI.Alpha_beta_Hash.hash_board_map)
                        else:
                            AI.Alpha_beta_Hash.tem_hash_board_map = deepcopy(AI.Alpha_beta_Hash.hash_board_map)
                    if player2 == 7:
                        if white - black > 10:
                            AI.Alpha_beta_Hash.hash_board_map = deepcopy(AI.Alpha_beta_Hash.tem_hash_board_map)
                            np.save(AI.Alpha_beta_Hash.path,AI.Alpha_beta_Hash.hash_board_map)
                        else:
                            AI.Alpha_beta_Hash.tem_hash_board_map = deepcopy(AI.Alpha_beta_Hash.hash_board_map)
                else:
                    # data collection:
                    if times%2==0:
                        #game_time
                        gametime_end=time.time()
                        sec=gametime_end-gametime_start
                        m,s=divmod(sec,60)
                        game_time="%02d:%02d"%(m,s)

                        #move_time
                        move_time = [black_movetime_list,white_movetime_list]

                        #move_list
                        action_list = [black_action_list,white_action_list]

                        #move_list_count
                        action_list_count = [len(black_action_list),len(white_action_list)]

                        #score
                        black,white=main.score(board)
                        score=[black,white,abs(black-white)]

                        #winner
                        if black>white:
                            winner = 1
                        elif black<white:
                            winner = -1
                        else:
                            winner = 0

                        #board
                        board=np.delete(board,[0,9],axis=1)
                        board=np.delete(board,[0,9],axis=0)
                        board[board==2] = -1
                        board=board.flatten()

                        if player1==7:
                            if black-white>10:
                                AI.Alpha_beta_Hash.hash_board_map=deepcopy(AI.Alpha_beta_Hash.tem_hash_board_map)
                                np.save(AI.Alpha_beta_Hash.path,AI.Alpha_beta_Hash.hash_board_map)
                            else:
                                AI.Alpha_beta_Hash.tem_hash_board_map=deepcopy(AI.Alpha_beta_Hash.hash_board_map)
                        if player2==7:
                            if white-black>10:
                                AI.Alpha_beta_Hash.hash_board_map=deepcopy(AI.Alpha_beta_Hash.tem_hash_board_map)
                                np.save(AI.Alpha_beta_Hash.path,AI.Alpha_beta_Hash.hash_board_map)
                            else:
                                AI.Alpha_beta_Hash.tem_hash_board_map=deepcopy(AI.Alpha_beta_Hash.hash_board_map)

                        return [list(board),game_time,move_time,action_list,action_list_count,score,winner]
                    else:
                        #game_time
                        gametime_end=time.time()
                        sec=gametime_end-gametime_start
                        m,s=divmod(sec,60)
                        game_time="%02d:%02d"%(m,s)

                        #move_time
                        move_time = [white_movetime_list,black_movetime_list]

                        #move_list
                        action_list = [white_action_list,black_action_list]

                        #move_list_count
                        action_list_count = [len(white_action_list),len(black_action_list)]

                        #score
                        black,white=main.score(board)
                        score=[white,black,abs(black-white)]

                        #winner
                        if black>white:
                            winner = -1
                        elif black<white:
                            winner = 1
                        else:
                            winner = 0

                        #board
                        board=np.delete(board,[0,9],axis=1)
                        board=np.delete(board,[0,9],axis=0)
                        board[board==2] = -1
                        board=board.flatten()

                        if player1 == 7:
                            if black - white > 10:
                                AI.Alpha_beta_Hash.hash_board_map = deepcopy(AI.Alpha_beta_Hash.tem_hash_board_map)
                                np.save(AI.Alpha_beta_Hash.path,AI.Alpha_beta_Hash.hash_board_map)
                            else:
                                AI.Alpha_beta_Hash.tem_hash_board_map = deepcopy(AI.Alpha_beta_Hash.hash_board_map)
                        if player2 == 7:
                            if white - black > 10:
                                AI.Alpha_beta_Hash.hash_board_map = deepcopy(AI.Alpha_beta_Hash.tem_hash_board_map)
                                np.save(AI.Alpha_beta_Hash.path,AI.Alpha_beta_Hash.hash_board_map)
                            else:
                                AI.Alpha_beta_Hash.tem_hash_board_map = deepcopy(AI.Alpha_beta_Hash.hash_board_map)

                        return [list(board),game_time,move_time,action_list,action_list_count,score,winner]



        if not gameover:
            # update board
            for x in range(1,9):
                for y in range(1,9):
                    if board[x][y] == 1:
                        main.surface.blit(main.gamepawn_black,
                                          (y*main.cell_size[0]+main.space_size[0]+375,
                                           x*main.cell_size[1]+main.space_size[1]+50))
                    elif board[x][y] == 2:
                        main.surface.blit(main.gamepawn_white,
                                          (y*main.cell_size[0]+main.space_size[0]+375,
                                           x*main.cell_size[1]+main.space_size[1]+50))


        pygame.display.update()
        main.Runingclock.tick(main.fps)
        # print('--------')