import os
import pygame as pg
import constants as c
import board


if __name__ == "__main__":

    pg.init()

    board_obj = board.Board()  # Creates board object
    size = 666  # Size must be a multiple of 9
    if size % 9 != 0:
        size = (size // 9) * 9
    canvas = pg.display.set_mode((size, size + size // 9))
    side = size // 9
    pg.display.set_caption("DUDU'S SUDOKU")  # Window name
    font = pg.font.Font(None, side)  # Standard pygame font

    selected, wrong = 0, 0  # Runtime flags

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
                    x = event.pos[1] // side
                    y = event.pos[0] // side

            if event.type == pg.KEYDOWN:
                # Handles the insertion of numbers in the board
                if not board_obj.is_constant(x, y):  # If the square is NULL
                    if 48 < event.key < 58:
                        num = event.key - 48
                        if not board_obj.check_board(x, y, num):
                            wrong = (x, y)
                        else:
                            wrong = 0

                        board_obj.add_num(x, y, num)
                    elif event.key == pg.K_BACKSPACE:
                        board_obj.remove_num(x, y)
                        wrong = 0

        board_obj.draw_grid(canvas, c.BLACK, size)  # Draws the sudoku grid
        board_obj.draw_board(canvas, size)  # Renders the numbers in the sudoku

        if wrong:
            rect_wrong = pg.Rect(wrong[1] * side, wrong[0] * side, side, side)
            board_obj.highlight_box(
                canvas, c.T_RED, rect_wrong
            )  # Highlights the wrong number in red
        else:
            if selected:
                board_obj.highlight_outline(
                    y, x, canvas, size
                )  # Highlights the edge of the selected box

            if board_obj.is_over():
                final_text = font.render("ALL DONE!", True, c.BLACK)
                final_square = final_text.get_rect(center=(size // 2, size // 2))
                pg.draw.rect(
                    canvas, c.GRAY, pg.Rect.inflate(final_square, size // 6, size // 6)
                )
                canvas.blit(final_text, final_square)

        pg.display.update()
        clock.tick(60)

    pg.quit()
