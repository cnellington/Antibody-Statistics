import sys
import pandas

class Stats:

	clusters = 0
	lengths = 0

	def __init__(self, filename):
		df = pandas.read_csv(filename, sep='\t')
		self.clusters = self.lengths = df.Clustered


	#Total clusters from PandaSeq output
	def totalClusters(self):
		return self.clusters.count()


	#Returns Big N50 cluster analysis
	#The number of clusters constituting the top 50 percent
	#of the total mass of clusters
	def N50(self):

		numlist = self.lengths.tolist()

		#Making file data useful (sorting)
		numlist.sort()
		newlist = []
		for x in numlist:
			newlist += [x]*x

		#returning N50 value
		if len(newlist) % 2 == 0:
			medianpos = len(newlist)/2
			return float(newlist[medianpos] + newlist[medianpos-1]) / 2
		else:
			medianpos = len(newlist)/2
			return newlist[medianpos]


	#Returns Little n50 cluster analysis
	#The smallest value above the N50 threshold
	def n50(self):

		n = self.N50()

		#return n50 value
		return self.lengths[self.lengths>n].count()


	#Returns the percent above the N50 threshold showing
	#data accuracy
	def percent(self):

		#Get n50 and total clusters
		littleN50 = self.n50()
		total = self.totalClusters()

		#return percentage
		return float(littleN50)/float(total)*100