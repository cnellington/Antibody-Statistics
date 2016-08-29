import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Stats:

	clusters = None #arange object
	lengths = None #list object
	nvalues = [] #stored Nvalues 0-100 to cut down on Nvalue usage/runtime (values added with NPlot() or getAllNValues())
	#littlenvalues = [] #stored little n values
	allvalues = False #has getAllNValues been run

	def __init__(self, filename):
		df = pd.read_csv(filename, sep='\t')
		self.clusters = self.lengths = df.Clustered
		#self.clusters = self.lengths = pd.Series(np.arange(1,11,1)) #Test arange for NValues
		self.lengths.tolist().sort(reverse = True)
		

	#Total clusters from PandaSeq output
	def totalClusters(self):
		return self.clusters.count()




#~~~~~~~~~~ Calculating N Value Data ~~~~~~~~~~~~~
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

	#Store N values so NValues() doesn't have to keep being called
	def getAllNValues(self):

		print("\ncalculating all N Values, this may take a second...")

		for x in range(0,101):
			self.nvalues.append(self.NValue(x))
		self.allvalues = True #Set allvalues to true, save time in other methods




#~~~~~~~~~~ Calculating Little N Value Data ~~~~~~~~~~~~~
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

	def getAllLittleNValues(self):
		littleNValues = []
		for x in range(1,101):
			littleNValues.append(self.nNValue(x)[1])
		return littleNValues



#~~~~~~~~~~ Percent N Value Data ~~~~~~~~~~~~~
	#Returns the percent above the N50 threshold showing
	#data accuracy
	def NValuePercent(self, n):

		#Get n50 and total clusters
		littleN = self.nNValue(n)[0]
		total = self.totalClusters()

		#return percentage
		return float(littleN)/float(total)*100



#~~~~~~~~~~ Graphing N Value Data ~~~~~~~~~~~~~
	#Plot from N01 to N100
	def NPlot(self):

		#Produce and store necessary N values
		if(not self.allvalues):
			self.getAllNValues()

		xaxis = range(1,101)

		#uncomment if margins are needed for graph clarity
		#buff = .05 #determines how close the plot is to the axes
		#xbuffer = int(xaxis[len(xaxis)-1]*buff) #x-axis buffer for clarity
		#ybuffer = int(self.nvalues[0]*buff) #y-axis buffer for clarity
		
		plt.ylabel("Cluster Size")
		plt.xlabel("N value (smallest cluster above n percent mass)")
		plt.plot(xaxis, self.nvalues[1:])
		#plt.axis([0-xbuffer, 100+xbuffer, 0-ybuffer, self.nvalues[0]+ybuffer ]) #plot axes, buffers added to both limits
		
		print("\nplotting graph...")
		plt.show()

		#finish
		print "plot has been produced"

	#Plot from nN01 to nN100
	def nNPlot(self):

		#Produce and store necessary N values
		if(not self.allvalues):
			self.getAllNValues()

		xaxis = range(1,101)

		#Fetch all little n values
		littlenvalues = self.getAllLittleNValues()
		
		
		plt.ylabel("Number of Clusters Above NX")
		plt.xlabel("N value")
		plt.plot(xaxis, littlenvalues)
		#plt.axis([0-xbuffer, 100+xbuffer, 0-ybuffer, littleNValues[len(littleNValues)-1]+ybuffer ]) #plot axes, buffers added to both limits
		
		print("\nplotting graph...\n")
		plt.show()

		#finish
		print "plot has been produced"

	def crossPlot(self, nplot, littlenplot):

		if(not nplot and not littlenplot):
			print("\nWhat are you doing, you silly sausage?\nPlot something next time.")
			return None

		if(not self.allvalues):
			self.getAllNValues()

		xaxis = range(1,101)

		if(nplot and not littlenplot):
			self.NPlot()
		if(littlenplot and not nplot):
			self.nNPlot()
		if(nplot and littlenplot):

			littlenvalues = self.getAllLittleNValues()

			fig, ax1 = plt.subplots()
			ax1.plot(xaxis, self.nvalues[1:], 'b-')
			ax1.set_xlabel('N Value')
			ax1.set_ylabel('Cluster Size', color='b')
			for t1 in ax1.get_yticklabels():
				t1.set_color('b')

			ax2 = ax1.twinx()
			ax2.plot(xaxis, littlenvalues, 'r-')
			ax2.set_ylabel('Number of Clusters Above NX', color='r')
			for t1 in ax2.get_yticklabels():
				t1.set_color('r')

			print "N Plot Average Slope: %s"%(self.avgSlope(xaxis, self.nvalues[1:]))
			print "n Plot Average Slope: %s"%(self.avgSlope(xaxis, littlenvalues))
			print("\nplotting graph...")
			plt.show()

				#avgSlope(self, xaxis, yaxis) or
				#avgSlope(self, x1, x2, y1, y2)
	def avgSlope(*args):
		if len(args) == 3:
			xaxis, yaxis = args[1], args[2]
			x1 = float(xaxis[0])
			x2 = float(xaxis[len(xaxis)-1])
			y1 = float(yaxis[0])
			y2 = float(yaxis[len(yaxis)-1])
			return (y2-y1)/(x2-x1) #Because calculus

		if len(args) == 5:
			x1, x2, y1, y2 = args[1:]
			return float(y2-y1)/float(x2-x1) #Because calculus

	def simpsonDiversity(self):
		D = 0.0
		N = float(len(self.clusters))
		for n in self.clusters:
			D += (float(n)/N)**2 #Simpson Diversity Index formula
		return D