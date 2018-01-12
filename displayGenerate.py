#! python3

#from tkinter import *
#from tkinter.ttk import *

import tkinter
from tkinter import *

from tkinter.ttk import *

class displayNumbers(object):

    def __init__(self, container, topLimit):

        self.topLimit = topLimit

        self.num = []
        self.ext = []

        Style().configure("W.TLabel", foreground= "black", background="white", font="Courier 8", anchor="center")
        Style().configure("G.TLabel", foreground= "white", background="green", font="Courier 8", anchor="center")
        
        for i in range(self.topLimit):
            idx = "{0:02}".format(i + 1)
            self.num.append(Label(container, text=idx, style="W.TLabel"))
        
       
    def changeTopStyle(self, topSelect):

        Style().configure("W.TLabel", foreground= "black", background="white", font="Courier 8", anchor="center")

        for i in range(self.topLimit):
            self.num[i]["style"] = "W.TLabel"

        for i in range(self.topLimit):
            if i + 1 in topSelect:
                self.num[i]["style"] = "G.TLabel"


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
        
        

        

        
