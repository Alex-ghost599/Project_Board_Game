#Liangyz
#2022/5/2  18:40

import pygame
import main
import time
import menu
import sys
# sys.path.append('/AI/')
import AI.Random as rm
import AI.Evaluate
import AI.Score_max
import AI.Score_min
import AI.MiniMax
import AI.Alpha_beta
import AI.Alpha_beta_Hash
import AI.MCTS
import AI.DQN_run

a_b_depth = 4
a_b_hash_depth = 5
hype_parameter = 3.2
def pvsai(player1,player2):
    #set human player
    human = True
    if player1 == 0:
        human = True

    elif player2 == 0:
        human = False

    # background
    main.surface.blit(main.gameboard,(375,50))

    #stop button
    stop_rect=main.surface.blit(main.stopbutton,(375,770))
    text_stop_rect=main.text_stop.get_rect()
    text_stop_rect.center=stop_rect.center
    main.surface.blit(main.text_stop,text_stop_rect)

    #set new board and put pawn on board
    board = main.restnewboard()
    info=[]
    for x in range(1,9):
        for y in range(1,9):
            if [x,y] not in [[4,4],[4,5],[5,4],[5,5]]:
                info.append([x,y])

    #prameter
    gameover=False
    turn='black'
    gameover_show=True

    running = True
    while running:
        for event in pygame.event.get():
            #quit
            if event.type==pygame.QUIT:
                main.exit_game()
            # restart
            if event.type==pygame.MOUSEBUTTONDOWN and \
                    event.pos[0] in range(1095,1172) and\
                        event.pos[1] in range(50,125):
                return pvsai(player1,player2)
            # return to main_menu
            if event.type==pygame.MOUSEBUTTONDOWN and \
                    event.pos[0] in range(1095,1176) and\
                        event.pos[1] in range(770,851):
                main.number_of_win_black=0
                main.number_of_win_white=0
                main.Draw=0
                # menu.main_menu()
                return

            # stop game
            if event.type==pygame.MOUSEBUTTONDOWN and\
                    event.pos[0] in range(375,456) and\
                    event.pos[1] in range(770,851):
                #resume button
                resume_rect=main.surface.blit(main.resumebutton,(375,770))
                text_resume_rect=main.text_resume.get_rect()
                text_resume_rect.center=resume_rect.center
                main.surface.blit(main.text_resume,text_resume_rect)

                pygame.display.update()
                main.Runingclock.tick(main.fps)

                flag=True
                while flag:
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            main.exit_game()
                        # restart game
                        if event.type==pygame.MOUSEBUTTONDOWN and\
                                event.pos[0] in range(1095,1172) and\
                                event.pos[1] in range(50,125):
                            return pvsai(player1,player2)
                        # return to menu
                        if event.type==pygame.MOUSEBUTTONDOWN and\
                                event.pos[0] in range(1095,1176) and\
                                event.pos[1] in range(770,851):
                            # menu.main_menu()
                            main.number_of_win_black=0
                            main.number_of_win_white=0
                            main.Draw=0
                            return
                        if event.type==pygame.MOUSEBUTTONDOWN and\
                                event.pos[0] in range(375,456) and\
                                event.pos[1] in range(770,851):
                            flag=False

                            stop_rect=main.surface.blit(main.stopbutton,(375,770))
                            text_stop_rect=main.text_stop.get_rect()
                            text_stop_rect.center=stop_rect.center
                            main.surface.blit(main.text_stop,text_stop_rect)

                            pygame.display.update()
                            main.Runingclock.tick(main.fps)

                            break
                        else:
                            time.sleep(0.01)


            # make move--------------------------------------------------------------------------------
            gameover = main.gameover(board,info)

            if not gameover:
                #show whose turn
                if turn == 'black':
                    main.surface.blit(main.gamepawn_black,(385,60))
                elif turn == 'white':
                    main.surface.blit(main.gamepawn_white,(385,60))

                #for black:
                if turn == 'black' and\
                        event.type == pygame.MOUSEBUTTONDOWN and\
                        event.button == 1 and\
                        human:
                    pos = event.pos
                    for [x,y] in info:
                        if pos[0] in range(375+y*80,375+y*80+80) and\
                                pos[1] in range(50+x*80,50+x*80+80):
                            if main.legal_move(board,'black',x,y):
                                board[x][y]=1
                                info.remove([x,y])
                                for i,j in main.flip_pawn(board,'black',x,y):
                                    board[i][j]=1
                                turn='white'
                                break

                elif turn == 'black' and\
                        not human:
                    if player1 == 1:
                        x,y = rm.move_random(board,'black',info)
                        if [x,y] != [None,None]:
                            board[x][y] = 1
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,'black',x,y):
                                board[i][j] = 1
                            turn = 'white'
                            break
                    elif player1 == 2:
                        x,y=AI.Evaluate.move_eva(board,'black',info)
                        if [x,y]!=[None,None]:
                            board[x][y]=1
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,'black',x,y):
                                board[i][j]=1
                            turn='white'
                            break
                    elif player1 == 3:
                        x,y=AI.Score_max.move_score(board,'black',info)
                        if [x,y]!=[None,None]:
                            board[x][y]=1
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,'black',x,y):
                                board[i][j]=1
                            turn='white'
                            break
                    elif player1 == 4:
                        x,y=AI.Score_min.move_score(board,'black',info)
                        if [x,y]!=[None,None]:
                            board[x][y]=1
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,'black',x,y):
                                board[i][j]=1
                            turn='white'
                            break
                    elif player1==5:
                        x,y=AI.MiniMax.move_minimax(board,3,'black',info,True)
                        if [x,y]!=[None,None]:
                            board[x][y]=1
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,'black',x,y):
                                board[i][j]=1
                            turn='white'
                            break
                    elif player1==6:
                        x,y=AI.Alpha_beta.move_Alpha_beta(board,a_b_depth,turn,info,True)
                        if [x,y]!=[None,None]:
                            board[x][y]=1
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,turn,x,y):
                                board[i][j]=1
                            turn='white'
                            break
                    elif player1==7:
                        x,y=AI.Alpha_beta_Hash.move_Alpha_beta_hash(board,a_b_hash_depth,turn,info,True)
                        if [x,y]!=[None,None]:
                            board[x][y]=1
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,turn,x,y):
                                board[i][j]=1
                            turn='white'
                            break
                    elif player1==8:
                        x,y=AI.MCTS.move_MCTS(board,turn,info,hype_parameter)
                        if [x,y]!=[None,None]:
                            board[x][y]=1
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,turn,x,y):
                                board[i][j]=1
                            turn='white'
                            break

                    elif player2==9:
                        x,y=AI.DQN_run.DQN_move(board,turn,info)
                        if [x,y]!=[None,None]:
                            board[x][y]=1
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,turn,x,y):
                                board[i][j]=1
                            turn='white'
                            break


                #for white
                elif turn == 'white' and\
                        event.type == pygame.MOUSEBUTTONDOWN and\
                        event.button == 1 and\
                        not gameover and\
                        not human:
                    pos=event.pos
                    for [x,y] in info:
                        if pos[0] in range(375+y*80,375+y*80+80) and\
                                pos[1] in range(50+x*80,50+x*80+80):
                            if main.legal_move(board,'white',x,y):
                                board[x][y]=2
                                info.remove([x,y])
                                for i,j in main.flip_pawn(board,'white',x,y):
                                    board[i][j]=2
                                turn='black'
                                break

                elif turn == 'white' and\
                        not gameover and\
                        human:
                    if player2 == 1:
                        x,y = rm.move_random(board,'white',info)
                        if [x,y] != [None,None]:
                            board[x][y] = 2
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,'white',x,y):
                                board[i][j] = 2
                            turn = 'black'
                            break
                    elif player2 == 2:
                        x,y=AI.Evaluate.move_eva(board,'white',info)
                        if [x,y]!=[None,None]:
                            board[x][y]=2
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,'white',x,y):
                                board[i][j]=2
                            turn='black'
                            break
                    elif player2 == 3:
                        x,y=AI.Score_max.move_score(board,'white',info)
                        if [x,y]!=[None,None]:
                            board[x][y]=2
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,'white',x,y):
                                board[i][j]=2
                            turn='black'
                            break
                    elif player2 == 4:
                        x,y=AI.Score_min.move_score(board,'white',info)
                        if [x,y]!=[None,None]:
                            board[x][y]=2
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,'white',x,y):
                                board[i][j]=2
                            turn='black'
                            break
                    elif player2==5:
                        x,y=AI.MiniMax.move_minimax(board,3,'white',info,True)
                        if [x,y]!=[None,None]:
                            board[x][y]=2
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,'white',x,y):
                                board[i][j]=2
                            turn='black'
                            break
                    elif player2==6:
                        x,y=AI.Alpha_beta.move_Alpha_beta(board,a_b_depth,turn,info,True)
                        if [x,y]!=[None,None]:
                            board[x][y]=2
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,turn,x,y):
                                board[i][j]=2
                            turn='black'
                            break
                    elif player2==7:
                        x,y=AI.Alpha_beta_Hash.move_Alpha_beta_hash(board,a_b_hash_depth,turn,info,True)
                        if [x,y]!=[None,None]:
                            board[x][y]=2
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,turn,x,y):
                                board[i][j]=2
                            turn='black'
                            break
                    elif player2==8:
                        x,y=AI.MCTS.move_MCTS(board,turn,info,hype_parameter)
                        if [x,y]!=[None,None]:
                            board[x][y]=2
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,turn,x,y):
                                board[i][j]=2
                            turn='black'
                            break

                    elif player2==9:
                        x,y=AI.DQN_run.DQN_move(board,turn,info)
                        if [x,y]!=[None,None]:
                            board[x][y]=2
                            info.remove([x,y])
                            for i,j in main.flip_pawn(board,turn,x,y):
                                board[i][j]=2
                            turn='black'
                            break


                #check is there any legal move for both player
                if turn == 'black':
                    if not main.check_is_any_legal_move(board,info,'black'):
                        turn = 'white'
                elif turn == 'white':
                    if not main.check_is_any_legal_move(board,info,'white'):
                        turn = 'black'


            else:
                if gameover_show:
                    main.show_score(main.socreboard,board)
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
                    gameover_show=False

        if not gameover:
            # update board
            for x in range(1,9):
                for y in range(1,9):
                    if board[x][y]==1:
                        main.surface.blit(main.gamepawn_black,
                                          (y*main.cell_size[0]+main.space_size[0]+375,
                                           x*main.cell_size[1]+main.space_size[1]+50))
                    elif board[x][y]==2:
                        main.surface.blit(main.gamepawn_white,
                                          (y*main.cell_size[0]+main.space_size[0]+375,
                                           x*main.cell_size[1]+main.space_size[1]+50))

        pygame.display.update()
        main.Runingclock.tick(main.fps)
