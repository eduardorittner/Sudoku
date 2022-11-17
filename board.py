import pygame as pg
import constants as c

class Board():

    def __init__(self):
        """
        Initializes the board as a 9x9 matrix of zeros
        """
        self.board = [[0 for i in range(9)] for j in range(9)]  # Matrix that stores the numbers of the sudoku grid
        self.flag = [[0 for i in range(9)] for j in range(9)]   # Matrix that stores the flag that indicates whether a number
                                                                # is constant (1) or mutable (0)

    def check_board(self, x: int, y: int, num: int) -> bool:
        """
        Checks if the new board is valid, where num is the number to be added
        and x, y are the coordinates in the board

        Returns True if the new board is valid
        Returns False if the new board is not valid

        Note: must be called before the number is added to the board
        """

        for i in range(9):
            if self.board[y][i] == num: # Checks the column
                return False    
            if self.board[i][x] == num: # Checks the line
                return False
            
        x_sqr = x // 3
        y_sqr = y // 3
        for i in range(3):
            for j in range(3):
                if self.board[i + y_sqr*3][j + x_sqr*3] == num: # Checks the 3x3 square
                    return False

        return True

    def add_num(self, x: int, y: int, num: int) -> None:
        """
        Adds the number (num) to the given position in the board
        """

        self.board[y][x] = num

    def is_over(self) -> bool:
        """
        Checks it the board is complete

        Returns True if it is complete
        Returns False if it is not complete
        """

        for i in self.board:
            for j in i:
                if j == 0:
                    return False

        return True

    def draw_board(self, canvas: pg.Surface, size: int) -> None:
        """
        Renders the numbers in the board
        """
        
        font = pg.font.Font(None, 56)
        side = size // 9
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    if self.flag[i][j]:
                        text = font.render(str(self.board[i][j]), True, c.BLACK)
                    else:
                        text = font.render(str(self.board[i][j]), True, c.BLUE)          

                    text_square = text.get_rect(center=(i*side + side//2, j*side + side//2))
                    canvas.blit(text, text_square)

    
    def is_zero(self, x: int, y: int) -> bool:
        """
        Checks if a given square is empty
        """

        if self.board[y][x] == 0:
            return True

        return False

    def is_constant(self, x: int, y: int) -> bool:
        """
        Checks if a given number is constant or not
        """

        return bool(self.flag[y][x])

    def draw_grid(self, canvas: pg.Surface, color: list, size: int) -> None:
        """
        Draws the sudoku grid
        """

        side = size // 9
        for i in range(1, 9):
            width = 1
            if i % 3 == 0:
                width = 3
            pg.draw.line(canvas, color, [0, side*i], [size, side*i], width)
            pg.draw.line(canvas, color, [side*i, 0], [side*i, size], width)

    def highlight_outline(self, x: int, y: int, canvas, size: int) -> None:
        """
        Highlights the given square's outline in red

        Must be called after the sudoku grid has been rendered
        """

        side = size // 9
        x *= side
        y *= side
        pg.draw.line(canvas, c.RED, [x, y], [x, y + side], 3)
        pg.draw.line(canvas, c.RED, [x, y], [x + side, y], 3)
        pg.draw.line(canvas, c.RED, [x + side, y], [x + side, y + side], 3)
        pg.draw.line(canvas, c.RED, [x, y + side], [x + side, y + side], 3)
    

    def highlight_box(self, surface: pg.Surface, color: list, rect: pg.Rect) -> None:
        """
        Highlights the given box in transparent red
        """

        shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
        pg.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)

