from random import randint
from tkinter import *
from tkinter import ttk
from Logic import *
import Difficulty_Colours as d


class Game:
    def __init__(self, structure):
        root = Tk()
        root.title("Minesweeper")
        root.geometry("430x460")
        root.resizable(False, False)
        self.struct = structure

        self.bg_frame = LabelFrame(root, bd=0)
        self.bg_frame.place(width=430, height=460)

        flag_frame = LabelFrame(self.bg_frame, bd=0, bg=d.board["flg_frm"])
        flag_frame.place(x=0, y=0, width=430, height=30)

        self.difficulty = ["Easy", "Medium", "Hard", "Restart"]

        self.clicked = StringVar()

        menu = ttk.OptionMenu(flag_frame,
                              self.clicked,
                              self.difficulty[self.difficulty.index(self.struct.diff)],
                              *self.difficulty,
                              command=self.level)
        menu.place(x=50, y=4, width=95, height=22)
        menu["menu"].insert_separator(3)

        flag_head1 = Label(
            flag_frame,
            text="\U0001F3F4",
            fg=d.board["flg"],
            bg=d.board["flg_frm"],
            font=(
                "Sans Serif",
                13,
                "bold"))
        flag_head1.place(x=190, y=1)
        self.flag_head2 = Label(
            flag_frame,
            text=self.struct.flag_count,
            fg=d.board["count"],
            bg=d.board["flg_frm"],
            font=(
                "Sans Serif",
                13,
                "bold"))
        self.flag_head2.place(x=215, y=3)

        sw1 = Label(
            flag_frame,
            text="\U000023F1",
            fg=d.board["clock"],
            bg=d.board["flg_frm"],
            font=(
                "Sans Serif",
                14))
        sw1.place(x=290, y=1)
        self.sw2 = Label(
            flag_frame,
            text="0",
            fg=d.board["count"],
            bg=d.board["flg_frm"],
            font=(
                "Sans Serif",
                13,
                "bold"))
        self.sw2.place(x=320, y=3)

        self.set_board()
        root.mainloop()

    def set_board(self):
        self.game_frame = LabelFrame(
            self.bg_frame, bd=0, bg=d.board["gme_frm"])
        self.game_frame.place(x=0, y=30, width=430, height=430)

        self.clicked.set(
            self.difficulty[self.difficulty.index(self.struct.diff)])
        self.sw2["text"] = "0"

        self.tside = d.tile_len[self.struct.diff]
        self.tile_f = d.tile_font[self.struct.diff]
        self.tile_x = d.x_font[self.struct.diff]
        self.tsft = d.tile_sft[self.struct.diff]

        self.tile_bg = {}
        self.button_press = {1: self.struct.click, 3: self.struct.flag_unflag}

        for i in range(1, self.struct.rnum + 1):
            for j in range(1, self.struct.rnum + 1):

                if (i + j) % 2 == 0:
                    self.tile_bg[i, j] = "even"
                else:
                    self.tile_bg[i, j] = "odd"

                ele1 = Label(self.game_frame, font=self.tile_f)
                ele1["bg"] = d.clrcl[self.tile_bg[i, j]]

                self.struct.values[i, j] = ele1
                self.struct.opened[i, j] = False
                self.struct.flags[i, j] = False

                ele1.bind(
                    "<Button>",
                    lambda event,
                    x=i,
                    y=j: self.move(
                        event,
                        x,
                        y),
                    add="+")
                ele1.place(x=self.tsft + (i - 1) * self.tside,
                           y=self.tsft + (j - 1) * self.tside,
                           width=self.tside,
                           height=self.tside)

    def display_board(self):
        self.flag_head2["text"] = self.struct.flag_count
        if self.struct.t == 0:
            self.clock()
        for i in range(1, self.struct.rnum + 1):
            for j in range(1, self.struct.rnum + 1):
                if self.struct.opened[i, j]:
                    cell = self.struct.game_matrix[i][j]
                    if cell == "\U000025CF":
                        n = randint(1, 8)
                        self.struct.values[i,
                                           j]["text"] = self.struct.game_matrix[i][j]
                        self.struct.values[i, j]["fg"] = d.mine_fg[n]
                        self.struct.values[i, j]["bg"] = d.mine_bg[n]
                        self.struct.values[i, j]["font"] = self.tile_x
                    else:
                        self.struct.values[i,
                                           j]["bg"] = d.clrop[self.tile_bg[i, j]]

                        if cell == 0:
                            self.struct.values[i, j]["text"] = ""
                        else:
                            self.struct.values[i,
                                               j]["text"] = self.struct.game_matrix[i][j]
                            self.struct.values[i, j]["fg"] = d.valclr[cell]

                elif self.struct.flags[i, j]:
                    self.struct.values[i, j]["text"] = "\U0001F3F4"
                    self.struct.values[i, j]["fg"] = d.board["flg"]

                elif self.struct.flags[i, j] == False:
                    self.struct.values[i, j]["text"] = ""
        self.unbind_moves()

    def unbind_moves(self):
        if self.struct.game_over or self.struct.game_won():
            for i in range(1, self.struct.rnum + 1):
                for j in range(1, self.struct.rnum + 1):
                    self.struct.values[i, j].unbind("<Button>")
                    if self.struct.game_matrix[i][j] != "\U000025CF" and self.struct.flags[i, j]:
                        self.struct.values[i, j]["text"] = "X"
                        self.struct.values[i, j]["fg"] = d.board["incrt_flg"]
            if self.struct.game_won():
                self.hscore()

    def move(self, event, x, y):
        if event.num in self.button_press:
            self.button_press[event.num](x, y)
        self.display_board()
        self.struct.game_won()

    def clock(self):
        if -1 < self.struct.t < 1000 and not (
                self.struct.game_won()) and self.struct.game_over == False:
            self.sw2["text"] = self.struct.t
            self.sw2.after(1000, self.clock)
            self.struct.t += 1

    def hscore(self):
        f = open("Best Time.txt")
        times = f.read().split()
        if self.struct.t < int(times[self.difficulty.index(self.struct.diff)]):
            times[self.difficulty.index(self.struct.diff)] = str(
                self.struct.t - 1)
            st = "\n".join(times)
            f = open("Best Time.txt", "w")
            f.write(st)
            f.close()

    def level(self, event):
        self.lvl = self.clicked.get()
        if self.struct.diff != self.lvl:
            for level in self.difficulty:
                if self.lvl == level:
                    if self.lvl == "Restart":
                        self.struct.__init__(self.struct.diff)
                    else:
                        self.struct.__init__(self.lvl)
                    self.game_frame.destroy()
                    self.set_board()
                    self.display_board()
                    break


if __name__ == "__main__":
    basic = Structure("Medium")
    game = Game(basic)
