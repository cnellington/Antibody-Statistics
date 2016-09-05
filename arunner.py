import sys
from annotationstats import stats

file = "files/annotation_100.txt"

s = stats(file)
s.Vgene_usage()
s.Vgene_usage(threshold = .5)
s.V_J_heatmap()
s.V_J_heatmap(threshold = .5)
print 'done\n'