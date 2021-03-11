import random

class Nim_Variation:
    def __init__(self, n, a, b, cpu_a, cpu_b) -> None:
        self.n = n
        self.a = a
        self.b = b
        self.cpu_a = cpu_a
        self.cpu_b = cpu_b
        self.a_turn = True
        self.b_turn = False

        self.player_turn = self.a

        self.chosen = 1
        self.win = False
        self.player_won = None
        self.counter = 0

    def __str__(self) -> str:
        return f"{self.player_turn} chose {self.chosen}. Now there are {self.n}"

    def is_win(self):
        if self.n == 0:
            self.player_won = self.player_turn
            return True
        else:
            return False

    def turn(self):
        if self.player_turn == self.a:
            self.player_turn = self.b
        else:
            self.player_turn = self.a
        self.a_turn = not self.a_turn
        self.b_turn = not self.b_turn

    def one_or_four(self):
        while True:
            try:
                self.chosen = int(input(f"{self.player_turn}: One or Four? "))
                while self.chosen != 1 and self.chosen != 4 or self.chosen > self.n:
                    print("Not Valid!")
                    self.chosen = int(input(f"{self.player_turn}: One or Four? "))
                break
            except:
                print("Whoops")

    def cpu_one_or_four(self):
        self.chosen = random.choice([1, 4])
        while self.chosen > self.n:
            self.chosen = random.choice([1, 4])

    def update(self):
        self.counter += 1
        self.n -= self.chosen
        # print(self)
        # print()
        if self.is_win():
            # print(f"{self.player_won} won the game after {self.counter} moves!")
            self.win = True
            return (self.player_won, self.counter)
        self.turn()

    def win(self) -> bool:
        return self.win