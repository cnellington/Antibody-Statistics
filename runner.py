import sys
from stats import Stats

file = "x_clustered_nt_pairs_over1read.txt"

s = Stats(file)
print(s.totalClusters())
print "[NValue, nNValue]"
for x in range(10,101, 10):
	print ("N%s"+str(s.nNValue(x))) % x
	print(s.NValuePercent(x))
s.crossPlot(nplot=True, littlenplot = True)
print s.simpsonDiversity()