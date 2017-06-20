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
import math

def begin_animation():
    canvas['state'] = 'disabled'

def stop_animation():
    canvas['state'] = 'normal'

def switch_block(event):
    closestRectangleId = event.widget.find_closest(event.x, event.y)[0]
    for y in board:
        for x in y:
            if x[0] == closestRectangleId:
                if x[1] == 0:
                    x[1] = 1
                    event.widget.itemconfig(closestRectangleId,
                                            fill="black")
                else:
                    x[1] = 0
                    event.widget.itemconfig(closestRectangleId,
                                            fill="white")


CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600

SQUARE_WIDTH = 10
SQUARE_HEIGHT = 10

board = []

master = Tk()
master.wm_title("The Game of Life")
master.resizable(width=False, height=False)

menu = Menu(master)
file_menu = Menu(menu, tearoff=0)
file_menu.add_command(label="Start", command=begin_animation)
file_menu.add_command(label="Stop", command=stop_animation)
menu.add_cascade(label="File", menu=file_menu)
master.config(menu=menu)


canvas = Canvas(master,
                width=CANVAS_WIDTH,
                height=CANVAS_HEIGHT,
                borderwidth=0)
canvas.pack()

for y in range(0, math.floor(CANVAS_WIDTH / SQUARE_WIDTH)):
    board.append([])
    for x in range(0, math.floor(CANVAS_HEIGHT / SQUARE_HEIGHT)):
        rectangle_id = canvas.create_rectangle(x * SQUARE_WIDTH,
                                               y * SQUARE_HEIGHT,
                                               (x + 1) * SQUARE_WIDTH,
                                               (y + 1) * SQUARE_HEIGHT,
                                               fill="white",
                                               outline="")
        board[y].append([rectangle_id, 0])
        canvas.tag_bind(rectangle_id, '<ButtonPress-1>', switch_block)


master.mainloop()

