#! python3

#from tkinter import *
#from tkinter.ttk import *

import Tkinter
from Tkinter import *

import ttk
from ttk import *

class displayNumbers(object):

    def __init__(self, container, topLimit):

        self.topLimit = topLimit
        self.num = []

        Style().configure("W.TLabel", foreground= "black", background="white", font="Courier 8", anchor="center")
        Style().configure("G.TLabel", foreground= "black", background="green", font="Courier 8", anchor="center")
        
        for i in range(self.topLimit):
            idx = "{0:02}".format(i + 1)
            self.num.append(Label(container, text=idx, style="W.TLabel", width=2))
        
       
    def changeStyle(self, topSelect):

        Style().configure("W.TLabel", foreground= "black", background="white", font="Courier 8", anchor="center")

        for i in range(self.topLimit):
            self.num[i]["style"] = "W.TLabel"

        if len(topSelect) == self.topLimit:
            pass
        else:

            for idx in topSelect:
                self.num[idx - 1]["style"] = "G.TLabel"


    def positionDisplays(self, row, col):

        x_position = 15
        col_ctr = 1
        row_ctr = row

        for i in range(self.topLimit):
            self.num[i].grid(row=row_ctr, column=col, padx=(x_position,10), pady=1, sticky='W')
            col_ctr += 1
            if col_ctr > 13:
                col_ctr = 1
                row_ctr += 1
                x_position = 15
            else:    
                x_position += 35

        row_ctr += 1
        

        

        
