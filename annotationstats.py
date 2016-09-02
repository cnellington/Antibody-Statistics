import sys
import collections
from collections import defaultdict
from collections import OrderedDict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

class stats:


	vlist = None #Tuple list of all V sequence types and their quality
	jlist = None #Typle list of all J sequence types and their quality
	dlist = None #Tuple list of all D sequence types and their quality

	vgenes = defaultdict() #Ordered Dict of all vgene types and their count
	jgenes = defaultdict() #Ordered Dict of all vgene types and their count
	dgenes = defaultdict() #Ordered Dict of all vgene types and their count


	#import and parse the file this class will use around
	def __init__(self, filename):

		print("\n************************************************************")
		print("************READING AND CLEANING ANNOTATION DATA************")
		print("***************...this may take a second...*****************\n")
		df = pd.read_csv(filename, sep='\t')
		self.vlist = df.allVHitsWithScore.tolist()
		self.jlist = df.allJHitsWithScore.tolist()
		self.dlist = df.allDHitsWithScore.tolist()
		
		self.cleanData(self.vlist)
		self.cleanData(self.jlist)
		self.cleanData(self.dlist)
		print("done!")

	#Returns dict {chain-name, chain-count}
	def geneCount(self, datalist):
		tally = defaultdict()
		for gene, quality in datalist:
			if len(gene)>0:
				if gene in tally:
					tally[gene] += 1
				else:
					tally.update({gene:1})
		return tally


	#Get read element chain type
	def getChain(self, data):
		i = data.find("*")
		if i == -1:
			return None
		return data[:i]


	#Get read element quality
	def getQuality(self, data):
		i = data.find("(")
		if i == -1:
			return None
		j = data.find(")")
		return int(data[i+1:j])


	#Sorts and determines which chain elements need to be sorted and 
	def cleanData(self, datalist):
		for i in range(0,len(datalist)):
			#Selects the best of the reads
			datalist[i] = str(datalist[i])
			if(datalist[i] and datalist[i].find(",") != -1):
				datalist[i] = self.getBestChain(datalist[i])

			#Creates tuple list object
			if(datalist[i].find("IGH") != -1 and datalist[i].find("*") != -1):
				datalist[i] = [self.getChain(datalist[i]), self.getQuality(datalist[i])]

			else: #For the occasional "nan" value
				datalist[i] = ["", 0]


	#returns the best quality read from the list element given
	def getBestChain(self, data):
		chains = [x.strip() for x in data.split(',')] #splice data by commas, leaves individual reads and their quality
		index = 1 #Compare any other chain qualities
		best = self.getQuality(chains[0])
		for x in chains[1:]:
			if self.getQuality(x) == best:
				index += 1

		return chains[random.randrange(0,index)]

	#Read usage bar plot from single list (v, d, j)
	def barPlot(self, datalist):

		tally = self.geneCount(datalist)

		#Limit the items plotted to those over 1% of the read mass
		geneplot = defaultdict()
		for g, n in tally.iteritems():
			if n > int(sum(tally.values())*.01):
				geneplot[g] = n

		#Get plotting values
		olist = OrderedDict(sorted(geneplot.items(),key=lambda t: t[0]))
		summe = sum(olist.values())
		freq = [float(x)/float(summe) for x in olist.values()]
		
		#Create plot
		fig = plt.figure()
		width = .35
		ind = np.arange(len(geneplot.keys()))
		plt.bar(ind, freq)
		plt.xticks(ind + width, geneplot.keys())
		locs, labels = plt.xticks() 
		plt.setp(labels, rotation=90)
		plt.show()

	def Vgene_usage(self):
		print("************************************************************")
		print("*****************CREATING V GENE USAGE PLOT*****************")
		print("************************************************************\n")

		self.barPlot(self.vlist)

	def Jgene_usage(self):
		print("************************************************************")
		print("*****************CREATING J GENE USAGE PLOT*****************")
		print("************************************************************\n")

		self.barPlot(self.jlist)

	def Dgene_usage(self):
		print("************************************************************")
		print("*****************CREATING D GENE USAGE PLOT*****************")
		print("************************************************************\n")

		self.barPlot(self.dlist)

	#Creates a heatmap graph of the V and J gene pairings
	def V_J_heatmap(self):
		print("************************************************************")
		print("*****************CREATING V/J GENE HEATMAP******************")
		print("************************************************************\n")
		
		#Getting which reads to check for
		sorted(geneplot.items(),key=lambda t: t[0]))
		vcount = OrderedDict(sorted(self.geneCount(self.vlist)
		jcount = self.geneCount(self.jlist)
		vjlist = []

		for x in range(len(vcount)):
			vjlist.append([])
			for y in range(len(jcount)):
				vjlist.append(0)

		#2D dict for storing gene hits
		#jaxis = {key:0 for key, val in jcount.iteritems()}
		#vjlist = {key: jaxis.copy() for key, val in vcount.iteritems()}

		#Checking for read hits in v and j list
		for x in range(len(self.vlist)):
			vgene = self.vlist[x][0]
			jgene = self.jlist[x][0]
			vjlist[vcount.index(vgene)][jcount.index(jgene)] += 1

		for x in vjlist:
			print x