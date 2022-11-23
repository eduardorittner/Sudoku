from abc import ABC, abstractmethod
from board import Board
from typing import Tuple, Type, List

class Solver(ABC):
	@abstractmethod
	def solve(self) -> List[int]:
		"""Returns the solved board"""

class Backtracking(Solver):

	def __init__(self, board_obj: Type[Board]) -> None:
		"""
		Copies the board to the solver object
		"""

		self.board = board_obj.board

	def check_board(self, x: int, y: int, num: int) -> bool:
		"""
		Checks if the new board is valid, where num is the number to be added
		and x, y are the coordinates in the board

		Returns True if the new board is valid
		Returns False if the new board is not valid

		Note: must be called before the number is added to the board
		"""

		for i in range(9):
			if self.board[y][i] == num:  # Checks the column
				return False

			if self.board[i][x] == num:  # Checks the line
				return False

		x_sqr = x // 3
		y_sqr = y // 3
		for i in range(3):
			for j in range(3):
				if (
					self.board[i + y_sqr * 3][j + x_sqr * 3] == num
				):  # Checks the 3x3 square
					return False

		return True

	def find_zero(self) -> Tuple[int, int]:
		"""
		Finds the next emtpy square in the board and returns its position as a tuple
		"""

		for i in range(9):
			for j in range(9):
				if self.board[i][j] == 0:
					return (i, j)


	def solve_aux(self) -> bool:
		"""
		Solves the sudoku board recursively
		"""

		zero = self.find_zero()

		if not zero:  # If there are no empty squares, the sudoku is solved
			return True

		for i in range(1, 10):
			if self.check_board(zero[1], zero[0], i):
				self.board[zero[0]][zero[1]] = i
				if self.solve_aux():
					return True
				self.board[zero[0]][zero[1]] = 0

		return False

	def solve(self) -> List[int]:
		"""
		Returns the solved board if it is valid

		Will return nothing in case it's not solvable for now
		"""

		if self.solve():
			return self.board