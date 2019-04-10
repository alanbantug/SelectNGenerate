#! python3

#import numpy as np
import pandas as pd
from pandas import Series, DataFrame

from collections import defaultdict
import datetime
import operator
import random
import copy
import os

from tkinter import messagebox

import math
from time import time

import itertools
from itertools import combinations

# the next two lines are required to create the classifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split


class getCombinations(object):

	def __init__(self, indicator, ltype):

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
			self.extlimit = 26

		if indicator == 1:
			self.selectedNumbers = [n for n in range(1,self.limit + 1) if n % 2 != 0]
		else:
			self.selectedNumbers = [n for n in range(1,self.limit + 1) if n % 2 == 0]

		for i in range(self.extlimit):
			self.extNumbers.append(i+1)

		random.shuffle(self.extNumbers)

		self.getCounts()


	def getCounts(self):

		''' This procedure will get the count of possible combinations based on the numbers selected
		'''

		self.numberCount = len(self.selectedNumbers)
		self.divCount = 5
		self.comboCount = math.factorial(self.numberCount) / (math.factorial(self.numberCount - self.divCount) * math.factorial(self.divCount))
		self.duplCount = 25 - self.numberCount

	def randomSelect(self):

		''' This function will generate the combinations using itertools instead of manually going thru
		    the combinations which is done in the old function. The generation will be limited to 100 loops.
		'''

		selection = []

		loop_count = 0
		comb_count = 0

		# initialize the generator
		n_set = self.initIterator()

		while True:

			try:
				num_list = sorted(next(n_set))

				# check if the generated combination satisfies the criteria

				if self.checkQualified(num_list, selection):

					selection.append(num_list)
					comb_count += 1

				if comb_count == 5:
					break

			except:
				loop_count += 1

				# limit the count to 100 loops
				if loop_count < 5:
					n_set = self.initIterator()
					selection = []
					comb_count = 0

				else:
					break

		unused = []

		for n in self.selectedNumbers:
			n_count = 0

			for sel in selection:
				n_count += sel.count(n)

			if n_count == 0:
				unused.append(n)

		if self.ltype != 1:

			for sel in selection:
				sel.append(self.extNumbers[random.randint(0, self.extlimit - 1)])

		return selection, len(unused)

	def initIterator(self):

		''' This function will be called to initialize the combination generator
		'''

		num_chk = copy.copy(self.selectedNumbers)

		random.shuffle(num_chk)

		n_set = itertools.combinations(num_chk, 5)

		for i in range(random.randint(1, self.comboCount)):
			next(n_set)

		return n_set

	def checkQualified(self, n_list, selection):

		''' This function will check for criteria. Note that since we are generating all odd or all even combinations,
		    there is no need to check for consecutives
		'''

		qual = True

		# Make sure that numbers are not repeated
		if self.checkUnique(n_list, selection):
			pass
		else:
			qual = False

		return qual

	def checkUnique(self, n_list, selection):

		# This function checks the numbers in the generated combinations exist is the selected combinations

		unique = True

		# if there are less than 3 or 4 sets in the selection and the generation is Fantasy or Super, respectively,
		# set the limit to 0, else set to 1. this will ensure that the first three combinations have unique numbers
		limit = 0
		if self.ltype == 1:
			if len(selection) > 2:
				limit = 1
		elif self.ltype == 2:
			if len(selection) > 3:
				limit = 1

		for n in n_list:
			n_count = 0
			for sel in selection:
				n_count += sel.count(n)

			if n_count > limit:
				unique = False

		return unique
