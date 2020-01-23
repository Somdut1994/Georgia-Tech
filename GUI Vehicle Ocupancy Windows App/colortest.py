import matplotlib.pyplot as plt
from matplotlib import colors as mcolors


colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

lists=['lightcoral','cadetblue','olivedrab','lemonchiffon', 'palegreen', 'paleturquoise','navajowhite','sandybrown', 'limegreen']

clist=[]
for i in lists:
	print i, colors[i]
	clist.append(colors[i])

print clist