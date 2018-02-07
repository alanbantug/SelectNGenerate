#! python

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

from collections import defaultdict
import datetime	
import operator
import random
import copy
import os

from time import time
import math

class numberSelect(object):

	def __init__(self, infile, ltype):

		self.infile = infile
		self.ltype = ltype

		if ltype == 1:
			self.topLimit = 39
		else:
			self.topLimit = 47

		self.selectedNumbers = []
		self.otherNumbers = []
		self.lastWinner = []
		self.allNumbers, self.extNumbers = self.createList(1, self.topLimit)

		self.reformatFile()
		self.loadSelectNumbers()
		

	def createList(self,start,top_limit=39):

		''' This function will create a list of numbers based on the top limit set
		'''

		add_one = lambda x: x + 1

		out_list = []
		ext_list = []

		for i in range(top_limit):

			num = add_one(i)

			if num >= start:
				out_list.append(add_one(i))

		if top_limit == 47:
			for i in range(27):
				ext_list.append(add_one(i))

		return out_list, ext_list


	def loadSelectNumbers(self):

		''' Get the select numbers if a selection was made. If not, default the list to 1 - 20
		'''
		
		self.selectedNumbers = []
		self.otherNumbers = []

		if self.ltype == 1:

			if os.path.exists("sf.txt"):

				with open('sf.txt', 'r') as selectFile:

					for data in selectFile:

						numb_list = data.split(' - ')

				for numb in numb_list:
					self.selectedNumbers.append(int(numb))

		elif self.ltype == 2:
			
			if os.path.exists("ss.txt"):

				with open('ss.txt', 'r') as selectFile:

					for data in selectFile:

						numb_list = data.split(' - ')

				for numb in numb_list:
					self.selectedNumbers.append(int(numb))

		else:

			self.selectedNumbers = self.createList(1, self.topLimit)


		for i in range(1, self.topLimit + 1):
			if i in self.selectedNumbers:
				pass
			else:
				self.otherNumbers.append(i)

		# Perform analysis on file after loading the randomly selected numbers


	def setSelectNumbers(self, select_count=20):

		''' This function will select numbers randomly
		'''

		self.selectedNumbers = []
		self.otherNumbers = []

		limit = math.floor(select_count / 2)

		# get even numbers  
		while (True):

			selected = random.choice(self.allNumbers)

			if selected in self.selectedNumbers:
				pass
			else:
				if selected % 2 == 0:
					self.selectedNumbers.append(selected)

			if len(self.selectedNumbers) == limit:
				break

		# get odd numbers
		while (True):

			selected = random.choice(self.allNumbers)

			if selected in self.selectedNumbers:
				pass
			else:
				if selected % 2 == 1:
					self.selectedNumbers.append(selected)

			if len(self.selectedNumbers) == select_count:
				break

		for i in range(1, self.topLimit + 1):
			if i in self.selectedNumbers:
				pass
			else:
				self.otherNumbers.append(i)

		if self.ltype == 1:
			selectFile = open("sf.txt", "w")
		elif self.ltype == 2:
			selectFile = open("ss.txt", "w")

		sel_num = []

		for i in range(select_count):

			sel_num.append("{0:02}".format(self.selectedNumbers[i]))

		record = " - ".join(sel_num)

		selectFile.write(record)
		selectFile.write("\n")

		selectFile.close()

		return self.selectedNumbers


	def clearSelectNumbers(self):

		''' This function will select all possible numbers as selected
		'''

		self.selectedNumbers = self.createList(1, self.topLimit)
		self.otherNumbers = []

		if self.ltype == 1:
			if os.path.exists("sf.txt"):
				os.remove("sf.txt")
		elif self.ltype == 2:
			if os.path.exists("ss.txt"):
				os.remove("ss.txt")

		return self.selectedNumbers


	def reformatFile(self):

		''' This function will create the CSV file to build the dataframe
		'''

		if self.ltype == 1:
			self.reformatFantasy()
		elif self.ltype == 2:
			self.reformatSuper()

	def reformatFantasy(self):

		rec_ctr = 0

		with open('cf_data.csv', 'w') as myOutput:
			with open(self.infile, 'r') as myInput:

				for dataLine in myInput:
			
					fields = dataLine.split()
				
					if len(fields) > 0:
					
						if fields[0].isdigit():

							# build the data to write to csv_data
							data = []

							in_date = fields[2] + ' ' + fields[3] + ' ' + fields[4]
							draw_date = datetime.datetime.strptime(in_date, '%b %d, %Y').date()

							data.append(fields[0])
							data.append(str(draw_date))

							for n in fields[5:10]:
								data.append(n)

							winner = ",".join(data)
							myOutput.write(winner)
							myOutput.write("\n")

							rec_ctr += 1

		myInput.close()
		myOutput.close()

	def reformatSuper(self):

		''' This function will count the occurences and get the top 25
		'''

		rec_ctr = 0

		with open('cs_data.csv', 'w') as myOutput:
			with open(self.infile, 'r') as myInput:

				for dataLine in myInput:
			
					fields = dataLine.split()
				
					if len(fields) > 0:
					
						if fields[0].isdigit():

							# build the data to write to csv_data
							data = []

							in_date = fields[2] + ' ' + fields[3] + ' ' + fields[4]
							draw_date = datetime.datetime.strptime(in_date, '%b %d, %Y').date()

							data.append(fields[0])
							data.append(str(draw_date))

							for n in fields[5:10]:
								data.append(n)

							data.append(fields[10])

							winner = ",".join(data)
							myOutput.write(winner)
							myOutput.write("\n")

		myInput.close()
		myOutput.close()


	def analyzeData(self):

		''' This function will do several things:

			1. Read the CSV file into a DataFrame
			2. Get the top 20 numbers at the time before the draws and then compares them with the winning draws
			3. Get the date of when the numbers from the last draw came from the top 20, the count of such incidents, and the shortest 
			   and longest dates in between the occurences
		'''

		# Load the csv_data file into a dataframe
		fantasy_file = pd.read_csv('csv_data.csv', header=None)
		fantasy_file.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E']

		fantasy_file['MS'] = fantasy_file[['Draw', 'A', 'B', 'C', 'D', 'E']].apply(self.matchSelect, axis=1)
		
		fantasy_select = copy.copy(fantasy_file[fantasy_file['MS'] == 5])
		fantasy_select.to_csv('select.csv')

		fantasy_select['GAP'] = fantasy_select[['Draw']].apply(self.getGaps, axis=1)
		fantasy_select.to_csv('select.csv')

		self.first_match = fantasy_select['Date'].min()
		self.last_match = fantasy_select['Date'].max()
		last_match_split = self.last_match.split('-')

		date_a = datetime.datetime(int(last_match_split[0]), int(last_match_split[1]), int(last_match_split[2]))
		curr_date  = datetime.datetime.now()

		self.last_match_days = curr_date - date_a

		self.exact_match = fantasy_select['MS'].count()
		self.max_gap = fantasy_select['GAP'].max()
		self.min_gap = fantasy_select[fantasy_select['GAP'] > 0]['GAP'].min()

		return self.last_match, self.first_match, self.last_match_days.days, self.max_gap, self.min_gap, self.exact_match
		
	def matchSelect(self, data):

		draw, numa, numb, numc, numd, nume = data

		draw_set = [numa, numb, numc, numd, nume]

		match_count = 0

		for n in draw_set:
			match_count += self.selectedNumbers.count(int(n))

		return match_count


	def getGaps(self, draw):

		''' This function will get the gaps between the 
		'''

		date_diff = datetime.timedelta(0)

		with open('select.csv', 'r') as inFile:

			for dataLine in inFile:
				fields = dataLine.split(',')

				if len(fields) > 0:

					if fields[0].isdigit():

						if int(draw) == int(fields[1]):

							draw_date = fields[2].split('-')

							date_a = datetime.datetime(int(draw_date[0]), int(draw_date[1]), int(draw_date[2]))

						if int(draw) > int(fields[1]):

							draw_date = fields[2].split('-')

							date_b = datetime.datetime(int(draw_date[0]), int(draw_date[1]), int(draw_date[2]))

							date_diff = date_a - date_b

							break

		# close the file so that the outside process can read it
		inFile.close()

		return date_diff.days

	def getSelectNumbers(self):

		''' Get the top numbers as of the last draw
		'''

		return self.selectedNumbers


	def getStats(self):

		return self.last_match, self.first_match, self.last_match_days.days, self.max_gap, self.min_gap, self.exact_match

