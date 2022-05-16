#Liangyz
#2022/5/2  18:41

import pygame
import main
import menu
import time
import menu
import sys
# sys.path.append('/AI/')
import AI.Random
import AI.Evaluate
import AI.Score_max
import AI.Score_min
import AI.MiniMax



def aivsai(player1,player2,number_of_rounds):
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

    #prameter
    turn = 'black'
    NOR = number_of_rounds

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
                return aivsai(player1,player2,NOR)

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
                            return aivsai(player1,player2,NOR)
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
                    x,y = AI.Random.move_random(board,turn,info)
                    if [x,y] != [None,None]:
                        board[x][y] = 1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j] = 1
                        turn = 'white'

                elif player1 == 2:
                    x,y = AI.Evaluate.move_eva(board,turn,info)
                    if [x,y] != [None,None]:
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=1
                        turn='white'

                elif player1 == 3:
                    x,y=AI.Score_max.move_score(board,turn,info)
                    if [x,y]!=[None,None]:
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=1
                        turn='white'

                elif player1 == 4:
                    x,y=AI.Score_min.move_score(board,turn,info)
                    if [x,y]!=[None,None]:
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=1
                        turn='white'

                elif player1 == 5:
                    x,y=AI.MiniMax.move_minimax(board,4,turn,info,True)
                    if [x,y]!=[None,None]:
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=1
                        turn='white'



            #for white
            elif turn == 'white':
                if player2 == 1:
                    x,y = AI.Random.move_random(board,turn,info)
                    if [x,y] != [None,None]:
                        board[x][y] = 2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j] = 2
                        turn = 'black'

                elif player2 == 2:
                    x,y = AI.Evaluate.move_eva(board,turn,info)
                    if [x,y] != [None,None]:
                        board[x][y] = 2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j] = 2
                        turn='black'

                elif player2 == 3:
                    x,y=AI.Score_max.move_score(board,turn,info)
                    if [x,y]!=[None,None]:
                        board[x][y]=2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=2
                        turn='black'

                elif player2 == 4:
                    x,y=AI.Score_min.move_score(board,turn,info)
                    if [x,y]!=[None,None]:
                        board[x][y]=2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=2
                        turn='black'

                elif player2 == 5:
                    x,y=AI.MiniMax.move_minimax(board,4,turn,info,True)
                    if [x,y]!=[None,None]:
                        board[x][y]=2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,turn,x,y):
                            board[i][j]=2
                        turn='black'

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
                    return aivsai(player1,player2,number_of_rounds)



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