import sys
import pandas as pd
import numpy as np

class Stats:

	clusters = 0
	lengths = 0

	def __init__(self, filename):
		df = pd.read_csv(filename, sep='\t')
		self.clusters = self.lengths = df.Clustered
		#self.clusters = self.lengths = pd.Series(np.arange(1,11,1))


	#Total clusters from PandaSeq output
	def totalClusters(self):
		return self.clusters.count()


	#Returns Big N50 cluster analysis
	#The number of clusters constituting the top 50 percent
	#of the total mass of clusters
	#Variable N value analysis
	def NValue(self, n):

		numlist = self.lengths.tolist()
		#numlist = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

		#Making file data useful (sorting)
		newlist = []
		for x in numlist:
			newlist += [x]*x

		newlist.sort(reverse = True)
		i = float(n)/100.0
		medianpos = int(float(len(newlist)) * i)
		return newlist[medianpos]

	def N50(self):
		return self.NValue(50.0)

	def N90(self):
		return self.NValue(90.0)

	#Returns Little n50 cluster analysis
	#The smallest value above the N50 threshold
	def nNValue(self, n):
		n = self.NValue(n)
		return [self.lengths[self.lengths>=n].count(), n]

	def nN50(self):
		n = self.N50()
		return [self.lengths[self.lengths>=n].count(), n]

	def nN90(self):
		n = self.N90()
		return [self.lengths[self.lengths>=n].count(), n]

	#Returns the percent above the N50 threshold showing
	#data accuracy
	def NValuePercent(self, n):

		#Get n50 and total clusters
		littleN = self.nNValue(n)[0]
		total = self.totalClusters()

		#return percentage
		return float(littleN)/float(total)*100