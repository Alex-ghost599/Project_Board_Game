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
import AI.Score_max
import AI.Score_min



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
    turn = 'black'

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
            if turn == 'black':
                main.surface.blit(main.gamepawn_black,(385,60))
            elif turn == 'white':
                main.surface.blit(main.gamepawn_white,(385,60))

            #for black:
            if turn == 'black':
                if player1 == 1:
                    x,y = AI.Random.move_random(board,'black',info)
                    if [x,y] != [None,None]:
                        board[x][y] = 1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,'black',x,y):
                            board[i][j] = 1
                        turn = 'white'

                elif player1 == 2:
                    x,y = AI.Evaluate.move_eva(board,'black',info)
                    if [x,y] != [None,None]:
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,'black',x,y):
                            board[i][j]=1
                        turn='white'

                elif player1 == 3:
                    x,y=AI.Score_max.move_score(board,'black',info)
                    if [x,y]!=[None,None]:
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,'black',x,y):
                            board[i][j]=1
                        turn='white'

                elif player1 == 4:
                    x,y=AI.Score_min.move_score(board,'black',info)
                    if [x,y]!=[None,None]:
                        board[x][y]=1
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,'black',x,y):
                            board[i][j]=1
                        turn='white'



            #for white
            elif turn == 'white':
                if player2 == 1:
                    x,y = AI.Random.move_random(board,'white',info)
                    if [x,y] != [None,None]:
                        board[x][y] = 2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,'white',x,y):
                            board[i][j] = 2
                        turn = 'black'

                elif player2 == 2:
                    x,y = AI.Evaluate.move_eva(board,'white',info)
                    if [x,y] != [None,None]:
                        board[x][y] = 2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,'white',x,y):
                            board[i][j] = 2
                        turn='black'

                elif player2 == 3:
                    x,y=AI.Score_max.move_score(board,'white',info)
                    if [x,y]!=[None,None]:
                        board[x][y]=2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,'white',x,y):
                            board[i][j]=2
                        turn='black'

                elif player2 == 4:
                    x,y=AI.Score_min.move_score(board,'white',info)
                    if [x,y]!=[None,None]:
                        board[x][y]=2
                        info.remove([x,y])
                        for i,j in main.flip_pawn(board,'white',x,y):
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
