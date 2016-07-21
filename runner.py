import sys
from stats import Stats

file = "x_clustered_nt_pairs_over1read.txt"

s = Stats(file)
print(s.totalClusters())
print "N50: %s N90: %s" % (s.nN50(), s.nN90())
print "nN50: %s nN90: %s" % (s.N50(), s.N90())
s.getAllNValues() #Speed up other functions
print "[NValue, nNValue]"
for x in range(10,101, 10):
	print ("N%s"+str(s.nNValue(x))) % x
	print(s.NValuePercent(x))
s.NPlot()