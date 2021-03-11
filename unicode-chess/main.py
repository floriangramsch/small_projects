from Board import Board

board = Board()
while True:
    board.draw()
    move_from = input("From: ")
    move_to = input ("To: ")
    board.make_move(move_from, move_to)