#! python3

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

from collections import defaultdict
import datetime
import operator
import random
import copy
import os

import math
from time import time

import itertools
from itertools import combinations

# the next two lines are required to create the classifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class getCombinations(object):

	def __init__(self, selected, ltype, usage):

		self.selectedNumbers = selected

		self.ltype = ltype
		self.othNumbers = []
		self.extNumbers = []
		self.limit = 0
		self.extlimit = 0

		if self.ltype == 1:
			self.limit = 39

		elif self.ltype == 2:
			self.limit = 47
			self.extlimit = 27

		elif self.ltype == 3:
			self.limit = 70
			self.extlimit = 25

		elif self.ltype == 4:
			self.limit = 69
			self.extlimit = 25

		for i in range(self.limit):
			if i+1 in self.selectedNumbers:
				pass
			else:
				self.othNumbers.append(i+1)

		for i in range(self.extlimit):
			self.extNumbers.append(i+1)

		random.shuffle(self.extNumbers)

		self.getCounts(usage)


	def getCounts(self, usage):

		''' This procedure will get the count of possible combinations based on the numbers selected
		'''

		self.numberCount = len(self.selectedNumbers)
		self.divCount = usage / 5
		self.comboCount = math.factorial(self.numberCount) / (math.factorial(self.numberCount - self.divCount) * math.factorial(self.divCount))
		self.duplCount = 25 - self.numberCount

	def randomSelect(self, usage):

		''' This function will generate the combinations using itertools instead of manually going thru
		    the combinations which is done in the old function. The generation will be limited to 100 loops.
		'''

		# initialize the generator
		n_set = self.initIterator(usage)

		selection = []
		numbers_used = []

		loop_count = 0

		# set the starting point of the iterator
		for i in range(random.randint(1, self.comboCount)):
			next(n_set)

		while True:

			try:
				num_list = sorted(next(n_set))

				sim_count = len([num for num in num_list if num in numbers_used])

				if sim_count == 0:

					# check if the generated combination satisfies the criteria
					if self.checkConsecutives(num_list) and self.checkSpread(num_list):

						if usage == 25:
							pass

						elif usage == 20:

							# get one more number from the unselected numbers to complete 5 numbers
							num_list = self.getMore(num_list, selection, 1)
							num_list = sorted(num_list)

						else:
							# get two more number from the unselected numbers to complete 5 numbers
							num_list = self.getMore(num_list, selection, 2)
							num_list = sorted(num_list)

						# select a Super number if the lotto game selected is SuperLotto
						if self.ltype == 2 or self.ltype == 3 or self.ltype == 4:
							num_list.append(self.extNumbers[random.randint(0, self.extlimit - 1)])

						for num in num_list:
							numbers_used.append(num)

						selection.append(num_list)

				if len(selection) == 5:
					break

			except:
				n_set = self.initIterator(usage)

				loop_count += 1

				# if the loop is on the second go-around, get a new starting point
				if loop_count == 2:

					selection = []
					numbers_used = []

					loop_count = 0

					for i in range(random.randint(1, self.comboCount)):
						next(n_set)

		return selection

	def initIterator(self, usage):

		''' This function will be called to initialize the combination generator
		'''

		num_chk = copy.copy(self.selectedNumbers)

		random.shuffle(num_chk)

		if usage == 25:
			n_set = itertools.combinations(num_chk, 5)
		elif usage == 20:
			n_set = itertools.combinations(num_chk, 4)
		else:
			n_set = itertools.combinations(num_chk, 3)

		return n_set

	def checkSpread(self, n_list):

		return True if n_list[4] - n_list[0] > 12 else False

	def checkConsecutives(self, n_list):

		# This function checks if a combination has consecutive numbers. If there are consecutive numbers, return 1

		conctr = 0

		for i in range(len(n_list) - 1):
			if n_list[i] + 1 == n_list[i + 1]:
				conctr += 1

		return True if conctr == 0 else False

	def getMore(self, n_set, selection, count):

		while True:

			n_set_new = copy.copy(n_set)
			o_set_new = copy.copy(self.othNumbers)

			random.shuffle(o_set_new)

			for i in range(count):
				n_set_new.append(o_set_new.pop())

			n_set_new = sorted(n_set_new)

			if self.checkConsecutives(n_set_new) == 0 and self.checkUnique(n_set_new, selection):
				break

		return n_set_new
