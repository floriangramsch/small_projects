class Square:
    def __init__(self, row, column, square) -> None:
        self.row = row
        self.column = column
        self.square = square
        self.figure = ""
        self.placed = False

    def __str__(self) -> str:
        if self.placed:
            return self.figure
        else:
            return self.square

    def set(self, figure):
        self.placed = True
        self.figure = figure

    def remove(self):
        self.placed = False
