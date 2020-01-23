
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

from random import random
from operator import itemgetter
from Activity_Engine import *


# Generating vehicles as B-event FEL for 10th St 

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

# Processing 10th Street Intersection and Creating B-events for 11th Street 

Activities_10=Activity_QSim(B_10, ServerInfo_10)
Activities_10.sort(key = itemgetter(1, 2))

i=0; B_11=[]
while i<len(Activities_10):
	if i==0:
		B_11.append([Activities_10[i+2][0]+10+random()*5, Activities_10[i][1], 'arrival'])
	else:
		B_11.append([max(Activities_10[i+2][0]+10+random()*5,B_11[-1][0]), Activities_10[i][1], 'arrival'])
	i+=3

# Go-Time (Green+Yellow), No-Go Time (Red), min-serving time, max-serving time and offset from previous intersection
ServerInfo_11=[12.5, 44.7, 55.4, .1, .3]

# Processing 11th Street Intersection and Creating B-events for 12th Street 

Activities_11=Activity_QSim(B_11, ServerInfo_11)
Activities_11.sort(key = itemgetter(1, 2))


i=0; B_12=[]
while i<len(Activities_11):
	if i==0:
		B_12.append([Activities_11[i+2][0]+10+random()*5, Activities_11[i][1], 'arrival'])
	else:
		B_12.append([max(Activities_11[i+2][0]+10+random()*5,B_12[-1][0]), Activities_11[i][1], 'arrival'])
	i+=3

# Go-Time (Green+Yellow), No-Go Time (Red), min-serving time, max-serving time and offset from previous intersection
ServerInfo_12=[25, 64.1, 35.7, .1, .3]

# Processing 12th Street Intersection and Creating B-events for 14th Street 

Activities_12=Activity_QSim(B_12, ServerInfo_12)
Activities_12.sort(key = itemgetter(1, 2))

i=0; B_14=[]
while i<len(Activities_12):
	if i==0:
		B_14.append([Activities_12[i+2][0]+20+random()*10, Activities_12[i][1], 'arrival'])
	else:
		B_14.append([max(Activities_12[i+2][0]+20+random()*10,B_14[-1][0]), Activities_12[i][1], 'arrival'])
	i+=3	

# Go-Time (Green+Yellow), No-Go Time (Red), min-serving time, max-serving time and offset from previous intersection
ServerInfo_14=[50, 37.8, 62.1, .1, .3]

# Processing 14th Street Intersection and Getting necessary output

Activities_14=Activity_QSim(B_14, ServerInfo_14)
Activities_14.sort(key = itemgetter(1, 2))

delays=[]
print('VehID  |  Arrival  |  Delay  |  Departure')

i=0
while i<len(Activities_14):
	delay=Activities_14[i+1][0]-Activities_14[i][0]
	print(Activities_14[i][1], ' | ', Activities_14[i][0], ' | ', delay, ' | ', Activities_14[i+1][0])
	delays.append(delay)
	i+=3

print('Average Delay=', sum(delays)/len(delays))	