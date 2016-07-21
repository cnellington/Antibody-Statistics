import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Stats:

	clusters = None #arange object
	lengths = None #list object
	nvalues = [] #stored Nvalues 0-100 to cut down on Nvalue usage/runtime (values added with NPlot() or getAllNValues())
	allvalues = False #has getAllNValues been run

	def __init__(self, filename):
		df = pd.read_csv(filename, sep='\t')
		self.clusters = self.lengths = df.Clustered
		#self.clusters = self.lengths = pd.Series(np.arange(1,11,1)) #Test arange for NValues
		self.lengths.tolist().sort(reverse = True)
		

	#Total clusters from PandaSeq output
	def totalClusters(self):
		return self.clusters.count()


	#Returns Big N50 cluster analysis
	#The number of clusters constituting the top 50 percent
	#of the total mass of clusters
	#Variable N value analysis
	def NValue(self, n):

		#find a new NValue
		if(not self.allvalues):
			numlist = self.lengths.tolist() #New list object transfer (idk if python messes with pointers, just to be safe)

			#Making file data useful (sorting)
			newlist = []
			for x in numlist:
				newlist += [x]*x

			#newlist.sort(reverse = True) #Uncomment if clusters = lengths
			i = float(n)/100.0
			medianpos = int(float(len(newlist)) * i)
			if i == 1:
				medianpos -= 1
			return newlist[medianpos]

		#use existing NValue
		else:
			return self.nvalues[int(n)]


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
		if(not self.allvalues):
			self.getAllNValues()
		xaxis = range(1,101)

		buff = .05 #determines how close the plot is to the axes
		xbuffer = int(xaxis[len(xaxis)-1]*buff) #x-axis buffer for clarity
		ybuffer = int(self.nvalues[0]*buff) #y-axis buffer for clarity
		
		plt.ylabel("Cluster Size")
		plt.xlabel("N value (smallest cluster above n percent mass)")
		plt.plot(xaxis, self.nvalues[1:])
		plt.axis([0-xbuffer, 100+xbuffer, 0-ybuffer, self.nvalues[0]+ybuffer ]) #plot axes, buffers added to both limits
		
		print("\nplotting graph...\n")
		plt.show()

		#finish
		print "plot has been produced"

	#Store N values so NValues() doesn't have to keep being called
	def getAllNValues(self):
		print("\ncalculating all N Values, this may take a second...\n")
		for x in range(0,101):
			self.nvalues.append(self.NValue(x))
		self.allvalues = True #Set allvalues to true, save time in other methods

	#Returns the percent above the N50 threshold showing
	#data accuracy
	def NValuePercent(self, n):

		#Get n50 and total clusters
		littleN = self.nNValue(n)[0]
		total = self.totalClusters()

		#return percentage
		return float(littleN)/float(total)*100