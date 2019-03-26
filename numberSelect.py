#! python3

#import numpy as np
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

	def __init__(self, config, infile, ltype):

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

		self.loadSelectNumbers(config)

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

	def loadSelectNumbers(self, config):

		''' Get the select numbers if a selection was made. If not, default the list to 1 - 20
		'''

		self.selectedNumbers = config.getSelect(self.ltype)
		self.otherNumbers = []

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
			try:
				selected = next(sel_iter)
			except:
				sel_iter = [num for num in selection if num not in numberSet]

				random.shuffle(sel_iter)

				sel_iter = iter(sel_iter)

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
						if self.latestDraw - self.dataHash[hash_check] < 60:
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

	def writeOutSelected(self, config):

		config.updateSelect(self.ltype, self.selectedNumbers)

	def writeGenerated(self, config, selection):

		config.updateLastSet(self.ltype, selection)

	def clearSelectNumbers(self, config):

		''' This function will select all possible numbers as selected
		'''

		config.updateSelect(self.ltype, [])

		self.selectedNumbers = []
		self.otherNumbers = []

		#self.selectedNumbers, self.otherNumbers = self.createList(self.topLimit)

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
		gap_list = fantasy_select[['Draw']].apply(self.getGapList, axis=0)

		fantasy_select = fantasy_select.set_index(pd.Index([n for n in range(len(fantasy_select))]))
		gap_list = gap_list.set_index(pd.Index([n for n in range(len(gap_list))]))

		fantasy_select = pd.concat([fantasy_select, gap_list], axis=1)
		fantasy_select.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E', 'MS', 'GAP']

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

	def analyzeSuperFile(self):

		# Load the csv_data file into a dataframe
		superlotto_file = pd.read_csv('data\\cs_data.csv', header=None)
		superlotto_file.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E', 'S']

		superlotto_file['MS'] = superlotto_file[['Draw', 'A', 'B', 'C', 'D', 'E']].apply(self.matchSelect, axis=1)

		superlotto_select = copy.copy(superlotto_file[superlotto_file['MS'] == 5])
		gap_list = superlotto_select[['Draw']].apply(self.getGapList, axis=0)

		superlotto_select = superlotto_select.set_index(pd.Index([n for n in range(len(superlotto_select))]))
		gap_list = gap_list.set_index(pd.Index([n for n in range(len(gap_list))]))

		superlotto_select = pd.concat([superlotto_select, gap_list], axis=1)
		superlotto_select.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E', 'S', 'MS', 'GAP']

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
		gap_list = megalotto_select[['Draw']].apply(self.getGapList, axis=0)

		megalotto_select = megalotto_select.set_index(pd.Index([n for n in range(len(megalotto_select))]))
		gap_list = gap_list.set_index(pd.Index([n for n in range(len(gap_list))]))

		megalotto_select = pd.concat([megalotto_select, gap_list], axis=1)
		megalotto_select.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E', 'M', 'MS', 'GAP']

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
		gap_list = powerball_select[['Draw']].apply(self.getGapList, axis=0)

		powerball_select = powerball_select.set_index(pd.Index([n for n in range(len(powerball_select))]))
		gap_list = gap_list.set_index(pd.Index([n for n in range(len(gap_list))]))

		powerball_select = pd.concat([powerball_select, gap_list], axis=1)
		powerball_select.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E', 'M', 'MS', 'GAP']

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

	def getGapList(self, draw):

		gap_list = []

		for idx in range(len(draw) - 1):

			diff = draw.iloc[idx] - draw.iloc[idx + 1]
			gap_list.append(diff)

		# add one more to account for the gap for the last row, whcih would be zero since nothing comes after
		gap_list.append(0)

		return gap_list



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

	def compareSaveSelect(self, config):

		''' This function will compare the selected numbers currently in storage to the selected numbers saved.
			If it is a match, then return False
		'''

		self.savedNumbers = config.getSelect(self.ltype)

		return self.savedNumbers == self.selectedNumbers

	def getStats(self):

		return self.last_match, self.last_compare, self.first_match, self.last_match_draws, self.max_gap, self.min_gap, self.exact_match
