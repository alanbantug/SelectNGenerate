#! python3

import Tkinter
from Tkinter import *

import ttk
from ttk import *

from tkFileDialog import askdirectory
from tkFileDialog import askopenfilename

# import the dataloader

#import numberSelection as ns
import displayNumbers as dn
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

        self.noConsec = IntVar()
        self.winnerUseCount = StringVar()
        self.winnerPassCount = StringVar()
        self.patternOpt = IntVar()
        self.spreadOut = IntVar()

        self.workDirectory = os.getcwd()
        
        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))

        # Set Label styles
        Style().configure("FF.TLabel", background="blue", foreground="yellow", font="Courier 20 bold", anchor="center")
        Style().configure("M.TLabel", font="Verdana 14", foreground="yellow", background="blue", height="20", anchor="center")
        Style().configure("N.TLabel", font="Verdana 10", background="white", height=80, width=30)
        Style().configure("T.TLabel", font="Verdana 10", foreground="black", background="white", anchor="center")
        Style().configure("G.TLabel", foreground= "white", background="green", font="Courier 8", anchor="center")
        Style().configure("L.TLabel", foreground= "white", background="blue", font="Courier 8", anchor="center")
        Style().configure("R.TLabel", foreground= "white", background="red", font="Courier 8", anchor="center")
        Style().configure("Y.TLabel", foreground= "blue", background="yellow", font="Courier 8", anchor="center")
        Style().configure("O.TLabel", foreground= "white", background="orange", font="Courier 8", anchor="center")
        Style().configure("B.TLabel", font="Verdana 8")
        Style().configure("SB.TLabel", font="Verdana 8", background="white")
        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")

        # Set button styles
        Style().configure("B.TButton", font="Verdana 8", relief="raised", width=18)
        Style().configure("S.TButton", font="Verdana 8", relief="raised", width=10)

        # Set check box and radio button styles
        Style().configure("B.TCheckbutton", font="Verdana 8")
        Style().configure("B.TRadiobutton", font="Verdana 8")
        
        # Create widgets
        self.h_sep_a = Separator(self.main_container, orient=HORIZONTAL)
        self.h_sep_b = Separator(self.main_container, orient=HORIZONTAL)
        self.h_sep_c = Separator(self.main_container, orient=HORIZONTAL)
        self.h_sep_d = Separator(self.main_container, orient=HORIZONTAL)
        self.h_sep_e = Separator(self.main_container, orient=HORIZONTAL)
        self.h_sep_f = Separator(self.main_container, orient=HORIZONTAL)
        self.h_sep_g = Separator(self.main_container, orient=HORIZONTAL)

        # Create widgets
        self.v_sep_a = Separator(self.main_container, orient=VERTICAL)
        self.v_sep_b = Separator(self.main_container, orient=VERTICAL)
        self.v_sep_c = Separator(self.main_container, orient=VERTICAL)
        self.v_sep_d = Separator(self.main_container, orient=VERTICAL)

        self.dA = []
        
        self.dA.append(dn.displayNumbers(self.main_container, 75, 30))
            
        self.mainLabel = Label(self.main_container, text="SELECT AND GENERATE", style="FF.TLabel" )
        self.topScaleL = Label(self.main_container, text="", style="T.TLabel" )
        self.extScaleL = Label(self.main_container, text="", style="T.TLabel" )

        self.topScale = Scale(self.main_container, from_=1, to=75)
        self.extScale = Scale(self.main_container, from_=1, to=30)

        # bind

        self.topScale.bind('<B1-Motion>', self.enterTopEvent())
        
        #self.randomSelect = Button(self.main_container, text="SELECT DATA FILE", style="B.TButton", command=self.selectRandom)
        #self.save = Button(self.main_container, text="SAVE COMBINATIONS TO FILE", style="B.TButton", command=self.saveCombinations)
        #self.delete = Button(self.main_container, text="DELETE COMBINATIONS FILE", style="B.TButton", command=self.deleteCombinations)
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", command=root.destroy)

        #self.progress_bar = Progressbar(self.main_container, orient="horizontal", mode="indeterminate", maximum=100)

        # Position widgets        
        self.mainLabel.grid(row=0, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')
        
        self.h_sep_a.grid(row=1, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

        offset = 0
        
        self.dA[0].positionTopDisplays(2, 0)

        self.topScale.grid(row=7, column=0, padx=5, pady=5, sticky='NSEW')

        self.h_sep_b.grid(row=8, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')        
        
        self.dA[0].positionExtDisplays(9, 0)

        self.extScale.grid(row=11, column=0, padx=5, pady=5, sticky='NSEW')
        #offset += 1
            
        self.h_sep_c.grid(row=12, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

        #self.submit.grid(row=18, column=0, columnspan=6, padx=10, pady=5, sticky='NSEW')
        #self.options.grid(row=18, column=6, columnspan=4, padx=10, pady=5, sticky='NSEW')

        #self.save.grid(row=19, column=0, columnspan=3, padx=10, pady=5, sticky='NSEW')
        #self.delete.grid(row=19, column=3, columnspan=3, padx=10, pady=5, sticky='NSEW')
        self.exit.grid(row=13, column=0, padx=10, pady=5, sticky='NSEW')
        
        self.h_sep_d.grid(row=14, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')

        #self.sourceLabel.grid(row=21, column=0, columnspan=7, padx=10 , pady=5, sticky='NSEW')
        #self.selectSource.grid(row=21, column=7, columnspan=3, padx=10, pady=5, sticky='NSEW')
        #self.h_sep_e.grid(row=22, column=0, columnspan=10, padx=5, pady=5, sticky='NSEW')
        #self.progress_bar.grid(row=23, columnspan=10, column=0, padx=10 , pady=(5,10), sticky='NSEW')

        # Add code to write datafile selected if config file exits. Write 'None' if file has not been selected

        #self.displayDataFile()

    def enterTopEvent(self):

        topSelect = self.topScale.get()
        
        if topSelect > 0:
            print topSelect
            self.dA[0].changeTopStyle(topSelect)


    def leaveTopEvent(self):
        
        topSelect = self.topScale.get()

        if topSelect > 0:
            self.dA[0].changeTopStyle(topSelect)

    def generate(self):

        import threading

        t = threading.Thread(None, self.generateNumbers, ())
        t.start()

        
    def generateNumbers(self):

        self.progress_bar.start(10)

        while True:

            score = 0
            not_used = 0

            self.num = []
            self.numStyle = []
        
            for i in range(10):
                self.num.append([])
                    
            selection = ns.numberSelection(self.noConsec.get(), self.winnerUseCount.get(), self.winnerPassCount.get(), self.patternOpt.get())

            g_count = 0
            
            while (True):
                
                score += self.checkNumberSets(selection,g_count)

                g_count += 1
                if g_count == 10:
                    break
                    
            if self.patternOpt.get() > 0:

                if self.noConsec.get() == 0:
                                    
                    if self.patternOpt.get() == 1:
                        if score == 10:
                            break
                    elif self.patternOpt.get() == 2:
                        if score >= 6:
                            break
                    elif self.patternOpt.get() == 3:
                        if score >= 3:
                            break
                else:

                    if self.patternOpt.get() == 1:
                        if score >= 8:
                            break
                    elif self.patternOpt.get() == 2:
                        if score >= 4:
                            break
                    elif self.patternOpt.get() == 3:
                        if score >= 2:
                            break

            else:

                if self.patternOpt.get() == 0 and self.spreadOut.get() == 1:

                    if score == 10:
                        break

                else:
                    
                    if score >= 7:
                        break

        self.progress_bar.stop()
        
        for i in range(10):
            self.dA[i].changeStyle(self.numStyle[i], self.num[i])
            
        self.checkUnusedNumbers()
        

    def checkNumberSets(self,selection,idx):
        
        checkSet = []
        set_score = 0
            
        for item,num in enumerate(selection.getSet()):
            self.num[idx].append(num)

        checkSet = self.num[idx]
        
        setStyle, sameCount, conCount, preCount, concentrated, matchThreeFnd = self.scoreSet(selection, checkSet)

        self.numStyle.append(setStyle)
        
        p_score = set_score

        if setStyle == "G.TLabel":
            set_score += 1

        if setStyle == "L.TLabel":
            set_score += 0.5

        if setStyle == "O.TLabel":
            set_score += 0.25

        if self.noConsec.get() == 1:
            if conCount > 0:
                set_score = p_score
        else:
            if conCount > 1:
                set_score = p_score

        if self.patternOpt.get() > 0:

            if self.spreadOut.get() == 1:
                if concentrated:
                    set_score = p_score
                
            if preCount > 1:
                set_score = p_score

            if self.checkCombinationsFile(checkSet):
                set_score = p_score

            if matchThreeFnd:
                set_score = p_score

        # if combination has two or more of the same number, set the score to a negative to make sure it will not pass

        if sameCount > 1:
            set_score -= 5
            
        return set_score


    def scoreSet(self, selection, checkSet):

        conCount = 0
        preCount = 0
        sameCount = 0
        matchThreeFnd = self.checkMatchThree(checkSet)

        # check the count of numbers from the previous winner

        for i in range(5):
            if checkSet[i] in selection.getLast():
                preCount += 1

        # Check for consecutive numbers
        
        for i in range(4):
            if checkSet[i + 1] == checkSet[i] + 1:
                conCount += 1

        # Check for same numbers in the same combination
        
        for i in range(4):
            if checkSet[i + 1] == checkSet[i]:
                sameCount += 1

        # Add code here to check if numbers are well distributed, that is, no more than two numbers are in the same range

        concentrated = False

        dis_count = 0

        for i in range(5):

            if checkSet[i] in [1,2,3,4,5,6,7,8,9]:
                dis_count += 1

        if dis_count > 2:
            concentrated = True

        dis_count = 0

        for i in range(5):

            if checkSet[i] in [10,11,12,13,14,15,16,17,18,19]:
                dis_count += 1

        if dis_count > 2:
            concentrated = True

        dis_count = 0
        
        for i in range(5):

            if checkSet[i] in [20,21,22,23,24,25,26,27,28,29]:
                dis_count += 1

        if dis_count > 2:
            concentrated = True

        dis_count = 0
        
        for i in range(5):

            if checkSet[i] in [30,31,32,33,34,35,36,37,38,39]:
                dis_count += 1

        dis_count = 0
        
        for i in range(5):

            if checkSet[i] in [40,41,42,43,44,45,46,47]:
                dis_count += 1

        if dis_count > 2:
            concentrated = True
        
        # if combination is a previous winner, return right away
        
        if self.checkIfWinner(checkSet):
            return "R.TLabel", sameCount, conCount, preCount, concentrated, matchThreeFnd

        e_count = 0
        
        for i in range(5):
            if checkSet[i] % 2 == 0:
                e_count += 1

        if e_count == 0 or e_count == 5:
            return "O.TLabel", sameCount, conCount, preCount, concentrated, matchThreeFnd

        if e_count == 1 or e_count == 4:
            return "L.TLabel", sameCount, conCount, preCount, concentrated, matchThreeFnd

        if e_count == 2 or e_count == 3:
            return "G.TLabel", sameCount, conCount, preCount, concentrated, matchThreeFnd
        

    def checkMatchThree(self, checkSet):

        match_three = 0
        rec_ctr = 0
        
        # Get file and path of latest data file

        if os.path.isfile("config.txt"):
            pass
        else:
            return False
        
        configFile = open("config.txt", "r")
        filename = configFile.readline()
        configFile.close()

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

                    match = 0
                    for i in range(5, 10):
                        match += checkSet.count(int(d_list[i]))

                    if match == 3:
                        match_three += 1

                    rec_ctr += 1

                    if rec_ctr == 50:
                        break
        
        dataFile.close()
        
        if match_three > 0:
            return True
        else:
            return False
        

    def checkIfWinner(self, checkSet):

        # If config file does not exist, return False

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

                    if checkSet == winner:
                        return True

        dataFile.close()
        return False
    

    def checkCombinationsFile(self, checkSet):

        if os.path.isfile("combination.txt"):
            pass
        else:
            return False
        
        combinationFile = open("combination.txt", "r")
        s_count = 0

        while True:
        
            c_line = combinationFile.readline()

            if c_line == "":
                break

            c_list = c_line.split(" - ")

            s_count = 0
            
            for i in range(5):
                s_count += checkSet.count(int(c_list[i]))

            if s_count > 2:
                break
                            
        combinationFile.close()

        if s_count > 3:
            return True
        else:
            return False
    

    def checkUnusedNumbers(self):

        usedNumbers = []
        unUsed = []

        for i in range(10):
            for j in range(5):
                if self.num[i][j] in usedNumbers:
                    pass
                else:
                    usedNumbers.append(self.num[i][j])

        usedNumbers.sort()

        for i in range(1, 48):
            if i in usedNumbers:
                pass
            else:
                unUsed.append(str(i))

        if len(unUsed) > 0:
            self.showUnusedNumbers(unUsed)
        

    def showUnusedNumbers(self, unUsed):
        
        self.popUnused = Toplevel(self.main_container)
        self.popUnused.title("Unused Numbers")
        self.popUnused.minsize(160, 130)

        self.osep_a = Separator(self.popUnused, orient=HORIZONTAL)
        self.osep_b = Separator(self.popUnused, orient=HORIZONTAL)
        
        self.unusedLabel = Label(self.popUnused, text="Unused Number(s)", style="B.TLabel" )
        self.unusedList = Label(self.popUnused, style="SB.TLabel" )
        
        self.close = Button(self.popUnused, text="CLOSE", style="B.TButton", command=self.popUnused.destroy)

        self.unusedLabel.grid(row=1, column=0, padx=10, pady=(10,5), sticky='W')
        self.osep_a.grid(row=2, column=0, padx=5, pady=5, sticky='NSEW')
        self.unusedList.grid(row=3, column=0, padx=10, pady=(10,5), sticky='W')
        self.osep_b.grid(row=4, column=0, padx=5, pady=5, sticky='NSEW')
        self.close.grid(row=5, column=0, padx=10, pady=5, sticky='NSEW')

        self.unusedList["text"] = ", ".join(unUsed)

        
    def showOptions(self):

        self.popOptions = Toplevel(self.main_container)
        self.popOptions.title("OPTIONS")
        self.popOptions.maxsize(440,450)
        self.popOptions.minsize(440,450)

        self.osep_a = Separator(self.popOptions, orient=HORIZONTAL)
        self.osep_b = Separator(self.popOptions, orient=HORIZONTAL)
        self.osep_c = Separator(self.popOptions, orient=VERTICAL)
        self.osep_d = Separator(self.popOptions, orient=HORIZONTAL)
        self.osep_e = Separator(self.popOptions, orient=HORIZONTAL)
        self.osep_f = Separator(self.popOptions, orient=HORIZONTAL)
        self.osep_g = Separator(self.popOptions, orient=HORIZONTAL)
        self.osep_h = Separator(self.popOptions, orient=VERTICAL)
        
        self.consecutives = Checkbutton(self.popOptions, text="No Consecutive Numbers", style="B.TCheckbutton", variable=self.noConsec) 
        self.optionsTextA = Label(self.popOptions, text="Check this box to avoid consecutive numbers", style="B.TLabel" )

        self.optionsTextB = Label(self.popOptions, text="Note: You can only set one of the three options", style="B.TLabel" )
        
        self.winnerAGroup = LabelFrame(self.popOptions, text=' 2. Pass Winner Options ', style="O.TLabelframe", width=300)
        self.passText = Label(self.winnerAGroup, text="Pass Count:", style="B.TLabel")
        self.passWinners = OptionMenu(self.winnerAGroup, self.winnerPassCount, " ", "0", "1", "2", command=self.selectWinnerPass)
        self.winnerBGroup = LabelFrame(self.popOptions, text=' 1. Use Winner Options ', style="O.TLabelframe", width=300)
        self.useText = Label(self.winnerBGroup, text="Use Count:", style="B.TLabel")
        self.useWinners = OptionMenu(self.winnerBGroup, self.winnerUseCount, " ", "0", "11", "12", command=self.selectWinnerUse)

        self.patGroup = LabelFrame(self.popOptions, text=' 3. Pattern Use Options ', style="O.TLabelframe")
        self.anyPattern = Radiobutton(self.patGroup, text="Random", style="B.TRadiobutton", variable=self.patternOpt, value=0)
        self.evenOdd3 = Radiobutton(self.patGroup, text="3E - 3O", style="B.TRadiobutton", variable=self.patternOpt, value=1, command=self.selectPatternUse)
        self.evenOdd4 = Radiobutton(self.patGroup, text="4E - 4O", style="B.TRadiobutton", variable=self.patternOpt, value=2, command=self.selectPatternUse)
        self.evenOdd5 = Radiobutton(self.patGroup, text="5E - 5O", style="B.TRadiobutton", variable=self.patternOpt, value=3, command=self.selectPatternUse)
        self.osep_i = Separator(self.patGroup, orient=HORIZONTAL)
        self.spread = Checkbutton(self.patGroup, text="Spread Out Numbers", style="B.TCheckbutton", variable=self.spreadOut) 
        self.optionsTextC = Label(self.patGroup, text="Check this box to avoid packing of numbers in one range" , style="B.TLabel" )

        self.optionsTextD = Label(self.popOptions, text="COLOR CODE DESCRIPTIONS", style="B.TLabel" )
        
        self.legendBest = Label(self.popOptions, width=2, style="G.TLabel" )
        self.legendGood = Label(self.popOptions, width=2, style="L.TLabel" )
        self.legendLowC = Label(self.popOptions, width=2, style="O.TLabel" )
        self.legendPrev = Label(self.popOptions, width=2, style="R.TLabel" )

        self.bestText = Label(self.popOptions, text="3O - 3E - High Occurence", style="B.TLabel" )
        self.goodText = Label(self.popOptions, text="4O - 4E - Low Occurence", style="B.TLabel" )
        self.lowCText = Label(self.popOptions, text="5O - 5E - Rare Occurence", style="B.TLabel" )
        self.prevText = Label(self.popOptions, text="Past Winner", style="B.TLabel" )

        self.closeOptions = Button(self.popOptions, text="CLOSE", style="B.TButton", command=self.popOptions.destroy)

        # Position widgets

        self.consecutives.grid(row=0, column=0, padx=10, pady=5, sticky='W')
        self.optionsTextA.grid(row=1, columnspan=3, column=0, padx=10, pady=0, sticky='W')

        self.osep_a.grid(row=2, columnspan=3, column=0, padx=5, pady=5, sticky='NSEW')

        self.optionsTextB.grid(row=3, columnspan=3, column=0, padx=10, pady=0, sticky='W')

        self.osep_b.grid(row=4, columnspan=3, column=0, padx=5, pady=5, sticky='NSEW')

        self.useText.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        self.useWinners.grid(row=0, column=0, padx=(130,20), pady=10, sticky='W')
        self.winnerBGroup.grid(row=5, column=0, padx=10, pady=(0,5), sticky='W')

        self.osep_c.grid(row=5, rowspan=1, column=1, padx=5, pady=5, sticky='NSEW')

        self.passText.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        self.passWinners.grid(row=0, column=0, padx=(130,20), pady=10, sticky='W')
        self.winnerAGroup.grid(row=5, column=2, padx=10, pady=(0,5), sticky='W')

        self.osep_d.grid(row=6, columnspan=3, column=0, padx=5, pady=5, sticky='NSEW')

        self.anyPattern.grid(row=0, column=0, padx=10, pady=10, sticky='W')
        self.evenOdd3.grid(row=0, column=0, padx=(120,10), pady=10, sticky='W')
        self.evenOdd4.grid(row=0, column=0, padx=(230,10), pady=10, sticky='W')
        self.evenOdd5.grid(row=0, column=0, padx=(330,15), pady=10, sticky='W')
        self.osep_i.grid(row=1, column=0, padx=10, pady=5, sticky='NSEW')
        self.spread.grid(row=2, column=0, padx=10, pady=0, sticky='W')
        self.optionsTextC.grid(row=3, column=0, padx=10, pady=(5,10), sticky='W')
        self.patGroup.grid(row=7, column=0, columnspan=3, padx=10, pady=(0,5), sticky='W')
        
        self.osep_e.grid(row=10, columnspan=3, column=0, padx=5, pady=5, sticky='NSEW')
        
        self.optionsTextD.grid(row=11, column=0, padx=10, pady=5, sticky='W')
        
        self.osep_f.grid(row=12, columnspan=3, column=0, padx=5, pady=5, sticky='NSEW')

        self.legendBest.grid(row=13, column=0, padx=10, pady=(0,5), sticky='W')
        self.bestText.grid(row=13, column=0, padx=(40,10), pady=5, sticky='W')

        self.osep_h.grid(row=13, rowspan=2, column=1, padx=5, pady=5, sticky='NSEW')

        self.legendLowC.grid(row=13, column=2, padx=10, pady=(0,5), sticky='W')
        self.lowCText.grid(row=13, column=2, padx=(40,10), pady=5, sticky='W')

        self.legendGood.grid(row=14, column=0, padx=10, pady=5, sticky='W')
        self.goodText.grid(row=14, column=0, padx=(40,10), pady=5, sticky='W')
        self.legendPrev.grid(row=14, column=2, padx=10, pady=5, sticky='W')
        self.prevText.grid(row=14, column=2, padx=(40,10), pady=5, sticky='W')

        self.osep_g.grid(row=15, columnspan=3, column=0, padx=5, pady=5, sticky='NSEW')
        
        self.closeOptions.grid(row=16, column=0, columnspan=3, padx=10, pady=5, sticky='NSEW')


    def selectWinnerPass(self,value):

        # this procedure will run if winners will be passed over. Other options will be set to default values

        if value == " " or value == "0":
            pass
        else:
            self.patternOpt.set(0)
            self.spreadOut.set(0)
            self.winnerUseCount.set("0")


    def selectWinnerUse(self,value):

        # this procedure will run if winners will be used. Other options will be set to default values

        if value == " " or value == "0":
            pass
        else:
            self.patternOpt.set(0)
            self.spreadOut.set(0)
            self.winnerPassCount.set("0")
        

    def selectPatternUse(self):

        # if a pattern is selected, no numbers will be excluded from selection and numbers will be group by even or odd nature
        
        if self.patternOpt.get() > 0:
            self.winnerPassCount.set("0")
            self.winnerUseCount.set("0")
            self.spread.config(state='normal')
        else:
            self.spread.config(state='disabled')


    def setDataFile(self):

        filename = askopenfilename()

        if os.path.isfile(filename):
            datafile = open(filename)

            # Read the first record on file
            d_line = datafile.readline()
            d_list = d_line.split()

            datafile.close()
        
            if "SUPERLOTTO" in d_list:
                configFile = open("config.txt", "w")

                configFile.write(filename)
                self.sourceLabel["text"] = filename
                
                configFile.close()

                self.displayCounts()
            else:
                self.displayDataFile()

    def displayCounts(self):

        # This functions will display the number of unique numbers in the last two, last five and last ten winning combinations

        rec_ctr = 0
        count_two = 0
        count_six = 0
        count_twelve = 0
        count_set = []
        latest_winner = []
        
        configFile = open("config.txt", "r")
        filename = configFile.readline()
        configFile.close()
        
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

                    for i in range(5,11):
                        if int(d_list[i]) in count_set:
                            pass
                        else:
                            count_set.append(int(d_list[i]))

                    rec_ctr += 1

                    if rec_ctr == 1:
                        latest_winner = copy.copy(count_set)

                    if rec_ctr == 2:
                        count_two = len(count_set)

                    if rec_ctr == 6:
                        count_six = len(count_set)

                    if rec_ctr == 12:
                        count_twelve = len(count_set)
                        
                    if rec_ctr == 12:
                        break
        
        dataFile.close()

        self.popCounts = Toplevel(self.main_container)
        self.popCounts.title("DATA FILE INFORMATION")
        self.popCounts.maxsize(405, 130)
        self.popCounts.minsize(405, 130)

        self.latestText = Label(self.popCounts, text=" ", style="B.TLabel" )
        self.countTwoText = Label(self.popCounts, text=" ", style="B.TLabel" )
        self.countSixText = Label(self.popCounts, text=" ", style="B.TLabel" )
        self.countTwelveText = Label(self.popCounts, text=" ", style="B.TLabel" )
        
        self.close = Button(self.popCounts, text="CLOSE", style="B.TButton", command=self.popCounts.destroy)
        self.countsSep = Separator(self.popCounts, orient=HORIZONTAL)

        # set the contents of the labels

        combo = []
        
        for i in range(6):
            combo.append("{0:02}".format(latest_winner[i]))

        last_record = " - ".join(combo)

        self.latestText["text"] = "The last winning combination is " + last_record + "."
        self.countTwoText["text"] = "There are {0:1} unique numbers in last two winning combinations.".format(count_two)
        self.countSixText["text"] = "There are {0:1} unique numbers in last six winning combinations.".format(count_six)
        self.countTwelveText["text"] = "There are {0:1} unique numbers in last twelve winning combinations.".format(count_twelve)
        
        self.latestText.grid(row=0, column=0, padx=10, pady=(5,0), sticky='NSEW')
        self.countTwoText.grid(row=1, column=0, padx=10, pady=0, sticky='NSEW')
        self.countSixText.grid(row=2, column=0, padx=10, pady=0, sticky='NSEW')
        self.countTwelveText.grid(row=3, column=0, padx=10, pady=(0,5), sticky='NSEW')
        self.countsSep.grid(row=4, column=0, padx=5, pady=5, sticky='NSEW')
        self.close.grid(row=5, column=0, padx=5, pady=5, sticky='NSEW')

        
    def displayDataFile(self):

        if os.path.exists("config.txt"):
            configFile = open("config.txt", "r")

            filename = configFile.readline()
            self.sourceLabel["text"] = filename

            configFile.close()
        else:
            self.sourceLabel["text"] = "None"


    def saveCombinations(self):

        try:
            gen_len = len(self.num)

            combinations = open("combination.txt", "w")

            for i in range(10):

                combo = []
            
                for j in range(6):
                    combo.append("{0:02}".format(self.num[i][j]))

                record = " - ".join(combo)
                combinations.write(record)
                combinations.write("\n")

            combinations.close()

            sp.Popen(["notepad.exe", "combination.txt"])

        except AttributeError:
            pass
                   

    def deleteCombinations(self):
        
        if os.path.isfile("combination.txt"):

            os.remove("combination.txt")

            self.popDelete = Toplevel(self.main_container)
            self.popDelete.title("COMBINATION FILE DELETED")
            self.popDelete.maxsize(180, 70)
            self.popDelete.minsize(180, 70)

            self.deleteText = Label(self.popDelete, text="Combinations File Deleted", style="B.TLabel" )
            self.close = Button(self.popDelete, text="CLOSE", style="B.TButton", command=self.popDelete.destroy)
            self.hsep = Separator(self.popDelete, orient=HORIZONTAL)

            self.deleteText.grid(row=0, column=0, padx=10, pady=(5,0), sticky='NSEW')
            self.hsep.grid(row=1, column=0, padx=5, pady=5, sticky='NSEW')
            self.close.grid(row=2, column=0, padx=5, pady=5, sticky='NSEW')



root = Tk()
root.title("FIVE FORTY-SEVEN PLUS")
root.minsize(300, 200)

app = Application(root)

root.mainloop()
