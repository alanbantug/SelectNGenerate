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
        Style().configure("FF.TLabel", font="Courier 20 bold", anchor="center")
        Style().configure("S.TLabel", font="Verdana 8")

        # Set button styles
        Style().configure("B.TButton", font="Verdana 8", relief="raised", width=12)

        # Set scale styles
        Style().configure("S.TScale", orient=HORIZONTAL, width=25)

        self.parentTab = ttk.Notebook(self.main_container)
        self.selTab = ttk.Frame(self.parentTab)   # first page, which would get widgets gridded into it
        self.genTab = ttk.Frame(self.parentTab)   # second page
        self.parentTab.add(self.selTab, text='   Select Numbers    ')
        self.parentTab.add(self.genTab, text='Generate Combinations')
        
        # Create widgets
        self.h_sep_a = Separator(self.selTab, orient=HORIZONTAL)
        self.h_sep_b = Separator(self.selTab, orient=HORIZONTAL)
        self.h_sep_c = Separator(self.selTab, orient=HORIZONTAL)
        self.h_sep_d = Separator(self.selTab, orient=HORIZONTAL)
        self.h_sep_e = Separator(self.selTab, orient=HORIZONTAL)
        self.h_sep_f = Separator(self.selTab, orient=HORIZONTAL)
        self.h_sep_g = Separator(self.selTab, orient=HORIZONTAL)

        self.dA = []
        
        for i in range(5):
            self.dA.append(ds.displayNumbers(self.selTab, 39))

        self.mainLabel = Label(self.main_container, text="SELECT AND GENERATE", style="FF.TLabel" )
            
        self.selLabel = Label(self.selTab, text="SELECT SCALE", style="FF.TLabel" )
        self.subLabelA = Label(self.selTab, text="Select the numbers to use for generating", style="S.TLabel" )
        self.subLabelB = Label(self.selTab, text="combinations by using the scale selector. ", style="S.TLabel" )
        
        self.topScale = Scale(self.selTab, from_=0, to=75, command=self.showTopValue, orient=HORIZONTAL)
        self.extScale = Scale(self.selTab, from_=0, to=30, command=self.showExtValue, orient=HORIZONTAL)

        self.selectScale = Button(self.selTab, text="SELECT", style="B.TButton", command=self.setScale)
        self.resetScale = Button(self.selTab, text="RESET", style="B.TButton", command=self.resetScale)
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", command=root.destroy)

        # Position widgets        
        self.selLabel.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')
        self.subLabelA.grid(row=1, column=0, columnspan=5, padx=5, pady=0, sticky='NSEW')
        self.subLabelB.grid(row=2, column=0, columnspan=5, padx=5, pady=0, sticky='NSEW')
        
        self.h_sep_a.grid(row=3, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        for i in range(5):
            self.dA[i].positionTopDisplays(4, i)
        #self.topScale.grid(row=9, column=0, padx=5, pady=5, sticky='NSEW')
        
        self.h_sep_b.grid(row=14, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')        
        
        #self.dA[0].positionExtDisplays(11, 0)
        #self.extScale.grid(row=13, column=0, padx=5, pady=5, sticky='NSEW')
           
        #self.h_sep_c.grid(row=14, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

        self.selectScale.grid(row=15, column=0, columnspan=3, padx=5, pady=5, sticky='W')
        self.resetScale.grid(row=15, column=4, columnspan=2, padx=(110,5), pady=5, sticky='W')
                
        self.mainLabel.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')
        self.parentTab.grid(row=1, column=0, padx=5, pady=5, sticky='NSEW')
        self.exit.grid(row=2, column=0, padx=5, pady=5, sticky='NSEW')


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
root.title("SELECT AND GENERATE")
root.minsize(400, 300)

app = Application(root)

root.mainloop()
