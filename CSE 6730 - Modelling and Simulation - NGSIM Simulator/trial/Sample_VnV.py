# Creating Distribution of inter-arrival time
from random import random

n=0; vehst=[]; vehN=[]
with open('Trimmed_NB_XY_Data.csv') as file:
	for line in file:
		if n>0:
			f=line.split('\n')[0].split(',')
			if not int(f[0]) in vehN:
				vehN.append(int(f[0])); vehst.append(float(f[1]))
		n+=1

vehInfo=sorted(zip(vehN, vehst), key=lambda x: x[1])

inter_arrival=[]
for i in range(len(vehInfo)-1):
	inter_arrival.append((vehInfo[i+1][1]-vehInfo[i][1])/1000.0)

X=[]; Y=[]
for i in inter_arrival:
	if random()>0.5:
		X.append(i)
	else:
		Y.append(i)

import matplotlib.pyplot as plt
import matplotlib.patches as patches 

inter_arrival=X

n_bins=int(len(inter_arrival)**.5)
bin_width=(max(inter_arrival)-min(inter_arrival))/(n_bins-1)
intervals=[min(inter_arrival)+bin_width*i for i in range(n_bins+1)]

bin_val=[]
for i in intervals[1:]:
	bin_val.append(0.0)


from bisect import bisect

for i in inter_arrival:
	bin_val[bisect(intervals, i)-1]+=1.0/len(inter_arrival)

bin_ind=bin_val[:]
for i in range(len(bin_val)-1):
	bin_val[i+1]+=bin_val[i]


fig,ax=plt.subplots(1)
y=[0]+bin_val

ax.plot(intervals, y, color='r', label='Output')


inter_arrival=Y

n_bins=int(len(inter_arrival)**.5)
bin_width=(max(inter_arrival)-min(inter_arrival))/(n_bins-1)
intervals=[min(inter_arrival)+bin_width*i for i in range(n_bins+1)]

bin_val=[]
for i in intervals[1:]:
	bin_val.append(0.0)


from bisect import bisect

for i in inter_arrival:
	bin_val[bisect(intervals, i)-1]+=1.0/len(inter_arrival)

bin_ind=bin_val[:]
for i in range(len(bin_val)-1):
	bin_val[i+1]+=bin_val[i]

y=[0]+bin_val

ax.plot(intervals, y, color='b', label='Validation')
plt.legend()
plt.xlabel('Inter-arrival Time(s)')
plt.ylabel('Frequency(%)')
plt.title('CDF Comparison Inter-arrrival Time')
plt.savefig('Inter-arrival_VnV.png',bbox_inches='tight')
plt.clf()
plt.close() 