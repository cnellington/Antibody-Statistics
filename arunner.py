import sys
from annotationstats import stats

file = "files/annotation_100.txt"

s = stats(file)
s.Vgene_usage(threshold = .01, figname = "Caleb")
print 'done\n'