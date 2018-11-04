#! python3

import tkinter
from tkinter import *

from tkinter.ttk import *
from tkinter import messagebox

from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

import threading

import setGenerate as sg
import setOddEven as so
import displaySelect as ds
import numberSelect as ns
import os
import pdb
import copy
import random
import shutil
import subprocess as sp
import displayGenerate as dg
import datetime

import dataDownload as dataD

from PIL import Image, ImageTk

class Application(Frame):

    def __init__(self, master):

        self.master = master
        self.main_container = Frame(self.master)

        self.useCount = IntVar()
        self.type = IntVar()

        self.getMatch3 = IntVar()
        self.getMatch4 = IntVar()
        self.getMatch5 = IntVar()
        self.getMatchExtra = IntVar()
        self.numberA = StringVar()
        self.numberB = StringVar()
        self.numberC = StringVar()
        self.numberD = StringVar()
        self.numberE = StringVar()
        self.numberExtra = StringVar()

        # Set images. Note that the line below is needed to change the working directory of the batch file to point to where the script files, including image files are
        # It has to be commented out in the testing library

        # os.chdir("c:\\users\\alan\\documents\\scripts\\code\\sng")

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
        Style().configure("B.TCheckbutton", font="Verdana 8")
        Style().configure("B.TRadiobutton", font="Verdana 8")

        # Set scale styles
        Style().configure("S.TScale", orient=HORIZONTAL, width=25)

        self.parentTab = Notebook(self.main_container)
        self.selTab = Frame(self.parentTab)   # first page, which would get widgets gridded into it
        self.datTab = Frame(self.parentTab)   # second page
        self.abtTab = Frame(self.parentTab)   # third page
        self.parentTab.add(self.selTab, text='    Select    ')
        self.parentTab.add(self.datTab, text='    Data      ')
        self.parentTab.add(self.abtTab, text='    About     ')

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
        self.dSel.append(ds.displayNumbers(self.numberGroup, 75))

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
        self.typeC = Radiobutton(self.typeGroup, text="Mega", style="B.TRadiobutton", command=self.displayDataFile, variable=self.type, value=3)
        self.typeD = Radiobutton(self.typeGroup, text="Powerball", style="B.TRadiobutton", command=self.displayDataFile, variable=self.type, value=4)

        self.sourceLabel = Label(self.selTab, text="None", style="SB.TLabel" )
        self.selectSource = Button(self.selTab, text="SET DATA FILE", style="B.TButton", command=self.setDataFile)
        self.downloadFile = Button(self.selTab, text="DOWNLOAD DATA", style="B.TButton", command=self.downloadThread)
        self.saveSource = Button(self.selTab, text="SAVE", style="B.TButton", command=self.saveDataSource)

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

        self.sourceLabel.grid(row=12, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')
        self.selectSource.grid(row=13, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.downloadFile.grid(row=13, column=2, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.saveSource.grid(row=13, column=4, columnspan=1, padx=5, pady=5, sticky='NSEW')

        self.h_sep_sd.grid(row=14, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        self.showGen.grid(row=15, column=0, columnspan=5, padx=5, pady=(2,5), sticky='NSEW')

        # Create widgets for the Data tab

        self.h_sep_da = Separator(self.datTab, orient=HORIZONTAL)
        self.h_sep_db = Separator(self.datTab, orient=HORIZONTAL)
        self.h_sep_dc = Separator(self.datTab, orient=HORIZONTAL)
        self.h_sep_dd = Separator(self.datTab, orient=HORIZONTAL)
        self.h_sep_de = Separator(self.datTab, orient=HORIZONTAL)
        self.h_sep_df = Separator(self.datTab, orient=HORIZONTAL)

        self.datLabel = Label(self.datTab, text="Data File", style="T.TLabel" )
        self.datLabelA = Label(self.datTab, text="Displays downloaded data from CALottery.com and allows filtering of ", style="B.TLabel" )
        self.datLabelB = Label(self.datTab, text="winning combinations based on provided numbers. Winners that ", style="B.TLabel" )
        self.datLabelC = Label(self.datTab, text="match 3 or 4 numbers from the combination entered are also listed.", style="B.TLabel" )

        self.numberEntry = LabelFrame(self.datTab, text=' Combination ', style="O.TLabelframe")
        self.numA = Entry(self.numberEntry, textvariable=self.numberA, width="5")
        self.numB = Entry(self.numberEntry, textvariable=self.numberB, width="5")
        self.numC = Entry(self.numberEntry, textvariable=self.numberC, width="5")
        self.numD = Entry(self.numberEntry, textvariable=self.numberD, width="5")
        self.numE = Entry(self.numberEntry, textvariable=self.numberE, width="5")
        self.numExtra = Entry(self.numberEntry, textvariable=self.numberExtra, width="5")
        self.extraLabel = Label(self.numberEntry, text="EXTRA", width="7", style="B.TLabel")

        self.filterOpt = LabelFrame(self.datTab, text=' Match Filter Options ', style="O.TLabelframe")
        self.match3 = Checkbutton(self.filterOpt, text=' 3 Numbers ', style="B.TCheckbutton", variable=self.getMatch3)
        self.match4 = Checkbutton(self.filterOpt, text=' 4 Numbers  ', style="B.TCheckbutton", variable=self.getMatch4)
        self.match5 = Checkbutton(self.filterOpt, text=' 5 Numbers  ', style="B.TCheckbutton", variable=self.getMatch5)
        self.matchExtra = Checkbutton(self.filterOpt, text=' Extra ', style="B.TCheckbutton", variable=self.getMatchExtra)

        self.dataDisplay = LabelFrame(self.datTab, text=' Winner Matches ', style="O.TLabelframe")
        self.scroller = Scrollbar(self.dataDisplay, orient=VERTICAL)
        self.dataSelect = Listbox(self.dataDisplay, yscrollcommand=self.scroller.set, width=68, height=8)

        self.filter = Button(self.datTab, text="FILTER", style="B.TButton", command=self.startProcess)
        self.reset = Button(self.datTab, text="RESET", style="B.TButton", command=self.readDataFile)

        self.statusLabel = Label(self.datTab, text="Select source and target folders", style="G.TLabel")
        #self.reset = Button(self.datTab, text="RESET", style="B.TButton", width=30, command=self.resetProcess)
        #self.exit = Button(self.datTab, text="EXIT", style="B.TButton", width=30, command=self.checkExit)

        # Position widgets

        self.datLabel.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')
        self.datLabelA.grid(row=1, column=0, padx=5, pady=0, sticky='NSEW')
        self.datLabelB.grid(row=2, column=0, padx=5, pady=0, sticky='NSEW')
        self.datLabelC.grid(row=3, column=0, padx=5, pady=0, sticky='NSEW')

        self.h_sep_da.grid(row=4, column=0, padx=5, pady=5, sticky='NSEW')

        self.dataSelect.grid(row=0, column=0, padx=(10,0), pady=(5,10), sticky='NSEW')
        self.scroller.grid(row=0, column=2, padx=(10,0), pady=(5,10), sticky='NSEW')
        self.dataDisplay.grid(row=5, column=0, padx=5, pady=5, sticky='NSEW')

        self.h_sep_db.grid(row=9, column=0, padx=5, pady=5, sticky='NSEW')

        self.numA.grid(row=0, column=0, padx=(10,0), pady=(5, 10), sticky='W')
        self.numB.grid(row=0, column=0, padx=(70,0), pady=(5, 10), sticky='W')
        self.numC.grid(row=0, column=0, padx=(130,0), pady=(5, 10), sticky='W')
        self.numD.grid(row=0, column=0, padx=(190,0), pady=(5, 10), sticky='W')
        self.numE.grid(row=0, column=0, padx=(250,0), pady=(5, 10), sticky='W')
        self.extraLabel.grid(row=0, column=0, padx=(320,0), pady=(5, 10), sticky='W')
        self.numExtra.grid(row=0, column=0, padx=(380,0), pady=(5, 10), sticky='W')
        self.numberEntry.grid(row=10, column=0, padx=5, pady=5, sticky='NSEW')

        self.match3.grid(row=0, column=0, padx=(10,0), pady=(5, 10), sticky='W')
        self.match4.grid(row=0, column=0, padx=(120,0), pady=(5, 10), sticky='W')
        self.match5.grid(row=0, column=0, padx=(230,0), pady=(5, 10), sticky='W')
        self.matchExtra.grid(row=0, column=0, padx=(340,0), pady=(5, 10), sticky='W')
        self.filterOpt.grid(row=11, column=0, padx=5, pady=5, sticky='NSEW')

        # self.h_sep_dc.grid(row=12, column=0, padx=5, pady=5, sticky='NSEW')

        self.filter.grid(row=13, column=0, padx=5, pady=5, sticky='NSEW')
        #self.h_sep_dc.grid(row=14, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        #self.reset.grid(row=15, column=0, padx=(10, 0), pady=5, sticky='W')
        #self.exit.grid(row=15, column=0, padx=(245, 0), pady=5, sticky='W')

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
        self.exit.grid(row=5, column=0, padx=5, pady=(2,5), sticky='NSEW')

        # set the type selection to Fantasy Five
        self.type.set(1)

        self.displayDataFile()

    def genOddSet(self):

        ''' This function will initiate the thread for generating combinations
        '''

        t = threading.Thread(None, self.genOddEvenThread(1), ())
        t.start()

    def genEvenSet(self):

        ''' This function will initiate the thread for generating combinations
        '''

        t = threading.Thread(None, self.genOddEvenThread(0), ())
        t.start()

    def genOddEvenThread(self, indicator):

        ''' This function will generate combinations of numbers using the getCombination method of the sg object
        '''

        self.showProgress()

        self.sOE = so.getCombinations(indicator, self.type.get())
        selection, unused = self.sOE.randomSelect()

        self.hideProgress()

        if unused > 0:
            self.unused['text'] = 'Unused: ' + str(unused)
        else:
            self.unused['text'] = ''

        # check the selection limit before showing it. this is needed since the looping limit for generating
        # may be reached without completely generating 5 combinations
        if len(selection) == 5:
            for i in range(5):
                self.dGen[i].changeTopStyle(selection[i])
        else:
            messagebox.showerror('Generate Error', 'Generation taking too long. Retry.')


    def generateSet(self):

        ''' This function will initiate the thread for generating combinations
        '''

        t = threading.Thread(None, self.genSetThread, ())
        t.start()

    def genSetThread(self):

        ''' This function will generate combinations of numbers using the getCombination method of the sg object
        '''

        self.showProgress()

        self.sGen = sg.getCombinations(self.numberSource.getSelectNumbers(), self.type.get(), self.useCount.get())
        selection = self.sGen.randomSelect(self.useCount.get())

        self.hideProgress()

        self.unused['text'] = ''

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

        if self.numberSource.compareSaveSelect():
            pass
        else:

            response = messagebox.askquestion('Select Numbers', 'Do you want to save the current selected numbers?')

            if response == 'yes':
                self.numberSource.writeOutSelected()

        root.destroy()

    def selectSet(self):

        ''' This function will initiate the thread for selecting numbers if a data file is provided
        '''

        if self.sourceLabel["text"] == "None" and (self.type == 1 or self.type ==2):
            messagebox.showerror('Select Error', 'Please select data file before proceeding.')
        else:

            t = threading.Thread(None, self.selectSetThread, ())
            t.start()

    def selectSetThread(self):
        ''' This function will select numbers that will be used for generating combinations. After generating, the
            numbers will be marked accordingly
        '''

        self.dSel[0].changeStyle(self.numberSource.randomSequentialAdd())
        #self.dSel[0].changeStyle(self.numberSource.getFromRecent(25))
        #self.dSel[0].changeStyle(self.numberSource.setSelectNumbers(25))


    def checkSet(self):

        ''' This function will initiate the thread that will generate the statistics from the select numbers
        '''

        if self.sourceLabel["text"] == "None":
            messagebox.showerror('Select Error', 'Please select data file before proceeding.')
        else:

            t = threading.Thread(None, self.checkSetThread, ())
            t.start()

    def checkSetThread(self):

        ''' This function will generate the statistics on the select numbers
        '''

        self.showProgress()
        self.numberSource.analyzeData()
        self.hideProgress()
        self.showStats()


    def clearSelSet(self):

        ''' This function will clear the set of selected numbers
        '''

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
                    self.dataFile = filename
                    self.sourceLabel["text"] = os.path.dirname(filename)[:20] + "..." + os.path.basename(filename)

                    # Create an instance of number source each time a new file is selected
                    self.numberSource = ns.numberSelect(self.dataFile, self.type.get())
                    self.dSel[0].changeStyle(self.numberSource.getSelectNumbers())
                    self.useCount.set(len(self.numberSource.getSelectNumbers()))

                else:
                    messagebox.showerror('Invalid File', 'File selected is not a valid Fantasy Five data file.')

            elif self.type.get() == 2:

                if "SUPERLOTTO" in d_list:
                    self.dataFile = filename
                    self.sourceLabel["text"] = os.path.dirname(filename)[:20] + "..." + os.path.basename(filename)

                    # Create an instance of number source each time a new file is selected
                    self.numberSource = ns.numberSelect(self.dataFile, self.type.get())
                    self.dSel[0].changeStyle(self.numberSource.getSelectNumbers())
                    self.useCount.set(len(self.numberSource.getSelectNumbers()))

                else:
                    messagebox.showerror('Invalid File', 'File selected is not a valid SuperLotto data file.')

            else:
                self.displayDataFile()

    def downloadThread(self):

        t = threading.Thread(None, self.downloadData, ())
        t.start()

    def downloadData(self):

        if self.type.get() == 1:
            baseUrl = 'http://www.calottery.com/play/draw-games/fantasy-5/winning-numbers'
            dataFileName = "data\\FantasyFive.txt"

        elif self.type.get() == 2:
            baseUrl = 'http://www.calottery.com/play/draw-games/superlotto-plus/winning-numbers'
            dataFileName = "data\\SuperLottoPlus.txt"

        else:
            messagebox.showerror("Download Error", "Download not available for game selected.")
            return

        try:
            dataFile = open(dataFileName, "w")
        except:
            os.makedirs("data")
            dataFile = open(dataFileName, "w")

        dataFile.close()

        fileNamePath = os.path.join(os.getcwd(), dataFileName)

        self.showProgress()
        dataD.dataDownload(baseUrl, fileNamePath)
        self.hideProgress()

        self.dataFile = fileNamePath
        self.sourceLabel["text"] = fileNamePath[:20] + '...' + os.path.basename(fileNamePath)

        self.numberSource = ns.numberSelect(self.dataFile, self.type.get())
        self.dSel[0].changeStyle(self.numberSource.getSelectNumbers())
        self.useCount.set(len(self.numberSource.getSelectNumbers()))

        messagebox.showinfo("Download complete", "The latest data file for the selected game hase been downloaded.")

    def saveDataSource(self):

        response = messagebox.askquestion('Save Data Source', 'Do you want to save the current data source?')

        if response == 'no':
            return

        if self.type.get() == 1:
            try:
                configFile = open("data\\cf.txt", "w")
            except:
                os.makedirs("data")
                configFile = open("data\\cf.txt", "w")

            configFile.write(self.dataFile)
            configFile.close()

            messagebox.showinfo("Source File Saved", "The data source file has been saved.")

        elif self.type.get() == 2:
            try:
                configFile = open("data\\cs.txt", "w")
            except:
                os.makedirs("data")
                configFile = open("data\\cs.txt", "w")

            configFile.write(self.dataFile)
            configFile.close()

            messagebox.showinfo("Source File Saved", "The data source file has been saved.")

    def displayDataFile(self):

        ''' This function will display the data file name
        '''

        ltype = self.type.get()

        if ltype == 1:
            config_file = "data\\cf.txt"
        elif ltype == 2:
            config_file = "data\\cs.txt"
        elif ltype == 3:
            config_file = "data\\cm.txt"
        elif ltype == 4:
            config_file = "data\\cp.txt"

        if os.path.exists(config_file):

            configFile = open(config_file, "r")

            filename = configFile.readline()

            if os.path.exists(filename):

                self.dataFile = filename
                self.sourceLabel["text"] = os.path.dirname(filename)[:20] + "..." + os.path.basename(filename)

                self.numberSource = ns.numberSelect(self.dataFile, ltype)
                self.dSel[0].changeStyle(self.numberSource.getSelectNumbers())
                self.useCount.set(len(self.numberSource.getSelectNumbers()))

                if ltype == 1:
                    self.datLabel['text'] = "Fantasy Five Data"
                if ltype == 2:
                    self.datLabel['text'] = "SuperLotto Data"
                if ltype == 3:
                    self.datLabel['text'] = "MegaLotto Data"
                if ltype == 4:
                    self.datLabel['text'] = "Powerball Data"

                self.readDataFile()

            else:
                # delete the contents of the display list, if any
                self.dataSelect.delete(0, END)
                self.sourceLabel["text"] = "None"

            configFile.close()
        else:
            # delete the contents of the display list, if any
            self.dataSelect.delete(0, END)
            self.sourceLabel["text"] = "None"

            # create instance of number select for MegaLotto and Powerball with no file inputs
            self.numberSource = ns.numberSelect(None, ltype)
            self.dSel[0].changeStyle(self.numberSource.getSelectNumbers())
            self.useCount.set(len(self.numberSource.getSelectNumbers()))

            self.datLabel['text'] = "No Data File"


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
        self.optLastCompare = Label(self.popStats, text="", style="B.TLabel" )
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
        self.optLastCompare.grid(row=6, column=0, padx=10, pady=0, sticky='W')

        self.osep_b.grid(row=7, columnspan=3, column=0, padx=5, pady=5, sticky='NSEW')

        self.resultsData.grid(row=8, column=0, rowspan=4, padx=5, pady=5, sticky='NSEW')

        self.osep_c.grid(row=12, columnspan=3, column=0, padx=5, pady=5, sticky='NSEW')

        self.closeStats.grid(row=13, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        last_match, last_compare, first_match, last_match_draws, max_gap, min_gap, exact_match = self.numberSource.getStats()

        self.optLastMatch['text'] = "The last winner from select numbers occured on %s." %last_match
        self.optLastMatchDays ['text']= "It has been %s draws since the last winner from select numbers." %last_match_draws
        self.optExactMatch ['text'] = "The total exact matches from this set is %s since %s." %(exact_match, first_match)
        self.optMaxGap ['text'] = "The maximum draw gap between incidents is %s." %max_gap
        self.optMinGap ['text'] = "The minimum draw gap between incidents is %s." %min_gap
        self.optLastCompare ['text'] = "The last comparison with this select set is %s." %last_compare

        # Set the images

        image = Image.open("data\\results.jpg")
        results_fig = ImageTk.PhotoImage(image)

        # Define a style
        root.results_fig = results_fig
        Style().configure("DT.TLabel", image=results_fig, background="white", anchor="left", font="Verdana 4")

        self.resultsData['style'] = 'DT.TLabel'

        # Set size

        wh = 490
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

        ''' This function will show the generate panel depending on the game type
        '''

        if self.type.get() == 1:
            self.showFantasy()
        elif self.type.get() == 2:
            self.showSuper()
        elif self.type.get() == 3:
            self.showMega()
        elif self.type.get() == 4:
            self.showPower()


    def showFantasy(self):

        ''' This function will show the Fantasy Five generate pane
        '''

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
        self.genOdd = Button(self.popGen, text="ALL ODD", style="B.TButton", command=self.genOddSet)
        self.genEven = Button(self.popGen, text="ALL EVEN", style="B.TButton", command=self.genEvenSet)
        self.unused = Label(self.popGen, text="", style="B.TLabel" )
        self.topLabel = Label(self.popGen, text="Fantasy Five", style="B.TLabel" )
        self.exitGen = Button(self.popGen, text="EXIT", style="B.TButton", command=self.popGen.destroy)

        self.topLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 2), sticky='NSEW')
        self.unused.grid(row=0, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.h_sep_ga.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        for i in range(5):
            self.dGen[i].positionDisplays(5, i)

        self.h_sep_gb.grid(row=15, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

        self.genSet.grid(row=16, column=0, columnspan=3, padx=5, pady=(5, 2), sticky='NSEW')
        self.genOdd.grid(row=16, column=3, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.genEven.grid(row=16, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.exitGen.grid(row=17, column=0, columnspan=5, padx=5, pady=(2, 5), sticky='NSEW')

        wh = 320
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

        ''' This function will show the SuperLotto generate panel
        '''

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

        self.unused = Label(self.popGen, text="", style="B.TLabel" )
        self.topLabel = Label(self.popGen, text="Super Lotto", style="B.TLabel" )

        self.genSet = Button(self.popGen, text="GENERATE", style="B.TButton", command=self.generateSet)
        self.genOdd = Button(self.popGen, text="ALL ODD", style="B.TButton", command=self.genOddSet)
        self.genEven = Button(self.popGen, text="ALL EVEN", style="B.TButton", command=self.genEvenSet)
        self.exitGen = Button(self.popGen, text="EXIT", style="B.TButton", command=self.popGen.destroy)

        self.topLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 2), sticky='NSEW')
        self.unused.grid(row=0, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')

        self.h_sep_ga.grid(row=4, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        for i in range(5):
            self.dGen[i].positionDisplays(5, i)

        self.h_sep_gb.grid(row=20, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

        self.genSet.grid(row=21, column=0, columnspan=3, padx=5, pady=(5, 2), sticky='NSEW')
        self.genOdd.grid(row=21, column=3, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.genEven.grid(row=21, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.exitGen.grid(row=22, column=0, columnspan=5, padx=5, pady=(2, 5), sticky='NSEW')

        wh = 410
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

    def showMega(self):

        ''' This function will show the MegaLotto generate panel
        '''

        self.popGen = Toplevel(self.main_container)
        self.popGen.title("MegaLotto")

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

        self.unused = Label(self.popGen, text="", style="B.TLabel" )
        self.topLabel = Label(self.popGen, text="Super Lotto", style="B.TLabel" )

        self.genSet = Button(self.popGen, text="GENERATE", style="B.TButton", command=self.generateSet)
        self.genOdd = Button(self.popGen, text="ALL ODD", style="B.TButton", command=self.genOddSet)
        self.genEven = Button(self.popGen, text="ALL EVEN", style="B.TButton", command=self.genEvenSet)
        self.exitGen = Button(self.popGen, text="EXIT", style="B.TButton", command=self.popGen.destroy)

        self.topLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 2), sticky='NSEW')
        self.unused.grid(row=0, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')

        self.h_sep_ga.grid(row=4, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        for i in range(5):
            self.dGen[i].positionDisplays(5, i)

        self.h_sep_gb.grid(row=24, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

        self.genSet.grid(row=25, column=0, columnspan=3, padx=5, pady=(5, 2), sticky='NSEW')
        self.genOdd.grid(row=25, column=3, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.genEven.grid(row=25, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.exitGen.grid(row=26, column=0, columnspan=5, padx=5, pady=(2, 5), sticky='NSEW')

        wh = 460
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

    def showPower(self):

        ''' This function will show the MegaLotto generate panel
        '''

        self.popGen = Toplevel(self.main_container)
        self.popGen.title("Powerball")

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

        self.unused = Label(self.popGen, text="", style="B.TLabel" )
        self.topLabel = Label(self.popGen, text="Super Lotto", style="B.TLabel" )

        self.genSet = Button(self.popGen, text="GENERATE", style="B.TButton", command=self.generateSet)
        self.genOdd = Button(self.popGen, text="ALL ODD", style="B.TButton", command=self.genOddSet)
        self.genEven = Button(self.popGen, text="ALL EVEN", style="B.TButton", command=self.genEvenSet)
        self.exitGen = Button(self.popGen, text="EXIT", style="B.TButton", command=self.popGen.destroy)

        self.topLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 2), sticky='NSEW')
        self.unused.grid(row=0, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')

        self.h_sep_ga.grid(row=4, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        for i in range(5):
            self.dGen[i].positionDisplays(5, i)

        self.h_sep_gb.grid(row=25, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

        self.genSet.grid(row=26, column=0, columnspan=3, padx=5, pady=(5, 2), sticky='NSEW')
        self.genOdd.grid(row=26, column=3, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.genEven.grid(row=26, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.exitGen.grid(row=27, column=0, columnspan=5, padx=5, pady=(2, 5), sticky='NSEW')

        wh = 460
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

        ''' This function will show the progress bar for the different threads
        '''

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

    def hideProgress(self):

        self.progressBar.stop()
        self.popProgress.destroy()


    def readDataFile(self, filter=False):

        ''' This function will check for close matches to the numbers entered
        '''

        # Set indicator for finding exact match to False
        self.exactMatch = False

        # delete the contents of the list
        self.dataSelect.delete(0, END)

        filename = self.dataFile
        print(filename)
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

                    if len(d_list) > 10:
                        winner_extra = int(d_list[10])
                    else:
                        winner_extra = ''

                    if filter:
                        self.filterData(winner, winner_extra, d_line)
                    else:
                        self.formatOutput(d_line, 0, 0)


        dataFile.close()

        self.scroller.config(command=self.dataSelect.yview)

    def filterData(self, winner, winner_extra, d_line):

        search_set = [int(self.numberA.get()), int(self.numberB.get()), int(self.numberC.get()), int(self.numberD.get()), int(self.numberE.get())]

        match_ctr = 0

        for w in winner:
            for s in search_set:
                if s == w:
                    match_ctr += 1

        if match_ctr == 3 and self.getMatch3.get() == 1:
            if len(d_line.split()) > 10:
                search_extra = int(self.numberExtra.get())
                if search_extra == winner_extra and self.getMatchExtra.get() == 1:
                    self.formatOutput(d_line, match_ctr, 1)
            else:
                self.formatOutput(d_line, match_ctr, 0)

        elif match_ctr == 4 and self.getMatch4.get() == 1:
            if len(d_line.split()) > 10:
                search_extra = int(self.numberExtra.get())
                if search_extra == winner_extra and self.getMatchExtra.get() == 1:
                    self.formatOutput(d_line, match_ctr, 1)
            else:
                self.formatOutput(d_line, match_ctr, 0)

        elif match_ctr == 5 and self.getMatch5.get() == 1:
            if len(d_line.split()) > 10:
                search_extra = int(self.numberExtra.get())
                if search_extra == winner_extra and self.getMatchExtra.get() == 1:
                    self.exactMatch = True
                    self.formatOutput(d_line, match_ctr, 1)
            else:
                self.formatOutput(d_line, match_ctr, 0)

        if len(d_line.split()) > 10:
            search_extra = int(self.numberExtra.get())
            if search_extra == winner_extra and self.getMatchExtra.get() == 1:
                self.formatOutput(d_line, match_ctr, 1)


    def formatOutput(self, data_line, match_ctr, super_ctr):

        data_list = data_line.split()

        winner_data = []

        # Format draw number
        draw_number = '{:06d}'.format(int(data_list[0]))

        winner_data.append(draw_number)

        in_date = data_list[2] + ' ' + data_list[3] + ' ' + data_list[4]
        draw_date = str(datetime.datetime.strptime(in_date, '%b %d, %Y').date())

        winner_data.append(draw_date)

        for i in range(5, 10):
            number = '{:02d}'.format(int(data_list[i]))
            winner_data.append(number)

        winner_data.append(str(match_ctr))

        if len(data_list) > 10:
            winner_data.append('{:02d}'.format(int(data_list[10])))
            winner_data.append(str(super_ctr))

        format_data_line = "   |   ".join(winner_data)

        self.dataSelect.insert(END, format_data_line)


    def startProcess(self):

        if self.getMatch3.get() == 0 and self.getMatch4.get() == 0 and self.getMatch5.get() == 0 and self.getMatchExtra.get() == 0:

            self.getMatch3.set(1)
            self.getMatch4.set(1)
            self.getMatch5.set(1)
            self.getMatchExtra.set(1)

        self.readDataFile(True)

    def resetProcess(self):

        self.readDataFile(False)

    def checkExit(self):
        pass

root = Tk()
root.title("SELECT AND GENERATE")

# Set size

wh = 550
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
