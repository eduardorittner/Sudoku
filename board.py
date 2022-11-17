import pygame as pg
import constants as c

class Board():

    def __init__(self):
        self.board = [[0 for i in range(9)] for j in range(9)]

    def check_board(self, x: int, y: int, num: int) -> bool:
        """
        Checks if the new board is valid, where num is the number to be added
        and x, y are the coordinates in the board

        Returns True if the new board is valid
        Returns False if the new board is not valid
        """

        for i in range(9):
            if self.board[y][i] == num:
                return False
            if self.board[i][x] == num:
                return False
            
        x_sqr = x//3
        y_sqr = y//3
        for i in range(3):
            for j in range(3):
                if self.board[i + y_sqr*3][j + x_sqr*3] == num:
                    return False
        return True

    def add_num(self, x: int, y: int, num: int) -> None:
        self.board[y][x] = num

    def is_over(self) -> bool:
        """
        Checks it the board is complete

        Returns True if the board is complete
        Returns False if the board is not complete
        """

        for i in self.board:
            for j in i:
                if j == 0:
                    return False
        return True

    def draw_board(self, canvas, size: int) -> None:
        font = pg.font.Font(None, 56)
        side = size // 9
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    text = font.render(str(self.board[i][j]), True, c.BLACK)
                    text_square = text.get_rect(center=(i*side + side//2, j*side + side//2))
                    canvas.blit(text, text_square)

    
    def is_zero(self, x: int, y: int):
        if self.board[y][x] == 0:
            return True
        return False


    def draw_grid(self, canvas, color, size) -> None:
        sub = size // 9
        for i in range(1, 9):
            width = 1
            if i % 3 == 0:
                width = 3
            pg.draw.line(canvas, color, [0, sub*i], [size, sub*i], width)
            pg.draw.line(canvas, color, [sub*i, 0], [sub*i, size], width)

    def highlight_outline(self, x: int, y: int, canvas, size: int) -> None:
        #self.draw_grid(canvas, [0, 0, 0], size)
        side = size // 9
        x *= side
        y *= side
        pg.draw.line(canvas, c.RED, [x, y], [x, y + side], 3)
        pg.draw.line(canvas, c.RED, [x, y], [x + side, y], 3)
        pg.draw.line(canvas, c.RED, [x + side, y], [x + side, y + side], 3)
        pg.draw.line(canvas, c.RED, [x, y + side], [x + side, y + side], 3)

    def highlight_box(self, x:int, y: int, canvas, size: int) -> None:
        pass

    def highlight(self, x: int, y: int, canvas, clock):
        """

        """
        #self.add_num(x, y)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN:
                    if self.is_zero(x, y):
                        self.board[y][x] = event.key - 48
                        return
                    return
            self.highlight_box(y, x, canvas, 666)
            clock.tick(60)
    

    def draw_rect_alpha(self, surface, color, rect):
        shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
        pg.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)

