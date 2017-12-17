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
import displayGenerate as dg
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

        self.use_numbers = IntVar()
        self.use_numbers.set(1)

        # Set images. Note that the line below is needed to change the working directory of the batch file to point to where the script files, including image files are
        # It has to be commented out in the testing library
        
        # os.chdir("c:\\users\\alan\\mypythonscripts\\scripts")

        self.topValue = 0
        self.extValue = 0
        self.workDirectory = os.getcwd()
        
        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))

        # Set Label styles
        Style().configure("M.TLabel", font="Verdana 20 bold", anchor="center")

        Style().configure("G.TLabel", foreground= "black", background="green", font="Courier 8", anchor="center")
        Style().configure("L.TLabel", foreground= "white", background="blue", font="Courier 8", anchor="center")
        Style().configure("R.TLabel", foreground= "white", background="red", font="Courier 8", anchor="center")
        Style().configure("Y.TLabel", foreground= "black", background="yellow", font="Courier 8", anchor="center")
        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")
        Style().configure("T.TLabel", font="Verdana 12 bold")
        Style().configure("S.TLabel", font="Verdana 10")
        Style().configure("B.TLabel", font="Verdana 8")

        # Set button styles
        Style().configure("B.TButton", font="Verdana 8", relief="raised")

        # Set scale styles
        Style().configure("S.TScale", orient=HORIZONTAL, width=25)

        self.parentTab = ttk.Notebook(self.main_container)
        self.selTab = ttk.Frame(self.parentTab)   # first page, which would get widgets gridded into it
        self.genTab = ttk.Frame(self.parentTab)   # second page
        self.abtTab = ttk.Frame(self.parentTab)   # second page
        self.parentTab.add(self.selTab, text='    Select  ')
        self.parentTab.add(self.genTab, text='   Generate ')
        self.parentTab.add(self.abtTab, text='    About ')
        
        # Create widgets for the main screen

        self.mainLabel = Label(self.main_container, text="SELECT AND GENERATE", style="M.TLabel" )
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", command=root.destroy)

        # Create widgets for the Select Tab

        self.h_sep_sa = Separator(self.selTab, orient=HORIZONTAL)
        self.h_sep_sb = Separator(self.selTab, orient=HORIZONTAL)
        self.h_sep_sc = Separator(self.selTab, orient=HORIZONTAL)
        self.h_sep_sd = Separator(self.selTab, orient=HORIZONTAL)
        self.h_sep_se = Separator(self.selTab, orient=HORIZONTAL)
        self.h_sep_sf = Separator(self.selTab, orient=HORIZONTAL)
        self.h_sep_sg = Separator(self.selTab, orient=HORIZONTAL)

        self.selLabel = Label(self.selTab, text="Select Options", style="T.TLabel" )
        self.selLabelA = Label(self.selTab, text="Select the numbers to use for generating the combinations", style="B.TLabel" )
        self.selLabelB = Label(self.selTab, text="as well as all the other options. ", style="B.TLabel" )

        self.dSel = []

        self.dSel.append(ds.displayNumbers(self.selTab, 39))

        self.selSet = Button(self.selTab, text="SELECT", style="B.TButton", command=self.selectSet)
        self.chkSet = Button(self.selTab, text="CHECK", style="B.TButton", command=self.checkSet)
        self.clearSet = Button(self.selTab, text="CLEAR", style="B.TButton", command=self.clearSelSet)

        self.useGroup = LabelFrame(self.selTab, text=' Number Use Options ', style="O.TLabelframe")
        self.useSel = Radiobutton(self.useGroup, text="Select Numbers", style="B.TRadiobutton", variable=self.use_numbers, value=1)
        self.useOth = Radiobutton(self.useGroup, text="Other Numbers", style="B.TRadiobutton", variable=self.use_numbers, value=2)
        self.useMix = Radiobutton(self.useGroup, text="Mixed Numbers", style="B.TRadiobutton", variable=self.use_numbers, value=3)

        # Position widgets on the Select tab

        self.selLabel.grid(row=0, column=0, columnspan=5, padx=5, pady=(10,5), sticky='NSEW')
        
        self.h_sep_sa.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        self.selLabelA.grid(row=2, column=0, columnspan=5, padx=5, pady=0, sticky='NSEW')
        
        self.h_sep_sb.grid(row=3, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        self.dSel[0].positionTopDisplays(4, 0)

        self.h_sep_sc.grid(row=7, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        self.selSet.grid(row=8, column=0, padx=(195,5), pady=5, sticky='W')
        self.chkSet.grid(row=8, column=0, padx=(290,5), pady=5, sticky='W')
        self.clearSet.grid(row=8, column=0, padx=(385,5), pady=5, sticky='W')

        self.h_sep_sd.grid(row=9, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        self.useSel.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        self.useOth.grid(row=0, column=0, padx=(140,50), pady=10, sticky='W')
        self.useMix.grid(row=0, column=0, padx=(270,20), pady=10, sticky='W')
        self.useGroup.grid(row=10, column=0, columnspan=3, padx=10, pady=(0,5), sticky='W')

        # Create widgets for the Generate Tab

        self.h_sep_ga = Separator(self.genTab, orient=HORIZONTAL)
        self.h_sep_gb = Separator(self.genTab, orient=HORIZONTAL)
        self.h_sep_gc = Separator(self.genTab, orient=HORIZONTAL)
        self.h_sep_gd = Separator(self.genTab, orient=HORIZONTAL)
        self.h_sep_ge = Separator(self.genTab, orient=HORIZONTAL)
        self.h_sep_gf = Separator(self.genTab, orient=HORIZONTAL)
        self.h_sep_gg = Separator(self.genTab, orient=HORIZONTAL)

        self.dGen = []
        
        for i in range(5):
            self.dGen.append(dg.displayNumbers(self.genTab, 39))
                    
        self.genLabel = Label(self.genTab, text="Generate Combinations", style="T.TLabel" )
        self.genLabelA = Label(self.genTab, text="Generate the combinations using the numbers and options selected. ", style="B.TLabel" )
        self.genLabelB = Label(self.genTab, text="Combinations will be color-coded to indicate probability of winning. ", style="B.TLabel" )
        
        self.topScale = Scale(self.genTab, from_=0, to=75, command=self.showTopValue, orient=HORIZONTAL)
        self.extScale = Scale(self.genTab, from_=0, to=30, command=self.showExtValue, orient=HORIZONTAL)

        self.genSet = Button(self.genTab, text="GENERATE", style="B.TButton", command=self.generateSet)
        self.clearSet = Button(self.genTab, text="CLEAR", style="B.TButton", command=self.clearGenSet)
        
        # Position widgets on the generate tab

        self.genLabel.grid(row=0, column=0, columnspan=5, padx=5, pady=(10,5), sticky='NSEW')

        self.h_sep_ga.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        self.genLabelA.grid(row=2, column=0, columnspan=5, padx=5, pady=0, sticky='NSEW')
        self.genLabelB.grid(row=3, column=0, columnspan=5, padx=5, pady=0, sticky='NSEW')
        
        self.h_sep_gb.grid(row=4, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        for i in range(5):
            self.dGen[i].positionTopDisplays(5, i)
                
        self.h_sep_gc.grid(row=15, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')        
        
        self.genSet.grid(row=16, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.clearSet.grid(row=16, column=3, columnspan=2, padx=5, pady=5, sticky='NSEW')

        # Create widgets for About tab

        self.h_sep_aa = Separator(self.abtTab, orient=HORIZONTAL)
        self.h_sep_ab = Separator(self.abtTab, orient=HORIZONTAL)
        self.h_sep_ac = Separator(self.abtTab, orient=HORIZONTAL)
        self.h_sep_ad = Separator(self.abtTab, orient=HORIZONTAL)

        self.aboutText  = Label(self.abtTab, text="About this script", style="T.TLabel" )
        self.aboutTextA = Label(self.abtTab, text="This script can be used to generate numbers for the Fantasy Five game in ", style="B.TLabel" )
        self.aboutTextB = Label(self.abtTab, text="California Lottery. This script will require a valid Fantasy Five data", style="B.TLabel" )
        self.aboutTextC = Label(self.abtTab, text="file that may be downloaded from the California Lottery website", style="B.TLabel" )
        self.aboutTextD = Label(self.abtTab, text="The numbers generated can be set to come randomly from all numbers in the ", style="B.TLabel" )
        self.aboutTextE = Label(self.abtTab, text="selection or from a select group of numbers that are randomly selected.", style="B.TLabel" )
        self.aboutTextF = Label(self.abtTab, text="Combination generated can only have one pair of consecutive numbers.", style="B.TLabel" )

        self.aboutTextG = Label(self.abtTab, text="Color coding", style="T.TLabel" )
        self.aboutTextH = Label(self.abtTab, text="Combinations are color-coded depending on their likelyhood of occurence", style="B.TLabel" )
        self.aboutTextI = Label(self.abtTab, text="based on data provided. The color codes are listed below", style="B.TLabel" )

        self.legendBest = Label(self.abtTab, width=2, style="G.TLabel" )
        self.legendGood = Label(self.abtTab, width=2, style="L.TLabel" )
        self.legendLowC = Label(self.abtTab, width=2, style="Y.TLabel" )
        self.legendPrev = Label(self.abtTab, width=2, style="R.TLabel" )

        self.bestText = Label(self.abtTab, text="3O - 3E - High Occurence", style="B.TLabel" )
        self.goodText = Label(self.abtTab, text="4O - 4E - Low Occurence", style="B.TLabel" )
        self.lowCText = Label(self.abtTab, text="5O - 5E - Rare Occurence", style="B.TLabel" )
        self.prevText = Label(self.abtTab, text="Past Winner", style="B.TLabel" )

        # Position widgets in About tab

        self.aboutText.grid(row=0, column=0, columnspan=5, padx=5, pady=(10,5), sticky='W')

        self.h_sep_aa.grid(row=1, columnspan=5, column=0, padx=5, pady=5, sticky='NSEW')

        self.aboutTextA.grid(row=2, column=0, padx=10, pady=0, sticky='W')
        self.aboutTextB.grid(row=3, column=0, padx=10, pady=0, sticky='W')
        self.aboutTextC.grid(row=4, column=0, padx=10, pady=0, sticky='W')

        self.h_sep_ab.grid(row=6, columnspan=5, column=0, padx=5, pady=5, sticky='NSEW')

        self.aboutTextD.grid(row=7, column=0, padx=10, pady=0, sticky='W')
        self.aboutTextE.grid(row=8, column=0, padx=10, pady=0, sticky='W')
        self.aboutTextF.grid(row=9, column=0, padx=10, pady=0, sticky='W')

        self.h_sep_ac.grid(row=10, columnspan=5, column=0, padx=5, pady=5, sticky='NSEW')

        self.aboutTextG.grid(row=11, column=0, padx=5, pady=5, sticky='W')
        self.aboutTextH.grid(row=12, column=0, padx=10, pady=0, sticky='W')
        self.aboutTextI.grid(row=13, column=0, padx=10, pady=0, sticky='W')

        self.h_sep_ad.grid(row=14, columnspan=5, column=0, padx=5, pady=5, sticky='NSEW')

        self.legendBest.grid(row=15, column=0, padx=10, pady=5, sticky='W')
        self.bestText.grid(row=15, column=0, padx=(40,10), pady=5, sticky='W')
        self.legendGood.grid(row=15, column=0, padx=(220, 10), pady=5, sticky='W')
        self.goodText.grid(row=15, column=0, padx=(250,10), pady=5, sticky='W')
        self.legendLowC.grid(row=16, column=0, padx=10, pady=5, sticky='W')
        self.lowCText.grid(row=16, column=0, padx=(40,10), pady=5, sticky='W')
        self.legendPrev.grid(row=16, column=0, padx=(220,10), pady=5, sticky='W')
        self.prevText.grid(row=16, column=0, padx=(250,10), pady=5, sticky='W')

        self.mainLabel.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')
        self.parentTab.grid(row=1, column=0, padx=5, pady=5, sticky='NSEW')
        self.exit.grid(row=2, column=0, padx=5, pady=(5,10), sticky='NSEW')


    def generateSet(self):

        pass

    def clearGenSet(self):

        pass

    def selectSet(self):

        pass

    def checkSet(self):

        pass

    def clearSelSet(self):

        pass

    def showTopValue(self, value=None):

        self.topValue = int(self.topScale.get())

        
        self.dA[0].changeTopStyle(self.topValue + 1)


    def showExtValue(self, value=None):

        self.extValue = int(self.extScale.get())

        self.dA[0].changeExtStyle(self.extValue + 1)


    def clearGen(self):

        response = tkMessageBox.askquestion('Clear', 'Clear the generated combinations?')

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
