#! python3

import tkinter
from tkinter import *

from tkinter.ttk import *
from tkinter import messagebox

from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

import threading

import setGenerate as sg
import displaySelect as ds
import numberSelect as ns
import os
import pdb
import copy
import random
import shutil
import subprocess as sp
import displayGenerate as dg

from PIL import Image, ImageTk

class Application(Frame):

    def __init__(self, master):

        self.master = master
        self.main_container = Frame(self.master)

        self.useCount = IntVar()
        self.type = IntVar()

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

        Style().configure("G.TLabel", foreground="white", background="green", font="Courier 8", anchor="center")
        Style().configure("L.TLabel", foreground="white", background="blue", font="Courier 8", anchor="center")
        Style().configure("R.TLabel", foreground="white", background="red", font="Courier 8", anchor="center")
        Style().configure("Y.TLabel", foreground="black", background="yellow", font="Courier 8", anchor="center")
        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")
        Style().configure("T.TLabel", font="Verdana 12 bold")
        Style().configure("S.TLabel", font="Verdana 10")
        Style().configure("B.TLabel", font="Verdana 8")
        Style().configure("SB.TLabel", font="Verdana 8", background="white")

        # Set button styles
        Style().configure("B.TButton", font="Verdana 8", relief="raised")
        Style().configure("B.TRadiobutton", font="Verdana 8")

        # Set scale styles
        Style().configure("S.TScale", orient=HORIZONTAL, width=25)

        self.parentTab = Notebook(self.main_container)
        self.selTab = Frame(self.parentTab)   # first page, which would get widgets gridded into it
        self.abtTab = Frame(self.parentTab)   # second page
        self.parentTab.add(self.selTab, text='    Select  ')
        self.parentTab.add(self.abtTab, text='    About ')

        # Create widgets for the main screen

        self.mainLabel = Label(self.main_container, text="Select and Generate", style="M.TLabel" )
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", command=self.exitRoutine)

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

        self.numberGroup = LabelFrame(self.selTab, text=' Selection ', style="O.TLabelframe")
        self.dSel.append(ds.displayNumbers(self.numberGroup, 47))

        self.selSet = Button(self.selTab, text="SELECT", style="B.TButton", command=self.selectSet)
        self.chkSet = Button(self.selTab, text="CHECK", style="B.TButton", command=self.checkSet)
        self.clearSet = Button(self.selTab, text="CLEAR", style="B.TButton", command=self.clearSelSet)
        self.showGen = Button(self.selTab, text="SHOW GENERATE PANEL", style="B.TButton", command=self.showGenerate)

        self.selectGroup = LabelFrame(self.selTab, text=' Use Counts ', style="O.TLabelframe")
        self.selectionA = Radiobutton(self.selectGroup, text="15", style="B.TRadiobutton", variable=self.useCount, value=15)
        self.selectionB = Radiobutton(self.selectGroup, text="20", style="B.TRadiobutton", variable=self.useCount, value=20)
        self.selectionC = Radiobutton(self.selectGroup, text="25", style="B.TRadiobutton", variable=self.useCount, value=25)

        self.typeGroup = LabelFrame(self.selTab, text=' Game Selection ', style="O.TLabelframe")
        self.typeA = Radiobutton(self.typeGroup, text="Fantasy", style="B.TRadiobutton", command=self.displayDataFile, variable=self.type, value=1)
        self.typeB = Radiobutton(self.typeGroup, text="Super", style="B.TRadiobutton", command=self.displayDataFile, variable=self.type, value=2)
        self.typeC = Radiobutton(self.typeGroup, text="Not Used", style="B.TRadiobutton", command=self.displayDataFile, variable=self.type, value=3)
        self.typeD = Radiobutton(self.typeGroup, text="Not Used", style="B.TRadiobutton", command=self.displayDataFile, variable=self.type, value=4)

        self.sourceLabel = Label(self.selTab, text="None", style="SB.TLabel" )
        self.selectSource = Button(self.selTab, text="SET DATA FILE", style="B.TButton", command=self.setDataFile)

        # Position widgets on the Select tab

        self.selLabel.grid(row=0, column=0, columnspan=5, padx=5, pady=(10,10), sticky='NSEW')
        self.selLabelA.grid(row=2, column=0, columnspan=5, padx=5, pady=(0, 5), sticky='NSEW')

        self.h_sep_sa.grid(row=3, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        self.typeA.grid(row=0, column=0, padx=20, pady=(5, 10), sticky='W')
        self.typeB.grid(row=0, column=1, padx=20, pady=(5, 10), sticky='W')
        self.typeC.grid(row=0, column=2, padx=20, pady=(5, 10), sticky='W')
        self.typeD.grid(row=0, column=3, padx=20, pady=(5, 10), sticky='W')
        self.typeGroup.grid(row=4, column=0, columnspan=5, padx=5, pady=(0,5), sticky='NSEW')

        self.dSel[0].positionDisplays(0, 0)
        self.numberGroup.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.selectionA.grid(row=0, column=0, padx=10, pady=5, sticky='W')
        self.selectionB.grid(row=1, column=0, padx=10, pady=5, sticky='W')
        self.selectionC.grid(row=2, column=0, padx=10, pady=5, sticky='W')
        self.selectGroup.grid(row=5, column=4, columnspan=1, padx=5, pady=5, sticky='NSEW')

        self.h_sep_sb.grid(row=7, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        self.selSet.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.chkSet.grid(row=8, column=2, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.clearSet.grid(row=8, column=4, columnspan=1, padx=5, pady=5, sticky='NSEW')

        self.h_sep_sc.grid(row=9, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        self.sourceLabel.grid(row=12, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')
        self.selectSource.grid(row=12, column=4, columnspan=1, padx=5, pady=5, sticky='NSEW')

        self.h_sep_sd.grid(row=13, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        self.showGen.grid(row=14, column=0, columnspan=5, padx=5, pady=(2,5), sticky='NSEW')

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

        self.aboutText.grid(row=0, column=0, columnspan=5, padx=5, pady=(10,10), sticky='W')
        self.aboutTextA.grid(row=2, column=0, padx=5, pady=0, sticky='W')
        self.aboutTextB.grid(row=3, column=0, padx=5, pady=0, sticky='W')
        self.aboutTextC.grid(row=4, column=0, padx=5, pady=(0,10), sticky='W')
        self.aboutTextD.grid(row=7, column=0, padx=5, pady=0, sticky='W')
        self.aboutTextE.grid(row=8, column=0, padx=5, pady=0, sticky='W')
        self.aboutTextF.grid(row=9, column=0, padx=5, pady=0, sticky='W')

        self.h_sep_aa.grid(row=10, columnspan=5, column=0, padx=5, pady=5, sticky='NSEW')

        self.aboutTextG.grid(row=11, column=0, padx=5, pady=5, sticky='W')
        self.aboutTextH.grid(row=12, column=0, padx=5, pady=0, sticky='W')
        self.aboutTextI.grid(row=13, column=0, padx=5, pady=0, sticky='W')

        self.h_sep_ab.grid(row=14, columnspan=5, column=0, padx=5, pady=5, sticky='NSEW')

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
        self.exit.grid(row=3, column=0, padx=5, pady=(2,5), sticky='NSEW')

        # set the type selection to Fantasy Five
        self.type.set(1)

        self.displayDataFile()

    def generateSet(self):

        t = threading.Thread(None, self.genSetThread, ())
        t.start()

    def genSetThread(self):

        self.showProgress()

        self.sGen = sg.getCombinations(self.numberSource.getSelectNumbers(), self.type.get(), self.useCount.get())
        selection = self.sGen.randomSelect(self.useCount.get())

        self.popProgress.destroy()

        # check the selection limit before showing it. this is needed since the looping limit for generating
        # may be reached without completely generating 5 combinations
        if len(selection) == 5:
            for i in range(5):
                self.dGen[i].changeTopStyle(selection[i])
        else:
            messagebox.showerror('Generate Error', 'Generation taking too long. Retry.')

    def exitRoutine(self):
        ''' This function will be executed when the user exits
        '''
        response = messagebox.askquestion('Select Numbers', 'Do you want to save the current selected numbers?')

        if response == 'yes':
            self.numberSource.writeOutSelected(self.useCount.get())

        root.destroy()

    def selectSet(self):

        if self.sourceLabel["text"] == "None":
            messagebox.showerror('Select Error', 'Please select data file before proceeding.')
        else:
            self.showProgress()
            self.dSel[0].changeStyle(self.numberSource.randomSequentialAdd())
            self.popProgress.destroy()


    def checkSet(self):

        if self.sourceLabel["text"] == "None":
            messagebox.showerror('Select Error', 'Please select data file before proceeding.')
        else:

            t = threading.Thread(None, self.checkSetThread, ())
            t.start()

    def checkSetThread(self):

        self.showProgress()
        self.numberSource.analyzeData()
        self.popProgress.destroy()
        self.showStats()


    def clearSelSet(self):

        if self.sourceLabel["text"] == "None":
            messagebox.showerror('Clear Error', 'Please select data file before proceeding.')
        else:
            self.dSel[0].changeStyle(self.numberSource.clearSelectNumbers())


    def setDataFile(self):

        ''' This function will check if the selected file is valid and display information from the file
        '''

        filename = askopenfilename()

        if os.path.isfile(filename):
            datafile = open(filename)

            # Read the first record on file
            d_line = datafile.readline()
            d_list = d_line.split()

            datafile.close()

            if self.type.get() == 1:

                if "FANTASY" in d_list:
                    try:
                        configFile = open("data\\cf.txt", "w")
                    except:
                        os.makedirs("data")
                        configFile = open("data\\cf.txt", "w")

                    configFile.write(filename)
                    self.dataFile = filename
                    self.sourceLabel["text"] = os.path.dirname(filename)[:15] + ".../" + os.path.basename(filename)

                    # Create an instance of number source each time a new file is selected
                    self.numberSource = ns.numberSelect(self.dataFile, self.type.get())
                    self.dSel[0].changeStyle(self.numberSource.getSelectNumbers())
                    self.useCount.set(len(self.numberSource.getSelectNumbers()))

                    configFile.close()
                else:
                    messagebox.showerror('Invalid File', 'File selected is not a valid Fantasy Five data file.')

            elif self.type.get() == 2:

                if "SUPERLOTTO" in d_list:
                    try:
                        configFile = open("data\\cs.txt", "w")
                    except:
                        os.makedirs("data")
                        configFile = open("data\\cs.txt", "w")

                    configFile.write(filename)
                    self.dataFile = filename
                    self.sourceLabel["text"] = os.path.dirname(filename)[:15] + ".../" + os.path.basename(filename)

                    # Create an instance of number source each time a new file is selected
                    self.numberSource = ns.numberSelect(self.dataFile, self.type.get())
                    self.dSel[0].changeStyle(self.numberSource.getSelectNumbers())
                    self.useCount.set(len(self.numberSource.getSelectNumbers()))

                    configFile.close()
                else:
                    messagebox.showerror('Invalid File', 'File selected is not a valid SuperLotto data file.')

            else:
                self.displayDataFile()


    def displayDataFile(self):

        ''' This function will display the data file name
        '''

        ltype = self.type.get()

        if ltype == 1:

            if os.path.exists("data\\cf.txt"):

                configFile = open("data\\cf.txt", "r")

                filename = configFile.readline()

                if os.path.exists(filename):

                    self.dataFile = filename
                    self.sourceLabel["text"] = os.path.dirname(filename)[:20] + ".../" + os.path.basename(filename)

                    self.numberSource = ns.numberSelect(self.dataFile, ltype)
                    self.dSel[0].changeStyle(self.numberSource.getSelectNumbers())
                    self.useCount.set(len(self.numberSource.getSelectNumbers()))
                else:
                    self.sourceLabel["text"] = "None"

                configFile.close()
            else:
                self.sourceLabel["text"] = "None"

        elif ltype == 2:

            if os.path.exists("data\\cs.txt"):

                configFile = open("data\\cs.txt", "r")

                filename = configFile.readline()

                if os.path.exists(filename):

                    self.dataFile = filename
                    self.sourceLabel["text"] = os.path.dirname(filename)[:20] + ".../" + os.path.basename(filename)

                    self.numberSource = ns.numberSelect(self.dataFile, ltype)
                    self.dSel[0].changeStyle(self.numberSource.getSelectNumbers())
                    self.useCount.set(len(self.numberSource.getSelectNumbers()))
                else:
                    self.sourceLabel["text"] = "None"

                configFile.close()
            else:
                self.sourceLabel["text"] = "None"
        else:
            self.sourceLabel["text"] = "None"

    def showStats(self):

        ''' This function will build the options and other information
        '''

        self.popStats = Toplevel(self.main_container)
        self.popStats.title("Number Stats")

        self.osep_a = Separator(self.popStats, orient=HORIZONTAL)
        self.osep_b = Separator(self.popStats, orient=HORIZONTAL)
        self.osep_c = Separator(self.popStats, orient=HORIZONTAL)

        self.optLastMatch = Label(self.popStats, text="", style="B.TLabel" )
        self.optExactMatch = Label(self.popStats, text="", style="B.TLabel" )
        self.optMaxGap = Label(self.popStats, text="", style="B.TLabel" )
        self.optMinGap = Label(self.popStats, text="", style="B.TLabel" )
        self.optLastMatchDays = Label(self.popStats, text="", style="B.TLabel" )

        self.resultsData = Label(self.popStats)

        self.closeStats = Button(self.popStats, text="CLOSE", style="B.TButton", command=self.popStats.destroy)

        # Position widgets

        self.osep_a.grid(row=0, columnspan=3, column=0, padx=5, pady=5, sticky='NSEW')

        self.optLastMatch.grid(row=1, column=0, padx=10, pady=0, sticky='W')
        self.optExactMatch.grid(row=2, column=0, padx=10, pady=0, sticky='W')
        self.optLastMatchDays.grid(row=3, column=0, padx=10, pady=0, sticky='W')
        self.optMaxGap.grid(row=4, column=0, padx=10, pady=0, sticky='W')
        self.optMinGap.grid(row=5, column=0, padx=10, pady=0, sticky='W')

        self.osep_b.grid(row=6, columnspan=3, column=0, padx=5, pady=5, sticky='NSEW')

        self.resultsData.grid(row=7, column=0, rowspan=4, padx=5, pady=5, sticky='NSEW')

        self.osep_c.grid(row=11, columnspan=3, column=0, padx=5, pady=5, sticky='NSEW')

        self.closeStats.grid(row=12, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        last_match, first_match, last_match_draws, max_gap, min_gap, exact_match = self.numberSource.getStats()

        self.optLastMatch['text'] = "The last winner from select numbers occured on %s." %last_match
        self.optLastMatchDays ['text']= "It has been %s draws since the last winner from select numbers." %last_match_draws
        self.optExactMatch ['text'] = "The total exact matches from this set is %s since %s." %(exact_match, first_match)
        self.optMaxGap ['text'] = "The maximum draw gap between incidents is %s." %max_gap
        self.optMinGap ['text'] = "The minimum draw gap between incidents is %s." %min_gap

        # Set the images

        image = Image.open("data\\results.jpg")
        results_fig = ImageTk.PhotoImage(image)

        # Define a style
        root.results_fig = results_fig
        Style().configure("DT.TLabel", image=results_fig, background="white", anchor="left", font="Verdana 4")

        self.resultsData['style'] = 'DT.TLabel'

        # Set size

        wh = 480
        ww = 420

        #root.resizable(height=False, width=False)

        self.popStats.minsize(ww, wh)
        self.popStats.maxsize(ww, wh)

        # Position in center screen

        ws = self.popStats.winfo_screenwidth()
        hs = self.popStats.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (ww/2)
        y = (hs/2) - (wh/2)

        self.popStats.geometry('%dx%d+%d+%d' % (ww, wh, x, y))


    def showTopValue(self, value=None):

        self.topValue = int(self.topScale.get())
        self.dA[0].changeTopStyle(self.topValue + 1)


    def showExtValue(self, value=None):

        self.extValue = int(self.extScale.get())
        self.dA[0].changeExtStyle(self.extValue + 1)


    def showGenerate(self):

        if self.type.get() == 1:
            self.showFantasy()
        elif self.type.get() == 2:
            self.showSuper()

    def showFantasy(self):

        self.popGen = Toplevel(self.main_container)
        self.popGen.title("Fantasy Five")

        self.h_sep_ga = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gb = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gc = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gd = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_ge = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gf = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gg = Separator(self.popGen, orient=HORIZONTAL)

        self.dGen = []

        for i in range(5):
            self.dGen.append(dg.displayNumbers(self.popGen, self.type.get()))

        self.genSet = Button(self.popGen, text="GENERATE", style="B.TButton", command=self.generateSet)
        self.exitGen = Button(self.popGen, text="EXIT", style="B.TButton", command=self.popGen.destroy)

        self.h_sep_ga.grid(row=4, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        for i in range(5):
            self.dGen[i].positionDisplays(5, i)

        self.h_sep_gb.grid(row=15, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

        self.genSet.grid(row=16, column=0, columnspan=5, padx=5, pady=(5, 2), sticky='NSEW')
        self.exitGen.grid(row=17, column=0, columnspan=5, padx=5, pady=(2, 5), sticky='NSEW')

        wh = 290
        ww = 490

        self.popGen.minsize(ww, wh)
        self.popGen.maxsize(ww, wh)

        # Position in center screen

        ws = self.popGen.winfo_screenwidth()
        hs = self.popGen.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (ww/2)
        y = (hs/2) - (wh/2)

        self.popGen.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

    def showSuper(self):

        self.popGen = Toplevel(self.main_container)
        self.popGen.title("SuperLotto")

        self.h_sep_ga = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gb = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gc = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gd = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_ge = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gf = Separator(self.popGen, orient=HORIZONTAL)
        self.h_sep_gg = Separator(self.popGen, orient=HORIZONTAL)

        self.dGen = []

        for i in range(5):
            self.dGen.append(dg.displayNumbers(self.popGen, self.type.get()))

        self.genSet = Button(self.popGen, text="GENERATE", style="B.TButton", command=self.generateSet)
        self.exitGen = Button(self.popGen, text="EXIT", style="B.TButton", command=self.popGen.destroy)

        self.h_sep_ga.grid(row=4, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        for i in range(5):
            self.dGen[i].positionDisplays(5, i)

        self.h_sep_gb.grid(row=20, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

        self.genSet.grid(row=21, column=0, columnspan=5, padx=5, pady=(5, 2), sticky='NSEW')
        self.exitGen.grid(row=22, column=0, columnspan=5, padx=5, pady=(2, 5), sticky='NSEW')

        wh = 380
        ww = 640

        self.popGen.minsize(ww, wh)
        self.popGen.maxsize(ww, wh)

        # Position in center screen

        ws = self.popGen.winfo_screenwidth()
        hs = self.popGen.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (ww/2)
        y = (hs/2) - (wh/2)

        self.popGen.geometry('%dx%d+%d+%d' % (ww, wh, x, y))


    def showProgress(self):

        Style().configure("P.TLabel", font="Verdana 12 bold", anchor="center")
        Style().configure("B.TProgressbar", foreground="blue", background="blue")

        self.popProgress = Toplevel(self.main_container)
        self.popProgress.title("Processing")

        self.progressMessage = Label(self.popProgress, text="Processing, please wait...", style="P.TLabel" )
        self.progressBar = Progressbar(self.popProgress, orient="horizontal", mode="indeterminate", length=280)

        self.progressMessage.grid(row=0, column=0, columnspan=5, padx=10 , pady=5, sticky='NSEW')
        self.progressBar.grid(row=1, column=0, columnspan=5, padx=10 , pady=5, sticky='NSEW')

        wh = 70
        ww = 300

        self.popProgress.minsize(ww, wh)
        self.popProgress.maxsize(ww, wh)

        # Position in center screen

        ws = self.popProgress.winfo_screenwidth()
        hs = self.popProgress.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (ww/2)
        y = (hs/2) - (wh/2)

        self.popProgress.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

        self.progressBar.start()


root = Tk()
root.title("SELECT AND GENERATE")

# Set size

wh = 500
ww = 480

#root.resizable(height=False, width=False)

root.minsize(ww, wh)
root.maxsize(ww, wh)

# Position in center screen

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (ww/2)
y = (hs/2) - (wh/2)

root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

app = Application(root)

root.mainloop()
