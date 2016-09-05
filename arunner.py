import sys
from annotationstats import stats

file = "files/annotation.txt"

s = stats(file)
s.Vgene_usage()
s.V_J_heatmap()
print 'done\n'