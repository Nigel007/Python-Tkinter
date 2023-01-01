from tkinter import *
from Logic import *
import Colours

from random import randint
from copy import deepcopy


class Game:
    def __init__(self, board):
        self.board = board
        self.root = Tk()
        self.root.title("2048")
        self.root.geometry("345x440")
        self.root.resizable(False, False)

        game_name = Label(
            self.root,
            text="2048",
            fg="#776e65",
            font=(
                "Sans Serif",
                55),
            anchor="nw")
        game_name.place(x=17, y=20, width=160, height=100)

        objective1 = Label(
            self.root,
            text="Join the numbers and get to the",
            fg="#776e65",
            font=(
                "Arial",
                7),
            anchor="w")
        objective1.place(x=17, y=85, width=150, height=15)
        self.objective2 = Label(
            self.root, fg="#776e65", font=(
                "Arial", 7, "bold"), anchor="w")
        self.objective2.place(x=153, y=85, width=60, height=15)

        self.game_name_3x3 = Label(
            self.root, fg="#776e65", font=(
                "Sans Serif", 10, "bold"))
        self.game_name_3x3.place(x=130, y=53)

        sc_frame = LabelFrame(self.root, bg=Colours.score_label_bg, bd=0)
        sc_frame.place(x=210, y=40, width=55, height=30)

        sc_head = Label(
            sc_frame,
            text="SCORE",
            font=(
                "Sans Serif",
                7,
                "bold"),
            fg="#eee4da",
            bg=Colours.score_label_bg)
        sc_head.place(x=3, y=16, width=50, height=12)
        self.score_value = Label(sc_frame, text=str(self.board.score), font=(
            "Sans Serif", 10, "bold"), fg="#faf5ef", bg=Colours.score_label_bg)
        self.score_value.place(x=3, y=2, width=50, height=15)

        self.hi_sc()

        hsc_frame = LabelFrame(self.root, bg=Colours.score_label_bg, bd=0)
        hsc_frame.place(x=270, y=40, width=55, height=30)

        hsc_head = Label(
            hsc_frame,
            text="BEST",
            font=(
                "Sans Serif",
                7,
                "bold"),
            fg="#eee4da",
            bg=Colours.score_label_bg)
        hsc_head.place(x=3, y=16, width=50, height=12)
        self.hsc_value = Label(
            hsc_frame,
            text=self.hi_score,
            font=(
                "Sans Serif",
                10,
                "bold"),
            fg="#faf5ef",
            bg=Colours.score_label_bg)
        self.hsc_value.place(x=3, y=2, width=50, height=15)

        und = Button(
            self.root,
            text="Undo",
            width=32,
            height=4,
            font=(
                "Arial",
                8,
                "bold"),
            fg="#faf5ef",
            bg="#776e65",
            command=self.undo,
            relief=FLAT)
        und.place(x=227, y=80, width=33, height=20)
        res = Button(
            self.root,
            text="New",
            width=32,
            height=4,
            font=(
                "Arial",
                8,
                "bold"),
            fg="#faf5ef",
            bg="#776e65",
            command=self.restart,
            relief=FLAT)
        res.place(x=264, y=80, width=30, height=20)
        self.gmde = Button(
            self.root,
            text="3x3",
            width=32,
            height=4,
            font=(
                "Arial",
                8,
                "bold"),
            fg="#faf5ef",
            bg="#776e65",
            command=self.change_mode,
            relief=FLAT)
        self.gmde.place(x=298, y=80, width=27, height=20)

        self.set_board()

        self.root.mainloop()

    def set_board(self):
        self.screen = LabelFrame(self.root, bg=Colours.bord_colour, bd=0)
        self.screen.place(x=20, y=115, width=305, height=305)
        self.objective2["text"] = str(self.board.num) + " tile!"

        if self.board.size == 3:
            self.game_name_3x3["text"] = "3x3"
        else:
            self.game_name_3x3["text"] = ""
        tl = Colours.tile_len[self.board.size]

        self.values = [[0 for i in range(self.board.size)]
                       for j in range(self.board.size)]
        for indrow, row in enumerate(self.board.game_matrix):
            for indcol, col in enumerate(row):
                ele = Label(self.screen)
                self.values[indrow][indcol] = ele
                ele.place(x=5 + indcol * (tl + 5), y=5 +
                          indrow * (tl + 5), width=tl, height=tl)

        self.display_board()

        self.arrow_keys = {
            "Up": self.board.moveup,
            "Down": self.board.movedown,
            "Right": self.board.moveright,
            "Left": self.board.moveleft}
        self.root.bind("<Key>", self.moves)

    def display_board(self):
        self.score_value["text"] = str(self.board.score)
        for indrow, row in enumerate(self.board.game_matrix):
            for indcell, cell in enumerate(row):
                if cell == 0:
                    self.values[indrow][indcell]["text"] = ""
                    self.values[indrow][indcell]["bg"] = Colours.emp_cell_colour
                else:
                    self.values[indrow][indcell]["text"] = cell
                    self.values[indrow][indcell]["fg"] = Colours.num_colour[cell]
                    self.values[indrow][indcell]["bg"] = Colours.cell_colour[cell]
                    self.values[indrow][indcell]["font"] = Colours.num_font[self.board.size][cell]

        self.hi_sc()

    def game_status(self):
        if self.board.game_won() or self.board.game_over():
            self.root.unbind("<Key>")
            if self.board.game_won():
                self.text1 = "You Won!\nDo you want to continue?"
            else:
                self.text1 = "Game Over!\nDo you want to play again?"

            self.game_status_frame = LabelFrame(self.root, bg="#faf5ef", bd=0)
            self.game_status_frame.place(x=50, y=220, width=245, height=95)

            game_status_label = Label(
                self.game_status_frame,
                text=self.text1,
                fg="#776e65",
                bg="#faf5ef",
                font=(
                    "Arial",
                    12,
                    "bold"))
            game_status_label.place(x=12, y=9, width=220, height=40)

            yes_button = Button(
                self.game_status_frame,
                text="Yes",
                fg="#faf5ef",
                bg=Colours.button_colour,
                command=self.yes,
                font=(
                    "Sans Serif",
                    9,
                    "bold"),
                relief=FLAT)
            yes_button.place(x=85, y=55, width=35, height=25)

            no_button = Button(
                self.game_status_frame,
                text="No",
                fg="#faf5ef",
                bg=Colours.button_colour,
                command=self.root.destroy,
                font=(
                    "Sans Serif",
                    9,
                    "bold"),
                relief=FLAT)
            no_button.place(x=125, y=55, width=35, height=25)

    def hi_sc(self):
        with open("High Score.txt") as f:
            high_scores = f.read().split()
            self.hi_score = high_scores[self.board.size - 3]
            with open("High Score.txt", "w") as f:
                if int(self.hi_score) < self.board.score:
                    self.hi_score = str(self.board.score)
                    self.hsc_value["text"] = high_scores[self.board.size -
                                                         3] = self.hi_score
                high_scores = "\n".join(high_scores)
                f.write(high_scores)

    def yes(self):
        self.game_status_frame.destroy()
        if self.board.game_won():
            self.board.num *= 2
            self.root.bind("<Key>", self.moves)
            self.objective2["text"] = str(self.board.num) + " tile!"
        if self.board.game_over():
            self.screen.destroy()
            self.board.__init__(self.board.size)
            self.set_board()

    def restart(self):
        self.screen.destroy()
        self.board.__init__(self.board.size)
        self.set_board()

    def undo(self):
        if self.board.game_over():
            self.game_status_frame.destroy()
            self.root.bind("<Key>", self.moves)
        if len(self.board.gamematrix_undo) >= 1:
            self.board.game_matrix = self.board.gamematrix_undo.pop()
            self.board.score = self.board.score_undo.pop()
        self.display_board()

    def change_mode(self):
        if self.board.size == 4:
            self.board.size = 3
            self.gmde["text"] = "4x4"
        else:
            self.board.size = 4
            self.gmde["text"] = "3x3"
        self.screen.destroy()
        self.board.__init__(self.board.size)
        self.set_board()
        self.hsc_value["text"] = self.hi_score

    def moves(self, event):
        if event.keysym in self.arrow_keys:
            self.arrow_keys[event.keysym]()
        self.display_board()
        self.game_status()


if __name__ == "__main__":
    board = Board(4)
    game = Game(board)
