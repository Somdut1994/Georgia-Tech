
# Creating Distribution of inter-arrival time
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


n_cars=200

# # 10th St intersection

# Creating First Future Event List (FEL)
from random import random
bin_val=[0]+bin_val
inter_arrivals=[]
for i in range(n_cars):
	u_rand=random()
	j=bisect(bin_val, u_rand)
	inter_arrivals.append(intervals[j-1]+bin_width*(u_rand-bin_val[j-1])/bin_ind[j-1])

B_10=[[inter_arrivals[0]+10+random()*5, 1, 'arrival']]
t=inter_arrivals[0]
for i in range(len(inter_arrivals)-1):
	t+=inter_arrivals[i+1]
	B_10.append([max(t+10+random()*5, B_10[-1][0]), i+2, 'arrival'])



# Go-Time (Green+Yellow), No-Go Time (Red), min-serving time, max-serving time
ServerInfo_10=[0, 38.3, 62.1, .1, .3]

from ActivityScanning_QSim import *
Activities=Activity_QSim(B_10, ServerInfo_10)
import operator
Activities = sorted(Activities, key = operator.itemgetter(1, 0))

# Printing info for 10th intersection Creating First Future Event List (FEL) for 11th intersection
a=input("\nPrint Data for 10th Street NB (True/False)? ")
if a:
	print('\nVehNr, Intersection Reached, Intersection Service Time, Interection Pass Time, Delay')

B_11=[]
for i in range(0, len(Activities), 3):
	if a:
		print(int(i/3)+1, Activities[i][0], Activities[i+2][0]-Activities[i+1][0], Activities[i+2][0], Activities[i+1][0]-Activities[i][0])
	if i==0:
		B_11.append([Activities[i+2][0]+10+random()*5, int(i/3)+1, 'arrival'])
	else:
		B_11.append([max(Activities[i+2][0]+10+random()*5, B_11[-1][0]), int(i/3)+1, 'arrival'])


# # 11th St intersection

# Go-Time (Green+Yellow), No-Go Time (Red), min-serving time, max-serving time and offset from previous intersection
ServerInfo_11=[0, 44.7, 55.4, .1, .3]

Activities=Activity_QSim(B_11, ServerInfo_11)
Activities = sorted(Activities, key = operator.itemgetter(1, 0))

# Printing info for 11th intersection Creating First Future Event List (FEL) for 12th intersection
a=input("\nPrint Data for 11th Street NB (True/False)? ")
if a:
	print('\nVehNr, Intersection Reached, Intersection Service Time, Interection Pass Time, Delay')

B_12=[]
for i in range(0, len(Activities), 3):
	if a:
		print(int(i/3)+1, Activities[i][0], Activities[i+2][0]-Activities[i+1][0], Activities[i+2][0], Activities[i+1][0]-Activities[i][0])
	if i==0:
		B_12.append([Activities[i+2][0]+10+random()*5, int(i/3)+1, 'arrival'])
	else:
		B_12.append([max(Activities[i+2][0]+10+random()*5, B_12[-1][0]), int(i/3)+1, 'arrival'])