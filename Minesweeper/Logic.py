from random import randint
import Difficulty_Colours as d


class Structure:
    def __init__(self, diff):
        self.diff = diff
        self.mine_c = d.mine_count[diff]
        self.rnum = d.rc_num[diff]

        self.game_matrix = [
            [0 for i in range(self.rnum + 2)] for j in range(self.rnum + 2)]
        self.values = {}
        self.opened = {}
        self.flags = {}
        self.flag_count = self.mine_c
        self.moves = 0
        self.t = -1
        self.game_over = False

    def place_mine(self, x, y):
        self.mines = []
        for b in range(self.mine_c):
            i = randint(1, self.rnum)
            j = randint(1, self.rnum)
            while (i, j) in self.check or (i, j) in self.mines:
                i = randint(1, self.rnum)
                j = randint(1, self.rnum)
            self.mines.append((i, j))
            self.game_matrix[i][j] = "\U000025CF"
            for r in range(i - 1, i + 2):
                for c in range(j - 1, j + 2):
                    if self.game_matrix[r][c] != "\U000025CF":
                        self.game_matrix[r][c] += 1

    def click_num(self, i, j):
        if self.flags[i, j]:
            self.flags[i, j] = False

        self.moves += 1
        if self.moves == 1:
            self.t = 0
            self.check = []
            for r in range(i - 1, i + 2):
                for c in range(j - 1, j + 2):
                    self.check.append((r, c))
            self.place_mine(i, j)

        cell = self.game_matrix[i][j]
        if cell == "\U000025CF":
            self.game_over = True
            self.opened[i, j] = True
            self.mines.remove((i, j))
            for val in self.mines:
                i, j = val
                if self.flags[i, j] == False:
                    self.opened[i, j] = True

        if cell == 0:
            self.click0(i, j)
        self.opened[i, j] = True

    def click0(self, i, j):
        if 0 < i < (self.rnum + 1) and 0 < j < (self.rnum + \
                    1) and self.opened[i, j] == False:
            cell = self.game_matrix[i][j]
            if cell != "\U000025CF":
                self.opened[i, j] = True
                if cell == 0:
                    for r in range(i - 1, i + 2):
                        for c in range(j - 1, j + 2):
                            self.click0(r, c)

    def auto_click(self, i, j):
        if self.opened[i, j]:
            cell = self.game_matrix[i][j]
            f = 0
            for r in range(max(1, i - 1), min(self.rnum + 1, i + 2)):
                for c in range(max(1, j - 1), min(self.rnum + 1, j + 2)):
                    if self.flags[r, c]:
                        f += 1
            if cell != "\U000025CF" and f == cell:
                for r in range(max(1, i - 1), min(self.rnum + 1, i + 2)):
                    for c in range(max(1, j - 1), min(self.rnum + 1, j + 2)):
                        if self.flags[r, c] == False:
                            if self.game_matrix[r][c] == "\U000025CF":
                                self.click_num(r, c)
                            else:
                                self.click0(r, c)

    def click(self, i, j):
        if self.opened[i, j] == False:
            self.click_num(i, j)
        else:
            self.auto_click(i, j)

    def flag_unflag(self, i, j):
        if self.opened[i, j] == False:
            if self.flags[i, j] == False:
                self.flags[i, j] = True
                self.flag_count -= 1
            else:
                self.flags[i, j] = False
                self.flag_count += 1

    def game_won(self):
        for i in range(1, self.rnum + 1):
            for j in range(1, self.rnum + 1):
                cell = self.game_matrix[i][j]
                if cell != "\U000025CF" and self.opened[i, j] == False:
                    return False
        else:
            return True
