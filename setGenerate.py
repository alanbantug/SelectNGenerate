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

	def __init__(self, selected, ltype):

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

		for i in range(self.limit):
			if i+1 in self.selectedNumbers:
				pass
			else:
				self.othNumbers.append(i+1)

		for i in range(self.extlimit):
			self.extNumbers.append(i+1)

		random.shuffle(self.extNumbers)

		self.getCounts()


	def getCounts(self):

		''' This procedure will get the count of possible combinations based on the numbers selected
		'''

		self.numberCount = len(self.selectedNumbers)
		self.divCount = self.numberCount / 5
		self.comboCount = math.factorial(self.numberCount) / (math.factorial(self.numberCount - self.divCount) * math.factorial(self.divCount))
		self.duplCount = 25 - self.numberCount

	def randomSelect(self):

		selection = []

		loop_count = 0
		comb_count = 0

		n_set = self.initIterator()

		while True:
        
			try:
				num_list = sorted(next(n_set))
				
				if self.checkQualified(num_list, selection):

					if self.divCount == 5:
						pass

					elif self.divCount == 4:
						num_list = self.getMore(num_list, 1)
						num_list = sorted(num_list)

					else:
						num_list = self.getMore(num_list, 2)
						num_list = sorted(num_list)

					if self.ltype == 2:
						num_list.append(self.extNumbers[random.randint(0, self.extlimit - 1)])

					selection.append(num_list)
					comb_count += 1

				if comb_count == 5:
					break
                
			except:
				loop_count += 1

				if loop_count < 100:

					n_set = self.initIterator()
					selection = []
					comb_count = 0

				else:
					print(loop_count)
					break

		return selection

	def initIterator(self):

		num_chk = copy.copy(self.selectedNumbers)
		random.shuffle(num_chk)
					
		if self.divCount == 5:
			n_set = itertools.combinations(num_chk, 5)
		elif self.divCount == 4:
			n_set = itertools.combinations(num_chk, 4)
		else:
			n_set = itertools.combinations(num_chk, 3)
                
		for i in range(random.randint(1, self.comboCount)):
			next(n_set)

		return n_set

	def randomSelection(self):

		''' This function will: 
		    1. Randomly select a combination  
		    2. Get the next combination from the qualified combinations making sure that the numbers in the combination have not been used yet
		'''

		selection = []
		
		num_chk = copy.copy(self.selectedNumbers)
		random.shuffle(num_chk)

		while (True):

			start_id = random.randint(1, self.comboCount)
			
			if self.divCount == 5:
				selection = self.generateFive(start_id)
			elif self.divCount == 4:
				selection = self.generateFour(start_id)
			elif self.divCount == 3:
				selection = self.generateThree(start_id)

			if len(selection) == 5:
				break

		return selection


	def generateFive(self, start_id):

		''' This function will generate all possible combinations of the selected numbers and tag whether they contain
			consecutives and what the pattern is. This will make combination selection faster, instead of generating
			a combination and then finding out it is not qualified.
		'''

		num_src = copy.copy(self.selectedNumbers)

		selection = []
		sel_ctr = 0
		idx = 0

		id_a = 0
		while (id_a < self.numberCount - 4):
			id_b = id_a + 1

			while (id_b < self.numberCount - 3):
				id_c = id_b + 1

				while (id_c < self.numberCount - 2):
					id_d = id_c + 1

					while (id_d < self.numberCount - 1):
						id_e = id_d + 1

						while (id_e < self.numberCount):

							idx += 1

							if idx == start_id:

								if sel_ctr < 5:

									n_set = sorted([num_src[id_a], num_src[id_b], num_src[id_c], num_src[id_d], num_src[id_e]])

									if self.checkQualified(n_set, selection):

										if self.ltype == 2:
											n_set.append(self.extNumbers[random.randint(0, self.extlimit - 1)])

										selection.append(n_set)
										sel_ctr += 1

								start_id += random.randint(1, 100)

							id_e += 1
					
						id_d += 1
					
					id_c += 1
					
				id_b += 1

			id_a += 1

		return selection

	def generateFour(self, start_id):

		''' This function will generate all possible combinations of the selected numbers and tag whether they contain
			consecutives and what the pattern is. This will make combination selection faster, instead of generating
			a combination and then finding out it is not qualified.
		'''

		num_src = copy.copy(self.selectedNumbers)

		selection = []
		sel_ctr = 0
		idx = 0

		id_a = 0
		while (id_a < self.numberCount - 3):
			id_b = id_a + 1

			while (id_b < self.numberCount - 2):
				id_c = id_b + 1

				while (id_c < self.numberCount - 1):
					id_d = id_c + 1

					while (id_d < self.numberCount):

						idx += 1

						if idx == start_id:

							if sel_ctr < 5:

								n_set = sorted([num_src[id_a], num_src[id_b], num_src[id_c], num_src[id_d]])

								if self.checkQualified(n_set, selection):

									n_set = self.getMore(n_set, 1)
									n_set = sorted(n_set)

									if self.ltype == 2:
										n_set.append(self.extNumbers[random.randint(0, self.extlimit - 1)])

									selection.append(n_set)
									sel_ctr += 1

							start_id += random.randint(1, 100)

						id_d += 1
					
					id_c += 1
					
				id_b += 1

			id_a += 1

		return selection

	def generateThree(self, start_id):

		''' This function will generate all possible combinations of the selected numbers and tag whether they contain
			consecutives and what the pattern is. This will make combination selection faster, instead of generating
			a combination and then finding out it is not qualified.
		'''

		num_src = copy.copy(self.selectedNumbers)

		selection = []
		sel_ctr = 0
		idx = 0

		id_a = 0
		while (id_a < self.numberCount - 2):
			id_b = id_a + 1

			while (id_b < self.numberCount - 1):
				id_c = id_b + 1

				while (id_c < self.numberCount):

					idx += 1

					if idx == start_id:

						if sel_ctr < 5:

							n_set = sorted([num_src[id_a], num_src[id_b], num_src[id_c]])

							if self.checkQualified(n_set, selection):

								# Get two more numbers
								n_set = self.getMore(n_set, 2)
								n_set = sorted(n_set)								

								if self.ltype == 2:
									n_set.append(self.extNumbers[random.randint(0, self.extlimit - 1)])

								selection.append(n_set)
								sel_ctr += 1

							start_id += random.randint(1, 100)

					id_c += 1
					
				id_b += 1

			id_a += 1

		return selection

	def checkQualified(self, n_set, selection):

		qual = True

		# Allow only one pair of consecutive numbers
		if self.checkConsecutives(n_set) == 0:
			pass
		else:
			qual = False

		# Make sure that numbers are not repeated
		if self.checkUnique(n_set, selection):
			pass
		else:
			qual = False

		return qual

	def checkConsecutives(self, data):
    
		# This function checks if a combination has consecutive numbers. If there are consecutive numbers, return 1
    	
		conctr = 0

		for i in range(len(data) - 1):
			if data[i] + 1 == data[i + 1]:
				conctr += 1

		return conctr

	def checkUnique(self, n_set, selection):

		# This function checks the numbers in the generated combinations exist is the selected combinations

		unique = True

		for n in n_set:
			for sel in selection:
				if n in sel:
					unique = False
					
		return unique

	def getMore(self, n_set, count):

		for i in range(count):
			n_set.append(random.choice(self.othNumbers))

		return n_set

