

from curses import KEY_DOWN
import os
import pygame as pg
import constants as c
import requests
import board




if not pg.font:
    print("Warning: fonts disabled")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

board = board.Board()

pg.init()

clock = pg.time.Clock()
canvas = pg.display.set_mode((666, 666))    #initializes the window
side = 666//9
pg.display.set_caption("SUDOKU")            #displays the name of the window
img = pg.image.load("wario.jpg")
exit = False

font = pg.font.Font(None, 72)
text = font.render("BOLA", True, c.BLACK)
text_rect = text.get_rect(center=(666/2, 666/2))
selected = 0
wrong = 0


while not exit:
    canvas.fill(c.WHITE)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit = True
        if event.type == pg.MOUSEBUTTONDOWN:
            selected = 1
            x = event.pos[1]//side
            y = event.pos[0]//side
        if event.type == pg.KEYDOWN:
            if board.is_zero(x, y):
                num = event.key - 48
                if not board.check_board(x, y, num):
                    wrong = (x, y)
                else:
                    wrong = 0                    
                board.add_num(x, y, num)

    board.draw_grid(canvas, c.BLACK, 666)
    board.draw_board(canvas, 666)
    if selected:
        board.highlight_outline(y, x, canvas, 666)
    if wrong:
        rect_wrong = pg.Rect(wrong[1]*side, wrong[0]*side, side, side)
        board.draw_rect_alpha(canvas, c.T_RED, rect_wrong)


    pg.display.update()
    clock.tick(60)

pg.quit()