import sys
from stats import Stats

file = "x_clustered_nt_pairs_over1read.txt"

s = Stats(file)
print(s.totalClusters())
print(s.N50())
print(s.n50())
print(s.percent())