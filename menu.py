#Liangyz
#2022/5/2  4:30
import datetime
import os
import pandas as pd
import numpy as np
import pygame
import time
import pygame_menu
import main
import P_vs_P
import P_vs_AI as pai
import AI_vs_AI as aiai


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  #check if there is a folder
        os.makedirs(path)  #makedirs folder if there is no folder

    else:
        pass


def mkcsv(path,data):
    file = os.path.exists(path)
    columns=['Board','Game Time','Move Time','Action List','Action List Count','Score','Winner']
    if not file:
        df = pd.DataFrame(data=[data],columns=columns)
        df.to_csv(path,index=False)
    else:
        df = pd.DataFrame(data=[data],columns=columns)
        df.to_csv(path,index=False,mode='a',header=False)


def button_onmouseover(w: 'pygame_menu.widgets.Widget',_) -> None:
    if w.readonly:
        return
    w.set_background_color((6,255,0))


def button_onmouseover_quit(w: 'pygame_menu.widgets.Widget',_) -> None:
    if w.readonly:
        return
    w.set_background_color((255,0,0))


def button_onmouseleave(w: 'pygame_menu.widgets.Widget',_) -> None:
    w.set_background_color((58,152,255))


def main_menu():
    theme = pygame_menu.Theme(
        background_color=main.background_color,
        title=False,
        widget_font=pygame_menu.font.FONT_FIRACODE,
        widget_font_color=(255,255,255),
        widget_margin=(0,15),
        widget_selection_effect=pygame_menu.widgets.NoneSelection()
    )

    menu = pygame_menu.Menu(
        height=900,
        mouse_motion_selection=True,
        position=(0,0,False),
        center_content=False,
        theme=theme,
        title='',
        width=1200
    )

    def onchange_dropselect(*args) -> None:
        ooo=menu.get_widget(widget_id='Player_1')
        oooo=menu.get_widget(widget_id='Player_2')
        a = ooo.get_index()
        aa = oooo.get_index()
        if a != -1 and aa != -1:
            b = menu.get_widget('start')
            b.is_selectable = True
            b.readonly=False
            b.set_cursor(pygame_menu.locals.CURSOR_HAND)

    # def onchange_dropselect_player2(*args) -> None:
    #     b = menu.get_widget('start')
    #     b.readonly = False
    #     b.set_cursor(pygame_menu.locals.CURSOR_HAND)

    def onchange_toggle_switch(state_value, *args) -> None:
        if state_value:
            b = menu.get_widget('range_slider')
            b.is_selectable = False
            b.readonly = True
            b.set_value(0)
            b.set_cursor(pygame_menu.locals.CURSOR_HAND)
        else:
            b = menu.get_widget('range_slider')
            b.is_selectable = True
            b.readonly = False
            b.set_cursor(pygame_menu.locals.CURSOR_HAND)

    menu.add.label(
        '',
        background_color='#FFFFFF',
        background_inflate=(775,750),
        float=True
    ).translate(175,425)

    menu.add.label(
        'Player 1 (Black):',
        font_name=pygame_menu.font.FONT_FIRACODE_BOLD,
        font_size=26,
        margin=(0,5),
        float=True,
    ).translate(-412,50)
    menu.add.dropselect(
        title='',
        items=[('Human player',0),
               ('AI(Random)',1),
               ('AI(Evaluate)',2),
               ('AI(Score[max])',3),
               ('AI(Score[min])',4),
               ('AI(MinMax)',5),
               ('AI(Alpha_Beta)',6),
               ('AI(Alpha_Beta_hash)',7),
               ('AI(MCTS)',8),
               ('AI(DQN)',9)],
        dropselect_id='Player_1',
        font_size=16,
        onchange=onchange_dropselect,
        padding=0,
        placeholder='Select one',
        placeholder_add_to_selection_box=False,
        selection_box_height=5,
        selection_box_inflate=(0,20),
        selection_box_margin=0,
        selection_box_text_margin=10,
        selection_box_width=260,
        selection_option_font_size=20,
        shadow_width=20,
        float=True,
    ).translate(-412,100)

    menu.add.label(
        'Player 2 (White):',
        font_name=pygame_menu.font.FONT_FIRACODE_BOLD,
        font_size=26,
        margin=(0,5),
        float=True,
    ).translate(-412,150)
    menu.add.dropselect(
        title='',
        items=[('Human player',0),
               ('AI(Random)',1),
               ('AI(Evaluate)',2),
               ('AI(Score[max])',3),
               ('AI(Score[min])',4),
               ('AI(MinMax)',5),
               ('AI(Alpha_Beta)',6),
               ('AI(Alpha_Beta_hash)',7),
               ('AI(MCTS)',8),
               ('AI(DQN)',9)],
        dropselect_id='Player_2',
        font_size=16,
        onchange=onchange_dropselect,
        padding=0,
        placeholder='Select one',
        placeholder_add_to_selection_box=False,
        selection_box_height=5,
        selection_box_inflate=(0,20),
        selection_box_margin=0,
        selection_box_text_margin=10,
        selection_box_width=260,
        selection_option_font_size=20,
        shadow_width=20,
        float=True,
    ).translate(-412,200)


    menu.add.toggle_switch(
        title='Data Collection',
        default=False,
        toggleswitch_id='Data_Collection',
        font_size=20,
        margin=(0,5),
        state_values=(0,1),
        onchange=onchange_toggle_switch,
        state_text_font_color=((0,0,0),(0,0,0)),
        state_text_font_size=15,
        switch_margin=(15,0),
        width=70
    ).translate(-412,265)

    menu.add.label(
        'Number of Rounds',
        font_name=pygame_menu.font.FONT_FIRACODE_BOLD,
        font_size=24,
        margin=(0,5),
        float=True,
    ).translate(-412,310)

    menu.add.label(
        '(0 for Manually):',
        font_name=pygame_menu.font.FONT_FIRACODE_BOLD,
        font_size=24,
        margin=(0,5),
        float=True,
    ).translate(-412,340)

    menu.add.range_slider('',0,(0,100),1,
                          rangeslider_id='range_slider',
                          float=True,
                          height=20,
                          width=300,
                          font_size=36,
                          padding=0,
                          value_format=lambda x: str(int(x))).translate(-412,400)

    menu.add.label(
        'Scoreboard',
        font_name=pygame_menu.font.FONT_FIRACODE_BOLD,
        font_size=24,
        margin=(0,5),
        float=True,
    ).translate(-412,500)

    menu.add.label(
        'Black',
        font_name=pygame_menu.font.FONT_FIRACODE_BOLD,
        font_size=22,
        margin=(0,5),
        float=True,
    ).translate(-525,550)

    menu.add.label(
        'Draw',
        font_name=pygame_menu.font.FONT_FIRACODE_BOLD,
        font_size=22,
        margin=(0,5),
        float=True,
    ).translate(-405,550)

    menu.add.label(
        'White',
        font_name=pygame_menu.font.FONT_FIRACODE_BOLD,
        font_size=22,
        margin=(0,5),
        float=True,
    ).translate(-285,550)

    menu.add.label(
        '',
        background_color='#FFFFFF',
        background_inflate=(40,10),
        float=True
    ).translate(-525,600)

    menu.add.label(
        '',
        background_color='#FFFFFF',
        background_inflate=(40,10),
        float=True
    ).translate(-405,600)

    menu.add.label(
        '',
        background_color='#FFFFFF',
        background_inflate=(40,10),
        float=True
    ).translate(-285,600)


    def start_game() -> None:
        """Start game."""
        player1=menu.get_widget(widget_id='Player_1').get_value()[1]
        player2=menu.get_widget(widget_id='Player_2').get_value()[1]
        number_of_rounds=round(menu.get_widget(widget_id='range_slider').get_value())

        data_collection=menu.get_widget(widget_id='Data_Collection').get_value()
        if data_collection == 1:
            #making dir for data collection
            path_dir='D:\\Durham\\Project\\code\\Data_collection'
            player1_name=menu.get_widget(widget_id='Player_1').get_value()[0][0]
            player2_name=menu.get_widget(widget_id='Player_2').get_value()[0][0]
            data_path=path_dir+'\\'+\
                      player1_name+'\\'+\
                      player2_name+'\\'+\
                      player1_name+'_VS_'+player2_name
            # print(data_path)
            mkdir(data_path)
        else:
            pass
        # print(player1,player2,number_of_rounds,data_collection)
        # print(player1_name[0] + player2_name[0])

        if player1 == player2 == 0:
            P_vs_P.pvsp()
        elif player1 == 0 and player2 != 0:
            pai.pvsai(player1,player2)

        elif player1 != 0 and player2 == 0:
            pai.pvsai(player1,player2)

        elif player1 != 0 and player2 != 0:
            if data_collection == 0:
                aiai.aivsai(player1,player2,number_of_rounds,data_collection)
            else:
                times = 1000
                # game_data = []
                game_csv_path = data_path + '\\' +\
                      player1_name + '_VS_' + player2_name + '_' +\
                      str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.csv'

                if number_of_rounds == 0:
                    for i in range(times):
                        game_data = aiai.aivsai(player1,player2,number_of_rounds,data_collection,times=i)
                        player1,player2 = player2,player1
                        # print(game_data)
                        mkcsv(game_csv_path,game_data)
                        # print(game_csv_path)

    start = menu.add.button(
        'Start',
        start_game,
        button_id='start',
        shadow_width=10,
        float=True
    )
    start.translate(-412,700)
    start.set_onmouseover(button_onmouseover)
    start.set_onmouseleave(button_onmouseleave)
    start.set_background_color((58,152,255))
    start.readonly = True
    start.is_selectable = False

    quit_game = menu.add.button(
        'Exit',
        main.exit_game,
        shadow_width=10,
        float=True
    )
    quit_game.translate(-412,800)
    quit_game.set_onmouseover(button_onmouseover_quit)
    quit_game.set_onmouseleave(button_onmouseleave)
    quit_game.set_background_color((58,152,255))

    menu.mainloop(main.surface)

    running = True
    while running:
        # close window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.exit_game()
            elif event.type == pygame.MOUSEMOTION:
                pass
                # print(event.pos)

        if menu.is_enabled():
            menu.update(pygame.event.get())
            menu.draw(main.surface)

        pygame.display.update()
        main.Runingclock.tick(main.fps)



