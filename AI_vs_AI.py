#Liangyz
#2022/5/2  18:41

import pygame
import main
import time
import menu
import sys
# sys.path.append('/AI/')
import AI.Random
import AI.Evaluate



def aivsai(player1,player2):
    # background
    main.surface.blit(main.gameboard,(375,50))

    #set new board and put pawn on board
    board = main.restnewboard()
    info = []
    for x in range(1,9):
        for y in range(1,9):
            if [x,y] not in [[4,4],[4,5],[5,4],[5,5]]:
                info.append([x,y])

    flag_d = False
    flag_u = False

    gameover = False
    turn = 'player1'

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.exit_game()
            # return to main_menu
            if event.type == pygame.MOUSEMOTION:
                if event.pos[0] in range(1095, 1176) and \
                        event.pos[1] in range(770, 851):
                    flag_d = True
                else:
                    flag_d = False
                # retry
                if event.pos[0] in range(1095, 1172) and \
                        event.pos[1] in range(50, 125):
                    flag_u = True
                else:
                    flag_u = False

            if event.type == pygame.MOUSEBUTTONDOWN and flag_u:
                return aivsai(player1,player2)

            if event.type==pygame.MOUSEBUTTONDOWN and flag_d:
                # menu.main_menu()
                return



        # make move--------------------------------------------------------------------------------
        gameover = main.gameover(board,info)

        if not gameover:
            #show whose turn
            if turn == 'player1':
                main.surface.blit(main.gamepawn_black,(385,60))
            elif turn == 'player2':
                main.surface.blit(main.gamepawn_white,(385,60))

            #for black:
            if turn == 'player1':
                if player1 == 1:
                    x,y = AI.Random.move_random(board,'player1',info)
                    if [x,y] != [None,None]:
                        board[x][y] = 1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,'player1',x,y):
                            board[i][j] = 1
                        turn = 'player2'

                elif player1 == 2:
                    x,y = AI.Evaluate.move_eva(board,'player1',info)
                    if [x,y] != [None,None]:
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,'player1',x,y):
                            board[i][j]=1
                        turn='player2'

                elif player1 == 3:
                    pass


            #for white
            elif turn == 'player2':
                if player2 == 1:
                    x,y = AI.Random.move_random(board,'player2',info)
                    if [x,y] != [None,None]:
                        board[x][y] = 2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,'player2',x,y):
                            board[i][j] = 2
                        turn = 'player1'

                elif player2 == 2:
                    x,y = AI.Evaluate.move_eva(board,'player2',info)
                    if [x,y] != [None,None]:
                        board[x][y] = 2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,'player2',x,y):
                            board[i][j] = 2
                        turn='player1'

                elif player2 == 3:
                    pass

            #check is there any legal move for both player
            if turn == 'player1':
                if not main.check_is_any_legal_move(board,info,'player1'):
                    turn = 'player2'
            elif turn == 'player2':
                if not main.check_is_any_legal_move(board,info,'player2'):
                    turn = 'player1'

        else:
            main.show_score(main.socreboard,board)


        if not gameover:
            # update board
            for x in range(1,9):
                for y in range(1,9):
                    if board[x][y] == 1:
                        main.surface.blit(main.gamepawn_black,
                                          (x*main.cell_size[0]+main.space_size[0]+375,
                                           y*main.cell_size[1]+main.space_size[1]+50))
                    elif board[x][y] == 2:
                        main.surface.blit(main.gamepawn_white,
                                          (x*main.cell_size[0]+main.space_size[0]+375,
                                           y*main.cell_size[1]+main.space_size[1]+50))
            # time.sleep(1.5)

        pygame.display.update()
        main.Runingclock.tick(main.fps)
