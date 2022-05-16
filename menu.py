#Liangyz
#2022/5/2  4:30

import pygame
import time
import pygame_menu
import main
import P_vs_P
import P_vs_AI as pai
import AI_vs_AI as aiai

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

    def onchange_dropselect_player1(*args) -> None:
        b = menu.get_widget('start')
        b.is_selectable = True
        b.set_cursor(pygame_menu.locals.CURSOR_HAND)

    def onchange_dropselect_player2(*args) -> None:
        b = menu.get_widget('start')
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
    ).translate(-412,200)
    menu.add.dropselect(
        title='',
        items=[('Human player',0),
               ('AI(Random)',1),
               ('AI(Evaluate)',2),
               ('AI(Score[max])',3),
               ('AI(Score[min])',4),
               ('AI(MinMax)',5)],
        dropselect_id='Player_1',
        font_size=16,
        onchange=onchange_dropselect_player1,
        padding=0,
        placeholder='Select one',
        placeholder_add_to_selection_box=False,
        selection_box_height=5,
        selection_box_inflate=(0,20),
        selection_box_margin=0,
        selection_box_text_margin=10,
        selection_box_width=200,
        selection_option_font_size=20,
        shadow_width=20,
        float=True,
    ).translate(-412,300)

    menu.add.label(
        'Player 2 (White):',
        font_name=pygame_menu.font.FONT_FIRACODE_BOLD,
        font_size=26,
        margin=(0,5),
        float=True,
    ).translate(-412,400)
    menu.add.dropselect(
        title='',
        items=[('Human player',0),
               ('AI(Random)',1),
               ('AI(Evaluate)',2),
               ('AI(Score[max])',3),
               ('AI(Score[min])',4),
               ('AI(MinMax)',5)],
        dropselect_id='Player_2',
        font_size=16,
        onchange=onchange_dropselect_player2,
        padding=0,
        placeholder='Select one',
        placeholder_add_to_selection_box=False,
        selection_box_height=5,
        selection_box_inflate=(0,20),
        selection_box_margin=0,
        selection_box_text_margin=10,
        selection_box_width=200,
        selection_option_font_size=20,
        shadow_width=20,
        float=True,
    ).translate(-412,500)

    def start_game() -> None:
        player1=menu.get_widget(widget_id='Player_1').get_value()[1]
        player2=menu.get_widget(widget_id='Player_2').get_value()[1]
        if player1 == player2 == 0:
            P_vs_P.pvsp()
        elif player1 == 0 and player2 != 0:
            pai.pvsai(player1,player2)

        elif player1 != 0 and player2 == 0:
            pai.pvsai(player1,player2)

        elif player1 != 0 and player2 != 0:
            aiai.aivsai(player1,player2)



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
                print(event.pos)

        if menu.is_enabled():
            menu.update(pygame.event.get())
            menu.draw(main.surface)

        pygame.display.update()
        main.Runingclock.tick(main.fps)



