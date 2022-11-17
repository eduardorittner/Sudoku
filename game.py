import os
import pygame as pg
import constants as c
import board


if __name__ == "__main__":
        
    pg.init()

    board = board.Board()       # Creates board object
    size = 666
    canvas = pg.display.set_mode((size, size))      
    side = size//9                                  
    pg.display.set_caption("DUDU'S SUDOKU")                # Window name
    font = pg.font.Font(None, 72)                   # Standard pygame font

    selected, wrong = 0, 0      # Runtime flags

    exit = False
    clock = pg.time.Clock()
    while not exit:
        canvas.fill(c.WHITE)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit = True

            if event.type == pg.MOUSEBUTTONDOWN:
                # Indicates that a square was selected and takes the cursor's position
                if not wrong:
                    selected = 1
                    x = event.pos[1]//side
                    y = event.pos[0]//side  

            if event.type == pg.KEYDOWN:
                # Handles the insertion of numbers in the board
                if not board.is_constant(x, y) and 48 < event.key < 58:     # If the square is NULL and an int was typed
                    num = event.key - 48
                    if not board.check_board(x, y, num):
                        wrong = (x, y)
                    else:
                        wrong = 0                    
                    board.add_num(x, y, num)

        board.draw_grid(canvas, c.BLACK, 666)   # Draws the sudoku grid
        board.draw_board(canvas, 666)           # Renders the numbers in the sudoku

        if wrong:
            rect_wrong = pg.Rect(wrong[1]*side, wrong[0]*side, side, side)
            board.highlight_box(canvas, c.T_RED, rect_wrong)  # Highlights the wrong number in red
        else:
            if selected:
                board.highlight_outline(y, x, canvas, 666)  # Highlights the edge of the selected box

            if board.is_over():
                final_text = font.render("VICTORY!", True, c.BLACK)
                final_square = final_text.get_rect(center=(size//2, size//2))
                canvas.blit(final_text, final_square)


        pg.display.update()
        clock.tick(60)

    pg.quit()