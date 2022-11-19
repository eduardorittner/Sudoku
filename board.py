import pygame as pg
import constants as c
from random import randint
import zipfile as zp

class Board():

    def __init__(self):
        """
        Initializes the board

        Fetches a random configuration from the file "puzzles0_kaggle" from data.zip
        Currently only one difficulty
        """
        self.board = [[0 for i in range(9)] for j in range(9)]  # Matrix that stores the numbers of the sudoku grid
        self.flag = [[0 for i in range(9)] for j in range(9)]   # Matrix that stores the flag that indicates whether a number is constant (1) or mutable (0)

        with zp.ZipFile("data.zip") as z:
            with z.open("data/puzzles0_kaggle") as f:
                num = randint(0, 100002)        # Chooses a specific line to read from
                for i, line in enumerate(f):
                    if i == num:
                        puzzle = line       

        puzzle = puzzle[0:-1]
        
        for i in range(9):
            for j in range(9):
                if puzzle[i*9 + j] != 46:       # The file is in ASCII format, so 46 is a "." and represents an empty square
                    self.board[i][j] = puzzle[i*9 + j] - 48    # Retrieves the number from its ASCII 
                    self.flag[i][j] = 1 


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

    def remove_num(self, x: int, y: int) -> None:
        """
        Erases the given square
        """

        self.board[y][x] = 0

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

    def generate_sudoku(self):
        set_nums = set(i for i in range(1, 10))
        lines, columns, squares = [], [], []
        for i in range(9):
            lines.append(list(set_nums))
            columns.append(list(set_nums))
            squares.append(list(set_nums))
        
        sudoku = [[0 for i in range(9)] for j in range(9)] # Matrix of the sudoku board

        for i in range(9):
            for j in range(9):
                temp = 2*(i // 3) + j // 3
                possible = [i for i in lines[i] and columns[j] and squares[temp]]
                sudoku[i][j] = possible[randint(0, len(possible))]

        print(sudoku)

