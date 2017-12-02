#! python3

import Tkinter
from Tkinter import *

import ttk
from ttk import *

from tkFileDialog import askdirectory
from tkFileDialog import askopenfilename

import tkMessageBox
# import the dataloader

#import numberSelection as ns
import displaySelect as ds
import os
import pdb
import copy
import random
import shutil
import subprocess as sp
        
class Application(Frame):
    
    def __init__(self, master):
        
        self.master = master
        self.main_container = Frame(self.master)

        # Set images. Note that the line below is needed to change the working directory of the batch file to point to where the script files, including image files are
        # It has to be commented out in the testing library
        
        # os.chdir("c:\\users\\alan\\mypythonscripts\\scripts")

        self.topValue = 0
        self.extValue = 0
        self.workDirectory = os.getcwd()
        
        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))

        # Set Label styles
        Style().configure("FF.TLabel", background="blue", foreground="yellow", font="Courier 20 bold", anchor="center")
        Style().configure("S.TLabel", font="Verdana 8")

        # Set button styles
        Style().configure("B.TButton", font="Verdana 8", relief="raised", width=12)

        # Set scale styles
        Style().configure("S.TScale", orient=HORIZONTAL, width=25)

        # Create widgets
        self.h_sep_a = Separator(self.main_container, orient=HORIZONTAL)
        self.h_sep_b = Separator(self.main_container, orient=HORIZONTAL)
        self.h_sep_c = Separator(self.main_container, orient=HORIZONTAL)
        self.h_sep_d = Separator(self.main_container, orient=HORIZONTAL)
        self.h_sep_e = Separator(self.main_container, orient=HORIZONTAL)
        self.h_sep_f = Separator(self.main_container, orient=HORIZONTAL)
        self.h_sep_g = Separator(self.main_container, orient=HORIZONTAL)

        self.dA = []
        
        self.dA.append(ds.displayNumbers(self.main_container, 75, 30))
            
        self.mainLabel = Label(self.main_container, text="SELECT SCALE", style="FF.TLabel" )
        self.subLabelA = Label(self.main_container, text="Select the numbers to use for generating", style="S.TLabel" )
        self.subLabelB = Label(self.main_container, text="combinations by using the scale selector. ", style="S.TLabel" )
        
        self.topScale = Scale(self.main_container, from_=0, to=75, command=self.showTopValue, orient=HORIZONTAL)
        self.extScale = Scale(self.main_container, from_=0, to=30, command=self.showExtValue, orient=HORIZONTAL)

        self.selectScale = Button(self.main_container, text="SELECT", style="B.TButton", command=self.setScale)
        self.resetScale = Button(self.main_container, text="RESET", style="B.TButton", command=self.resetScale)
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", command=root.destroy)

        # Position widgets        
        self.mainLabel.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')
        self.subLabelA.grid(row=1, column=0, padx=5, pady=0, sticky='NSEW')
        self.subLabelB.grid(row=2, column=0, padx=5, pady=0, sticky='NSEW')
        
        self.h_sep_a.grid(row=3, column=0, padx=5, pady=5, sticky='NSEW')

        self.dA[0].positionTopDisplays(4, 0)
        self.topScale.grid(row=9, column=0, padx=5, pady=5, sticky='NSEW')
        
        self.h_sep_b.grid(row=10, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')        
        
        self.dA[0].positionExtDisplays(11, 0)
        self.extScale.grid(row=13, column=0, padx=5, pady=5, sticky='NSEW')
           
        self.h_sep_c.grid(row=14, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

        self.selectScale.grid(row=15, column=0, padx=5, pady=5, sticky='W')
        self.resetScale.grid(row=15, column=0, padx=(110,5), pady=5, sticky='W')
        self.exit.grid(row=15, column=0, padx=(215,5), pady=5, sticky='W')
        
        self.h_sep_d.grid(row=16, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

    def showTopValue(self, value=None):

        self.topValue = int(self.topScale.get())

        self.dA[0].changeTopStyle(self.topValue + 1)


    def showExtValue(self, value=None):

        self.extValue = int(self.extScale.get())

        self.dA[0].changeExtStyle(self.extValue + 1)


    def resetScale(self):

        response = tkMessageBox.askquestion('Reset Scale', 'Reset the scale to default values. Continue?')

        if response == 'yes':
            self.topScale.set(0)
            self.extScale.set(0)


    def setScale(self):
        
        self.topScale.set(self.topValue)
        self.extScale.set(self.extValue)

        selectionMessage = "You selected {0:02} main numbers".format(self.topValue)

        if self.extValue > 0:
            selectionMessage += " and {0:02} additional numbers".format(self.extValue)

        tkMessageBox.showinfo('Selection Made!', selectionMessage)

        
root = Tk()
root.title("SELECT SCALE")
root.minsize(300, 200)

app = Application(root)

root.mainloop()
