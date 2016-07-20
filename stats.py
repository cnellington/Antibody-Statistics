import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Stats:

	clusters = 0
	lengths = 0
	nvalues = []

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

		#Making file data useful (sorting)
		newlist = []
		for x in numlist:
			newlist += [x]*x

		newlist.sort(reverse = True)
		i = float(n)/100.0
		medianpos = int(float(len(newlist)) * i)
		if i == 1:
			medianpos -= 1
		return newlist[medianpos]

	def N50(self):
		return self.NValue(50.0)

	def N90(self):
		return self.NValue(90.0)

	#Returns Little n50 cluster analysis
	#The smallest value above the N50 threshold
	def nNValue(self, x):
		n = self.NValue(x)
		return [n, self.lengths[self.lengths>=n].count()]

	def nN50(self):
		n = self.N50()
		return [self.lengths[self.lengths>=n].count(), n]

	def nN90(self):
		n = self.N90()
		return [self.lengths[self.lengths>=n].count(), n]

	def NPlot(self):
		xaxis = np.arange(0,101).tolist()
		nvalues = []
		for x in xaxis:
			nvalues.append(self.NValue(x))
		plt.plot(xaxis, nvalues)
		plt.axis([-5, xaxis[len(xaxis)-1]+5, -5, nvalues[0]+50 ])
		plt.show()
		print "plot has been produced"

	#Returns the percent above the N50 threshold showing
	#data accuracy
	def NValuePercent(self, n):

		#Get n50 and total clusters
		littleN = self.nNValue(n)[0]
		total = self.totalClusters()

		#return percentage
		return float(littleN)/float(total)*100