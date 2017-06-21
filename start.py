#!/usr/bin/env python3

# Components available to tkinter:
# Button, Label, Canvas, Menu, Text, Scale,
# OptionMenu, Frame, CheckButton, LabelFrame,
# MenuButton, PanedWindow, Entry, ListBox,
# Message, RadioButton, Scrollbar,
# Bitmap, SpinBox, Image

# Ttk Widget Names:
# Tbutton, TCheckbutton, TCombobox,
# TEntry, TFrame, TLabel, TLabelframe, TMenubutton
# TNotebook, TProgressbar, TRadiobutton, TScale,
# TScrollbar, TSpinbox, Treeview

from tkinter import *
from copy import deepcopy
import math
import numpy
import time


class GameOfLife:

    def __init__(self, root, width, height, s_width, s_height, delay):
        self.stop_id = 0
        self.delay = delay
        self.board = []
        self.initialBoard = deepcopy(self.board)
        self.tmpBoard = deepcopy(self.board)
        self.master = root
        master.title("The Game of Life")
        master.resizable(width=False, height=False)

        self.canvas = Canvas(master,
                             width=width,
                             height=height,
                             borderwidth=0)
        self.canvas.pack()

        menu = Menu(master)
        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="Start", command=self.initialize_animation)
        file_menu.add_command(label="Stop", command=self.stop_animation)
        menu.add_cascade(label="File", menu=file_menu)
        master.config(menu=menu)

        for y in range(0, math.floor(width / s_width)):
            self.board.append([])
            for x in range(0, math.floor(height / s_height)):
                rectangle_id = self.canvas.create_rectangle(x * s_width,
                                                            y * s_height,
                                                            (x + 1) * s_width,
                                                            (y + 1) * s_height,
                                                            fill="white",
                                                            outline="")
                self.board[y].append([rectangle_id, False])
                self.canvas.tag_bind(rectangle_id, '<ButtonPress-1>', self.switch_block)

    def draw_board(self):
        for y in self.board:
            for x in y:
                if x[1]:
                    self.canvas.itemconfig(x[0], fill="black")
                else:
                    self.canvas.itemconfig(x[0], fill="white")

    def outcome(self, x, y, value):
        count = 0
        coordinates_to_check = numpy.squeeze(numpy.asarray(numpy.matrix([[-1, -1],
                                                                         [0, -1],
                                                                         [1, -1],
                                                                         [-1, 0],
                                                                         [1, 0],
                                                                         [-1, 1],
                                                                         [0, 1],
                                                                         [1, 1]]) + numpy.matrix([[x, y]] * 8)))

        for coord in coordinates_to_check:
            try:
                if self.board[coord[1]][coord[0]][1]:
                    count += 1
            except IndexError:
                pass

        if value:
            if count <= 1:
                return False
            elif count <= 3:
                return True
            else:
                return False
        else:
            if count == 3:
                return True
            else:
                return False

    def begin_animation(self):
        for yIdx, y in enumerate(self.board):
            for xIdx, x in enumerate(y):
                self.tmpBoard[yIdx][xIdx][1] = self.outcome(xIdx, yIdx, x[1])
        self.board = deepcopy(self.tmpBoard)
        self.draw_board()
        self.stop_id = self.canvas.after(self.delay, self.begin_animation)

    def initialize_animation(self):
        self.initialBoard = deepcopy(self.board)
        self.tmpBoard = deepcopy(self.board)
        self.begin_animation()

    def stop_animation(self):
        self.board = self.canvas.after_cancel(self.stop_id)
        self.board = deepcopy(self.initialBoard)
        self.draw_board()

    def switch_block(self, event):
        closest_rectangle_id = event.widget.find_closest(event.x, event.y)[0]
        for y in self.board:
            for x in y:
                if x[0] == closest_rectangle_id:
                    x[1] = not x[1]
        self.draw_board()

master = Tk()
game = GameOfLife(master, 600, 600, 10, 10, 400)
master.mainloop()
