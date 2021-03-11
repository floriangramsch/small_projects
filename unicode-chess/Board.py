from globals import *
from Square import Square
import os

class Board:
    def __init__(self) -> None:
        self.board = [[0 for j in range(8)] for i in range(8)]
        for row in range(8):
            for column in range(8):
                if (row % 2 == 0 and column % 2 == 0) or (row % 2 == 1 and column % 2 == 1):
                    self.board[row][column] = Square(row, column, u"\u25A0")
                else:
                    self.board[row][column] = Square(row, column, u"\u25A1")
        self.start_up()

    def draw(self):
        os.system("clear")
        for i in self.board:
            for j in i:
                print(j, end=" ")
            print((7-i[0].row)+1)
        for i in range(8):
            print(letters[i], end=" ")
        print()

    def start_up(self):
        for i in range(8):
            self.board[1][i].set(figures_black["pawn"])
            self.board[6][i].set(figures_white["pawn"])
        self.board[0][0].set(figures_black["rook"])
        self.board[0][7].set(figures_black["rook"])
        self.board[7][0].set(figures_white["rook"])
        self.board[7][7].set(figures_white["rook"])

        self.board[0][1].set(figures_black["knight"])
        self.board[0][6].set(figures_black["knight"])
        self.board[7][1].set(figures_white["knight"])
        self.board[7][6].set(figures_white["knight"])

        self.board[0][2].set(figures_black["bishop"])
        self.board[0][5].set(figures_black["bishop"])
        self.board[7][2].set(figures_white["bishop"])
        self.board[7][5].set(figures_white["bishop"])

        self.board[0][3].set(figures_black["queen"])
        self.board[0][4].set(figures_black["king"])
        self.board[7][3].set(figures_white["queen"])
        self.board[7][4].set(figures_white["king"])

    def convert(self, letter):
        # letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        return str(letters.index(letter))

    def make_move(self, move_from, move_to):
        move_from = str(7-(int(move_from[1]) - 1)) + self.convert(move_from[0])
        move_to = str(7-(int(move_to[1]) - 1)) + self.convert(move_to[0])

        self.board[int(move_to[0])][int(move_to[1])].set(self.board[int(move_from[0])][int(move_from[1])].figure)
        self.board[int(move_from[0])][int(move_from[1])].remove()
