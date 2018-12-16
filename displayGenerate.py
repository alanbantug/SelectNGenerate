#! python3

import tkinter
from tkinter import *

from tkinter.ttk import *
import os

class displayNumbers(object):

    def __init__(self, container, ltype, config):

        self.config = config
        self.ltype = ltype

        if self.ltype == 1:
            self.topLimit = 39
            self.extLimit = 0

        elif self.ltype == 2:
            self.topLimit = 47
            self.extLimit = 27

        elif self.ltype == 3:
            self.topLimit = 70
            self.extLimit = 25

        elif self.ltype == 4:
            self.topLimit = 69
            self.extLimit = 26

        self.num = []
        self.ext = []

        Style().configure("W.TLabel", foreground= "black", background="white", font="Courier 8", anchor="center")
        Style().configure("L.TLabel", foreground= "white", background="blue", font="Courier 8", anchor="center")
        Style().configure("Y.TLabel", foreground= "blue", background="yellow", font="Courier 8", anchor="center")
        Style().configure("G.TLabel", foreground= "white", background="green", font="Courier 8", anchor="center")
        Style().configure("R.TLabel", foreground= "white", background="red", font="Courier 8", anchor="center")

        for i in range(self.topLimit):
            idx = "{0:02}".format(i + 1)
            self.num.append(Label(container, text=idx, style="W.TLabel"))

        for i in range(self.extLimit):
            idx = "{0:02}".format(i + 1)
            self.ext.append(Label(container, text=idx, style="W.TLabel"))

        self.h_sep_a = Separator(container, orient=HORIZONTAL)

    def changeTopStyle(self, topSelect):

        Style().configure("W.TLabel", foreground= "black", background="white", font="Courier 8", anchor="center")

        sty = self.checkPattern(topSelect)
        win = self.checkIfWinner(topSelect)
        if win:
            sty = "R.TLabel"

        for i in range(self.topLimit):
            self.num[i]["style"] = "W.TLabel"

        for i in range(self.extLimit):
            self.ext[i]["style"] = "W.TLabel"

        if self.ltype == 1:
            for i in range(len(topSelect)):
                self.num[topSelect[i] - 1]["style"] = sty
        elif self.ltype == 2:
            for i in range(len(topSelect) - 1):
                self.num[topSelect[i] - 1]["style"] = sty
            self.ext[topSelect[5] - 1]["style"] = sty
        elif self.ltype == 3:
            for i in range(len(topSelect) - 1):
                self.num[topSelect[i] - 1]["style"] = sty
            self.ext[topSelect[5] - 1]["style"] = sty
        elif self.ltype == 4:
            for i in range(len(topSelect) - 1):
                self.num[topSelect[i] - 1]["style"] = sty
            self.ext[topSelect[5] - 1]["style"] = sty

    def positionDisplays(self, row, col):

        if self.ltype == 1:
            self.positionFantasy(row, col)
        elif self.ltype == 2:
            self.positionSuper(row, col)
        elif self.ltype == 3:
            self.positionMega(row, col)
        elif self.ltype == 4:
            self.positionPower(row, col)

    def positionFantasy(self, row, col):

        x_position = 9
        col_ctr = 1
        row_ctr = row

        for i in range(self.topLimit):
            self.num[i].grid(row=row_ctr, column=col, padx=(x_position,10), pady=1, sticky='W')
            col_ctr += 1
            if col_ctr > 4:
                col_ctr = 1
                row_ctr += 1
                x_position = 9
            else:
                x_position += 20

        row_ctr += 1

    def positionSuper(self, row, col):

        x_position = 9
        col_ctr = 1
        row_ctr = row

        for i in range(self.topLimit):
            self.num[i].grid(row=row_ctr, column=col, padx=(x_position,10), pady=1, sticky='W')
            col_ctr += 1
            if col_ctr > 6:
                col_ctr = 1
                row_ctr += 1
                x_position = 9
            else:
                x_position += 18

        row_ctr += 1

        self.h_sep_a.grid(row=row_ctr, column=col, padx=5, pady=5, sticky='NSEW')

        x_position = 9
        col_ctr = 1
        row_ctr += 1

        for i in range(self.extLimit):
            self.ext[i].grid(row=row_ctr, column=col, padx=(x_position,10), pady=1, sticky='W')
            col_ctr += 1
            if col_ctr > 5:
                col_ctr = 1
                row_ctr += 1
                x_position = 9
            else:
                x_position += 18

    def positionMega(self, row, col):

        x_position = 9
        col_ctr = 1
        row_ctr = row

        for i in range(self.topLimit):
            self.num[i].grid(row=row_ctr, column=col, padx=(x_position,10), pady=1, sticky='W')
            col_ctr += 1
            if col_ctr > 6:
                col_ctr = 1
                row_ctr += 1
                x_position = 9
            else:
                x_position += 18

        row_ctr += 1

        self.h_sep_a.grid(row=row_ctr, column=col, padx=5, pady=5, sticky='NSEW')

        x_position = 9
        col_ctr = 1
        row_ctr += 1

        for i in range(self.extLimit):
            self.ext[i].grid(row=row_ctr, column=col, padx=(x_position,10), pady=1, sticky='W')
            col_ctr += 1
            if col_ctr > 5:
                col_ctr = 1
                row_ctr += 1
                x_position = 9
            else:
                x_position += 18

    def positionPower(self, row, col):

        x_position = 9
        col_ctr = 1
        row_ctr = row

        for i in range(self.topLimit):
            self.num[i].grid(row=row_ctr, column=col, padx=(x_position,10), pady=1, sticky='W')
            col_ctr += 1
            if col_ctr > 6:
                col_ctr = 1
                row_ctr += 1
                x_position = 9
            else:
                x_position += 18

        row_ctr += 1

        self.h_sep_a.grid(row=row_ctr, column=col, padx=5, pady=5, sticky='NSEW')

        x_position = 9
        col_ctr = 1
        row_ctr += 1

        for i in range(self.extLimit):
            self.ext[i].grid(row=row_ctr, column=col, padx=(x_position,10), pady=1, sticky='W')
            col_ctr += 1
            if col_ctr > 6:
                col_ctr = 1
                row_ctr += 1
                x_position = 9
            else:
                x_position += 18

    def checkPattern(self, num_set):

        odd_ctr = 0

        for num in num_set[:5]:
            if num % 2 != 0:
                odd_ctr += 1

        if odd_ctr == 5 or odd_ctr == 0:
            return "Y.TLabel"
        elif odd_ctr == 4 or odd_ctr == 1:
            return "L.TLabel"
        else:
            return "G.TLabel"


    def checkIfWinner(self, check_set):

        ''' This function will check if the combination is a previous winner
        '''

        filename = self.config.getSource(self.ltype)

        # If data file does not exist, return False
        if os.path.isfile(filename):
            pass
        else:
            return False

        dataFile = open(filename, "r")

        while True:

            d_line = dataFile.readline()

            if d_line == "":
                break

            d_list = d_line.split()

            if len(d_list) > 0:
                if d_list[0].isdigit():

                    winner = []

                    for i in range(5, 10):
                        winner.append(int(d_list[i]))

                    if check_set == winner:
                        return True

        dataFile.close()
        return False
