from random import randint
from copy import deepcopy


class Board:
    def __init__(self, size):
        self.size = size
        if self.size == 3:
            self.num = 256
        if self.size == 4:
            self.num = 2048
        self.game_matrix = [
            [0 for j in range(self.size)] for i in range(self.size)]
        r = randint(0, self.size - 1)
        s = randint(0, self.size - 1)
        self.game_matrix[r][s] = 2
        self.score = 0
        self.score_undo = [0]
        self.gamematrix_undo = [deepcopy(self.game_matrix)]
        self.gamematrix_temp = deepcopy(self.game_matrix)

    def transpose(self):
        self.game_matrix = [list(tup) for tup in zip(*self.game_matrix)]

    def invert(self):
        self.game_matrix = [row[::-1] for row in self.game_matrix]

    def rotclock90(self):
        self.transpose()
        self.invert()

    def rotantclock90(self):
        self.invert()
        self.transpose()

    def basic_move(self):
        self.score_temp = self.score
        for row in self.game_matrix:
            for i in range(self.size):
                for j in range(self.size - 1 - i):
                    if row[j] == 0:
                        row[j + 1], row[j] = row[j], row[j + 1]

            for i in range(self.size - 1):
                if row[i] == row[i + 1]:
                    row[i] *= 2
                    for j in range(i, self.size - 2):
                        row[j + 1] = row[j + 2]
                    row[-1] = 0
                    self.score += row[i]

    def add_tile(self):
        if self.game_matrix != self.gamematrix_temp:
            s = randint(0, self.size - 1)
            r = randint(0, self.size - 1)
            while self.game_matrix[s][r] != 0:
                s = randint(0, self.size - 1)
                r = randint(0, self.size - 1)
            t = randint(1, 10)
            if t == 10:
                self.game_matrix[s][r] = 4
            else:
                self.game_matrix[s][r] = 2
            self.gamematrix_undo.append(self.gamematrix_temp)
            self.score_undo.append(self.score_temp)

    def moveleft(self):
        self.gamematrix_temp = deepcopy(self.game_matrix)
        self.basic_move()
        self.add_tile()

    def moveright(self):
        self.gamematrix_temp = deepcopy(self.game_matrix)
        self.invert()
        self.basic_move()
        self.invert()
        self.add_tile()

    def moveup(self):
        self.gamematrix_temp = deepcopy(self.game_matrix)
        self.rotantclock90()
        self.basic_move()
        self.rotclock90()
        self.add_tile()

    def movedown(self):
        self.gamematrix_temp = deepcopy(self.game_matrix)
        self.rotclock90()
        self.basic_move()
        self.rotantclock90()
        self.add_tile()

    def game_won(self):
        if any(self.num in row for row in self.game_matrix):
            return True

    def game_over(self):
        if any(0 in row for row in self.game_matrix):
            return False
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.game_matrix[i][j] == self.game_matrix[i][j + 1]:
                    return False
        for j in range(self.size):
            for i in range(self.size - 1):
                if self.game_matrix[i][j] == self.game_matrix[i + 1][j]:
                    return False
        else:
            return True
