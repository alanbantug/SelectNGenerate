#! python3

import tkinter
from tkinter import *

from tkinter.ttk import *
import os

class displayNumbers(object):

    def __init__(self, container, topLimit):

        self.topLimit = topLimit

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
        
       
    def changeTopStyle(self, topSelect):

        Style().configure("W.TLabel", foreground= "black", background="white", font="Courier 8", anchor="center")

        sty = self.checkPattern(topSelect)
        win = self.checkIfWinner(topSelect)

        for i in range(self.topLimit):
            self.num[i]["style"] = "W.TLabel"

        for i in range(self.topLimit):
            if i + 1 in topSelect:
                if win:
                    self.num[i]["style"] = "R.TLabel"
                else:
                    self.num[i]["style"] = sty


    def positionTopsDisplays(self, row, col):

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
        
    def checkPattern(self, num_set):

        odd_ctr = 0

        for num in num_set:
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

        if os.path.isfile("config.txt"):
            pass
        else:
            return False
        
        configFile = open("config.txt", "r")
        filename = configFile.readline()
        configFile.close()

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



        
