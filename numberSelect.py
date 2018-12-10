#! python3

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

import matplotlib.pyplot as plt

import pdb

from collections import defaultdict
import datetime
import operator
import random
import copy
import os

from time import time
import math

import itertools

class numberSelect(object):

	def __init__(self, infile, ltype):

		self.infile = infile
		self.ltype = ltype

		if ltype == 1:
			self.topLimit = 39
		elif ltype == 2:
			self.topLimit = 47
		elif ltype == 3:
			self.topLimit = 70
		elif ltype == 4:
			self.topLimit = 69

		self.selectedNumbers = []
		self.otherNumbers = []
		self.lastWinner = []
		self.allNumbers, self.extNumbers = self.createList(self.topLimit)

		if self.infile == None:
			self.dataHash = {}
			self.lastestDraw = 0
		else:
			self.dataHash, self.latestDraw = self.hashDataFile()
			self.reformatFile()

		self.loadSelectNumbers()

	def hashDataFile(self):

		''' This function will create a hash table for the data file passed. Note this will be common for fantasy and superlotto
		'''
		hashTable = {}
		latest_draw = 0
		with open(self.infile, 'r') as f_data:

			for data in f_data:

				fields = data.split()

				if len(fields) == 0:
					continue

				if fields[0].isdigit():

					# get the draw and store it in the last draw field
					if latest_draw == 0:
						latest_draw = int(fields[0])

					# create the hash key
					hash_key = bytes([int(num) for num in fields[5:10]])

					# store the draw number with the hash key if it is still not in the table. this is needed so that
					# subsequent similar draws will not overwrite the latest draw
					if hash_key in hashTable:
						pass
					else:
						hashTable[hash_key] = int(fields[0])

		return hashTable, latest_draw

	def createList(self,top_limit=39):

		''' This function will create a list of numbers based on the top limit set
		'''

		add_one = lambda x: x + 1

		out_list = []
		ext_list = []

		for i in range(top_limit):

			num = add_one(i)

			if num >= 1:
				out_list.append(add_one(i))

		if top_limit == 47:
			for i in range(27):
				ext_list.append(add_one(i))
		elif top_limit == 70:
			for i in range(25):
				ext_list.append(add_one(i))
		elif top_limit == 69:
			for i in range(26):
				ext_list.append(add_one(i))

		return out_list, ext_list

	def loadSelectNumbers(self):

		''' Get the select numbers if a selection was made. If not, default the list to 1 - 20
		'''

		self.selectedNumbers = []
		self.otherNumbers = []

		if self.ltype == 1:
			data_file = "data\\sf.txt"

		elif self.ltype == 2:
			data_file = "data\\ss.txt"

		elif self.ltype == 3:
			data_file = "data\\sm.txt"

		elif self.ltype == 4:
			data_file = "data\\sp.txt"

		else:
			data_file = "data\\dummy.txt"
			self.selectedNumbers = self.createList(self.topLimit)

		if os.path.exists(data_file):

			with open(data_file, 'r') as selectFile:

				for data in selectFile:

					numb_list = data.split(' - ')

					for numb in numb_list:
						self.selectedNumbers.append(int(numb))

		for i in range(1, self.topLimit + 1):
			if i in self.selectedNumbers:
				pass
			else:
				self.otherNumbers.append(i)

		# Perform analysis on file after loading the randomly selected numbers

	def generateInitial(self, selection):

		''' This function will generate a combination of numbers that is not a previous winner
		'''

		numberSet = []

		limit = math.floor(5 / 2)

		while True:

			# get even numbers
			while (True):

				selected = random.choice(selection)

				if selected in numberSet:
					pass
				else:
					if selected % 2 == 0:
						numberSet.append(selected)

				if len(numberSet) == limit:
					break

			# get odd numbers
			while (True):

				selected = random.choice(selection)

				if selected in numberSet:
					pass
				else:
					if selected % 2 == 1:
						numberSet.append(selected)

				if len(numberSet) == 5:
					break

			numberSet = sorted(numberSet)

			hash_check = bytes([num for num in numberSet])

			if hash_check not in self.dataHash:
				break

		return numberSet

	def addOneAndCheck(self, numberSet, selection):

		''' This function will first create an iterator for the other numbers not selected, and then add them
			one at a time, getting all combinations along the way while checking if there was a match in the last
			30 days.
		'''

		# create an iterator of numbers not yet in inSet
		sel_iter = [num for num in selection if num not in numberSet]

		random.shuffle(sel_iter)
		sel_iter = iter(sel_iter)

		while True:
			# get a number from the selection
			selected = next(sel_iter)

	        # append to inSet
			numberSet.append(selected)

			# check combinations for winners the last several draws
			numberSet = self.getCombinations(numberSet, selected)

			if len(numberSet) == 25:
				break

		return sorted(numberSet)

	def getCombinations(self, numberSet, selected):

		''' This function will generate the combinations to check if any of it occured within the last 100 days.
			If it finds one, then it will pop-out the last number in the list since that's the number that most
			likely caused it
		'''

		iterator = itertools.combinations(numberSet, 5)

		while True:
			try:
				combination = sorted(next(iterator))

				if selected in combination:

					hash_check = bytes([int(num) for num in combination])

					if hash_check in self.dataHash:
						# if there was a match, check if the match is within 40 days from latest draw, if not pop the last number out
						if self.latestDraw - self.dataHash[hash_check] < 40:
							numberSet.pop()
							break

			except:
				break

		return numberSet


	def randomSequentialAdd(self):

		''' This function will create the selection of numbers in a random order
		'''

		self.selectedNumbers = []
		self.otherNumbers = []

		# create an initial set of numbers
		self.selectedNumbers = self.generateInitial(self.allNumbers)

		self.selectedNumbers = self.addOneAndCheck(self.selectedNumbers, self.allNumbers)

		for i in range(1, self.topLimit + 1):
			if i in self.selectedNumbers:
				pass
			else:
				self.otherNumbers.append(i)

		return self.selectedNumbers

	def avoidRecent(self, select_count=20):

		''' FOR DELETION
			This function will avoid recent winning numbers until the remaining numbers matches the count needed
		'''

		self.selectedNumbers = self.allNumbers
		self.otherNumbers = []

		if self.ltype == 1:
			sourceFile = 'data\\cf_data.csv'
		elif self.ltype == 2:
			sourceFile = 'data\\cs_data.csv'

		with open(sourceFile, 'r') as i_file:

			data_count = 0

			for data_line in i_file:

				data_count += 1
				fields = data_line.split(',')

				# remove the new line character at the end of the last field
				fields[-1] = fields[-1][:2]

				numbers = list(map(int, fields[2:]))

				for num in numbers:

					if num in self.selectedNumbers:
						self.selectedNumbers.pop(numbers.index(num))
						self.otherNumbers.append(num)

					# need to check if the count is satisfied after each pop
					if len(self.selectedNumbers) == select_count:
						break

				if len(self.selectedNumbers) == select_count:
					break

		print(data_count)
		return self.selectedNumbers

	def getFromRecent(self, select_count=20):

		''' FOR DELETION
			This function will create a list of numbers from the recent draws
		'''

		self.selectedNumbers = []
		self.otherNumbers = []

		if self.ltype == 1:
			sourceFile = 'data\\cf_data.csv'
		elif self.ltype == 2:
			sourceFile = 'data\\cs_data.csv'

		with open(sourceFile, 'r') as i_file:

			skipped = 0

			for data_line in i_file:

				if skipped < 25:
					skipped += 1
					continue

				fields = data_line.split(',')

				# remove the new line character at the end of the last field
				fields[-1] = fields[-1][:2]

				numbers = list(map(int, fields[2:]))

				for i in range(1):
					# randomly select a number from the data numbers
					remove = np.random.choice(numbers)

					# remove the selected number
					numbers.pop(numbers.index(remove))

				# load the remaining numbers
				self.selectedNumbers = self.loadSelected(self.selectedNumbers, numbers, select_count)

				if len(self.selectedNumbers) == select_count:
					break

		for i in range(1, self.topLimit + 1):
			if i in self.selectedNumbers:
				pass
			else:
				self.otherNumbers.append(i)

		return self.selectedNumbers

	def loadSelected(self, selected, numbers, limit):

		''' This function will load the numbers into the selected list
		'''

		for number in numbers:

			if number in selected:
				pass
			else:

				if len(selected) < limit:
					selected.append(number)
				else:
					break

		return selected


	def setSelectNumbers(self, select_count=20):

		''' FOR DELETION
			This function will select numbers randomly
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

		return self.selectedNumbers

	def writeOutSelected(self):

		if self.ltype == 1:
			selectFile = open("data\\sf.txt", "w")
		elif self.ltype == 2:
			selectFile = open("data\\ss.txt", "w")
		elif self.ltype == 3:
			selectFile = open("data\\sm.txt", "w")
		elif self.ltype == 4:
			selectFile = open("data\\sp.txt", "w")

		sel_num = []

		for i in range(25):
			sel_num.append("{0:02}".format(self.selectedNumbers[i]))

		record = " - ".join(sel_num)

		selectFile.write(record)
		selectFile.write("\n")
		selectFile.close()

	def clearSelectNumbers(self):

		''' This function will select all possible numbers as selected
		'''

		self.selectedNumbers = self.createList(self.topLimit)
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
		else:
			self.reformatSuperMegaPower(self.ltype)

	def reformatFantasy(self):

		rec_ctr = 0

		with open('data\\cf_data.csv', 'w') as myOutput:
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

	def reformatSuperMegaPower(self, ltype):

		''' This function will count the occurences and get the top 25
		'''

		if ltype == 2:
			dfile = 'data\\cs_data.csv'
		elif ltype == 3:
			dfile = 'data\\cm_data.csv'
		else:
			dfile = 'data\\cp_data.csv'

		rec_ctr = 0

		with open(dfile, 'w') as myOutput:
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

		if self.ltype == 1:
			self.analyzeFantasyFile()

		elif self.ltype == 2:
			self.analyzeSuperFile()

		elif self.ltype == 3:
			self.analyzeMegaFile()

		elif self.ltype == 4:
			self.analyzePowerFile()

	def analyzeFantasyFile(self):

		# Load the csv_data file into a dataframe
		fantasy_file = pd.read_csv('data\\cf_data.csv', header=None)
		fantasy_file.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E']

		fantasy_file['MS'] = fantasy_file[['Draw', 'A', 'B', 'C', 'D', 'E']].apply(self.matchSelect, axis=1)

		fantasy_select = copy.copy(fantasy_file[fantasy_file['MS'] == 5])
		fantasy_select.to_csv('data\\cf_select.csv')

		fantasy_select['GAP'] = fantasy_select[['Draw']].apply(self.getGaps, axis=1)
		fantasy_select.to_csv('data\\cf_select.csv')

		self.first_match = fantasy_select['Date'].min()
		self.last_match = fantasy_select['Date'].max()

		last_match_split = self.last_match.split('-')

		date_a = datetime.datetime(int(last_match_split[0]), int(last_match_split[1]), int(last_match_split[2]))
		curr_date  = datetime.datetime.now()

		self.last_match_days = curr_date - date_a
		self.last_match_draws = fantasy_file['Draw'].max() - fantasy_select['Draw'].max()
		self.last_compare = fantasy_file['MS'].iloc[0]

		self.exact_match = fantasy_select['MS'].count()
		self.max_gap = fantasy_select['GAP'].max()
		self.min_gap = fantasy_select[fantasy_select['GAP'] > 0]['GAP'].min()

		# delete the results files
		try:
			os.remove('data\\results.jpg')
		except:
			pass

		plt.figure(figsize=(4,3))
		plt.plot(fantasy_file['MS'][:100])
		plt.savefig('data\\results.jpg')

		#return self.last_match, self.first_match, self.last_match_days.days, self.max_gap, self.min_gap, self.exact_match

	def analyzeSuperFile(self):

		# Load the csv_data file into a dataframe
		superlotto_file = pd.read_csv('data\\cs_data.csv', header=None)
		superlotto_file.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E', 'S']

		superlotto_file['MS'] = superlotto_file[['Draw', 'A', 'B', 'C', 'D', 'E']].apply(self.matchSelect, axis=1)

		superlotto_select = copy.copy(superlotto_file[superlotto_file['MS'] == 5])
		superlotto_select.to_csv('data\\cs_select.csv')

		superlotto_select['GAP'] = superlotto_select[['Draw']].apply(self.getGaps, axis=1)
		superlotto_select.to_csv('data\\cs_select.csv')

		self.first_match = superlotto_select['Date'].min()
		self.last_match = superlotto_select['Date'].max()
		last_match_split = self.last_match.split('-')

		date_a = datetime.datetime(int(last_match_split[0]), int(last_match_split[1]), int(last_match_split[2]))
		curr_date  = datetime.datetime.now()

		self.last_match_days = curr_date - date_a
		self.last_match_draws = superlotto_file['Draw'].max() - superlotto_select['Draw'].max()
		self.last_compare = superlotto_file['MS'].iloc[0]

		self.exact_match = superlotto_select['MS'].count()
		self.max_gap = superlotto_select['GAP'].max()
		self.min_gap = superlotto_select[superlotto_select['GAP'] > 0]['GAP'].min()

		# delete the results files
		try:
			os.remove('data\\results.jpg')
		except:
			pass

		plt.figure(figsize=(4,3))
		plt.plot(superlotto_file['MS'][:100])
		plt.savefig('data\\results.jpg')

	def analyzeMegaFile(self):

		# Load the csv_data file into a dataframe
		megalotto_file = pd.read_csv('data\\cm_data.csv', header=None)
		megalotto_file.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E', 'M']

		megalotto_file['MS'] = megalotto_file[['Draw', 'A', 'B', 'C', 'D', 'E']].apply(self.matchSelect, axis=1)

		megalotto_select = copy.copy(megalotto_file[megalotto_file['MS'] == 5])
		megalotto_select.to_csv('data\\cm_select.csv')

		megalotto_select['GAP'] = megalotto_select[['Draw']].apply(self.getGaps, axis=1)
		megalotto_select.to_csv('data\\cm_select.csv')

		self.first_match = megalotto_select['Date'].min()
		self.last_match = megalotto_select['Date'].max()
		last_match_split = self.last_match.split('-')

		date_a = datetime.datetime(int(last_match_split[0]), int(last_match_split[1]), int(last_match_split[2]))
		curr_date  = datetime.datetime.now()

		self.last_match_days = curr_date - date_a
		self.last_match_draws = megalotto_file['Draw'].max() - megalotto_select['Draw'].max()
		self.last_compare = megalotto_file['MS'].iloc[0]

		self.exact_match = megalotto_select['MS'].count()
		self.max_gap = megalotto_select['GAP'].max()
		self.min_gap = megalotto_select[megalotto_select['GAP'] > 0]['GAP'].min()

		# delete the results files
		try:
			os.remove('data\\results.jpg')
		except:
			pass

		plt.figure(figsize=(4,3))
		plt.plot(megalotto_file['MS'][:100])
		plt.savefig('data\\results.jpg')


	def analyzePowerFile(self):

		# Load the csv_data file into a dataframe
		powerball_file = pd.read_csv('data\\cm_data.csv', header=None)
		powerball_file.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E', 'M']

		powerball_file['MS'] = powerball_file[['Draw', 'A', 'B', 'C', 'D', 'E']].apply(self.matchSelect, axis=1)

		powerball_select = copy.copy(powerball_file[powerball_file['MS'] == 5])
		powerball_select.to_csv('data\\cp_select.csv')

		powerball_select['GAP'] = powerball_select[['Draw']].apply(self.getGaps, axis=1)
		powerball_select.to_csv('data\\cp_select.csv')

		self.first_match = powerball_select['Date'].min()
		self.last_match = powerball_select['Date'].max()
		last_match_split = self.last_match.split('-')

		date_a = datetime.datetime(int(last_match_split[0]), int(last_match_split[1]), int(last_match_split[2]))
		curr_date  = datetime.datetime.now()

		self.last_match_days = curr_date - date_a
		self.last_match_draws = powerball_file['Draw'].max() - powerball_select['Draw'].max()
		self.last_compare = powerball_file['MS'].iloc[0]

		self.exact_match = powerball_select['MS'].count()
		self.max_gap = powerball_select['GAP'].max()
		self.min_gap = powerball_select[powerball_select['GAP'] > 0]['GAP'].min()

		# delete the results files
		try:
			os.remove('data\\results.jpg')
		except:
			pass

		plt.figure(figsize=(4,3))
		plt.plot(powerball_file['MS'][:100])
		plt.savefig('data\\results.jpg')

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

		if self.ltype == 1:
			csv_file = 'data\\cf_select.csv'
		elif self.ltype == 2:
			csv_file = 'data\\cs_select.csv'
		elif self.ltype == 3:
			csv_file = 'data\\cm_select.csv'
		elif self.ltype == 4:
			csv_file = 'data\\cp_select.csv'

		date_diff = datetime.timedelta(0)
		draw_diff = 0

		with open(csv_file, 'r') as inFile:

			for dataLine in inFile:
				fields = dataLine.split(',')

				if len(fields) > 0:

					if fields[0].isdigit():

						if int(draw) == int(fields[1]):

							draw_date = fields[2].split('-')

							date_a = datetime.datetime(int(draw_date[0]), int(draw_date[1]), int(draw_date[2]))
							draw_a = int(fields[1])

						if int(draw) > int(fields[1]):

							draw_date = fields[2].split('-')

							date_b = datetime.datetime(int(draw_date[0]), int(draw_date[1]), int(draw_date[2]))
							draw_b = int(fields[1])

							draw_diff = draw_a - draw_b
							date_diff = date_a - date_b

							break

		# close the file so that the outside process can read it
		inFile.close()

		#return date_diff.days
		return draw_diff

	def getSelectNumbers(self):

		''' Get the top numbers as of the last draw
		'''

		return self.selectedNumbers

	def compareSaveSelect(self):

		''' This function will compare the selected numbers currently in storage to the selected numbers saved.
			If it is a match, then return False
		'''

		self.savedNumbers = []

		if self.ltype == 1:
			select_file = "data\\sf.txt"
		elif self.ltype == 2:
			select_file = "data\\ss.txt"
		elif self.ltype == 3:
			select_file = "data\\sm.txt"
		elif self.ltype == 4:
			select_file = "data\\sp.txt"

		with open(select_file, 'r') as selectFile:

			for data in selectFile:

				numb_list = data.split(' - ')

		for numb in numb_list:
			self.savedNumbers.append(int(numb))

		return self.savedNumbers == self.selectedNumbers

	def getStats(self):

		return self.last_match, self.last_compare, self.first_match, self.last_match_draws, self.max_gap, self.min_gap, self.exact_match
