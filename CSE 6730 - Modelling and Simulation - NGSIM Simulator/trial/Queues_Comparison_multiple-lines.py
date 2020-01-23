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

from random import random
from operator import itemgetter
from Event_Engine import *
from Activity_Engine import *
from bisect import bisect
import time

EventQueues=[]
for run in range(50):
	print('Run', run+1)
	inter_arrival=[]
	for i in range(len(vehInfo)-1):
		inter_arrival.append((vehInfo[i+1][1]-vehInfo[i][1])/1000.0)


	n_bins=int(len(inter_arrival)**.5)
	bin_width=(max(inter_arrival)-min(inter_arrival))/(n_bins-1)
	intervals=[min(inter_arrival)+bin_width*i for i in range(n_bins+1)]

	bin_val=[]
	for i in intervals[1:]:
		bin_val.append(0.0)

	for i in inter_arrival:
		bin_val[bisect(intervals, i)-1]+=1.0/len(inter_arrival)

	bin_ind=bin_val[:]
	for i in range(len(bin_val)-1):
		bin_val[i+1]+=bin_val[i]

	n_cars=200	

	# Generating vehicles in FEL for 10th St 
	bin_val=[0]+bin_val
	inter_arrivals=[]
	for i in range(n_cars):
		u_rand=random()
		j=bisect(bin_val, u_rand)
		inter_arrivals.append(intervals[j-1]+bin_width*(u_rand-bin_val[j-1])/bin_ind[j-1])

	FEL_10=[[inter_arrivals[0]+10+random()*5, 1, 'arrival']]
	t=inter_arrivals[0]
	for i in range(len(inter_arrivals)-1):
		t+=inter_arrivals[i+1]
		FEL_10.append([max(t+10+random()*5, FEL_10[-1][0]), i+2, 'arrival'])

	# Go-Time (Green+Yellow), No-Go Time (Red), min-serving time, max-serving time 
	ServerInfo_10=[0, 38.3, 62.1, .1, .3]

	t=ServerInfo_10[0]
	signals=[]
	while t<FEL_10[-1][0]*10:
		signals.append([t, 'Signal', 'Go'])
		t+=ServerInfo_10[1]
		signals.append([t, 'Signal', 'No-Go'])
		t+=ServerInfo_10[2]

	FEL_10.extend(signals)
	FEL_10.sort(key=itemgetter(0))  


	# Processing 10th Street Intersection and Creating FEL for 11th Street
	Log_10=Event_QSim(FEL_10, ServerInfo_10)
	Log_10.sort(key=itemgetter(1, 0))   

	i=0; FEL_11=[]
	while i<len(Log_10):
		if i==0:
			FEL_11.append([Log_10[i+1][0]+10+random()*5, Log_10[i+1][1], 'arrival'])
		else:
			FEL_11.append([max(Log_10[i+1][0]+10+random()*5,FEL_11[-1][0]), Log_10[i+1][1], 'arrival'])
		i+=2

	ServerInfo_11=[12.5, 44.7, 55.4, .1, .3]

	t=ServerInfo_11[0]
	signals=[]
	while t<FEL_11[-1][0]*10:
		signals.append([t, 'Signal', 'Go'])
		t+=ServerInfo_11[1]
		signals.append([t, 'Signal', 'No-Go'])
		t+=ServerInfo_11[2]

	FEL_11.extend(signals)
	FEL_11.sort(key=itemgetter(0))  

	# Processing 11th Street Intersection and Creating FEL for 12th Street
	Log_11=Event_QSim(FEL_11, ServerInfo_11)
	Log_11.sort(key=itemgetter(1, 0)) 

	i=0; FEL_12=[]
	while i<len(Log_11):
		if i==0:
			FEL_12.append([Log_11[i+1][0]+10+random()*5, Log_11[i+1][1], 'arrival'])
		else:
			FEL_12.append([max(Log_11[i+1][0]+10+random()*5,FEL_12[-1][0]), Log_11[i+1][1], 'arrival'])
		i+=2

	ServerInfo_12=[25, 64.1, 35.7, .1, .3]

	t=ServerInfo_12[0]
	signals=[]
	while t<FEL_12[-1][0]*10:
		signals.append([t, 'Signal', 'Go'])
		t+=ServerInfo_12[1]
		signals.append([t, 'Signal', 'No-Go'])
		t+=ServerInfo_12[2]

	FEL_12.extend(signals)
	FEL_12.sort(key=itemgetter(0))  

	# Processing 12th Street Intersection and Creating FEL for 14th Street
	Log_12=Event_QSim(FEL_12, ServerInfo_12)
	Log_12.sort(key=itemgetter(1, 0)) 

	i=0; FEL_14=[]
	while i<len(Log_12):
		if i==0:
			FEL_14.append([Log_12[i+1][0]+20+random()*10, Log_12[i+1][1], 'arrival'])
		else:
			FEL_14.append([max(Log_12[i+1][0]+20+random()*10,FEL_14[-1][0]), Log_12[i+1][1], 'arrival'])
		i+=2	

	ServerInfo_14=[50, 37.8, 62.1, .1, .3]

	t=ServerInfo_14[0]
	signals=[]
	while t<FEL_14[-1][0]*10:
		signals.append([t, 'Signal', 'Go'])
		t+=ServerInfo_14[1]
		signals.append([t, 'Signal', 'No-Go'])
		t+=ServerInfo_14[2]

	FEL_14.extend(signals)
	FEL_14.sort(key=itemgetter(0)) 	

	# Processing 14th Street Intersection and getting output from 14th Street
	Log_14=Event_QSim(FEL_14, ServerInfo_14)
	Log_14.sort(key=itemgetter(1, 0))

	#print('VehID  |  Arrival  |  Delay  |  Departure')
	times=[]; queue=[]
	i=0
	while i<len(Log_14):
		gotGreen=Log_14[i+1][0]-Log_14[i+1][3]
		arrived=Log_14[i][0]
		for j in range(int(arrived)+(arrived!=int(arrived)), int(gotGreen)+1):
			if not j in times:
				times.append(j)
				queue.append(1)
			else:
				queue[times.index(j)]+=1
		i+=2

	data=[list(i) for i in zip(times,queue)]
	data.sort(key=lambda x: x[0])
	EventQueues.append(list(map(list, zip(*data))))

ActivityQueues=[]
for run in range(50):
	print('Run', run+1)

	inter_arrival=[]
	for i in range(len(vehInfo)-1):
		inter_arrival.append((vehInfo[i+1][1]-vehInfo[i][1])/1000.0)


	n_bins=int(len(inter_arrival)**.5)
	bin_width=(max(inter_arrival)-min(inter_arrival))/(n_bins-1)
	intervals=[min(inter_arrival)+bin_width*i for i in range(n_bins+1)]

	bin_val=[]
	for i in intervals[1:]:
		bin_val.append(0.0)

	for i in inter_arrival:
		bin_val[bisect(intervals, i)-1]+=1.0/len(inter_arrival)

	bin_ind=bin_val[:]
	for i in range(len(bin_val)-1):
		bin_val[i+1]+=bin_val[i]

	n_cars=200

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


	#print('VehID  |  Arrival  |  Delay  |  Departure')

	times=[]; queue=[]
	i=0
	while i<len(Activities_14):
		gotGreen=Activities_14[i+1][0]
		arrived=Activities_14[i][0]
		for j in range(int(arrived)+(arrived!=int(arrived)), int(gotGreen)+1):
			if not j in times:
				times.append(j)
				queue.append(1)
			else:
				queue[times.index(j)]+=1
		i+=3

	data=[list(i) for i in zip(times,queue)]
	data.sort(key=lambda x: x[0])
	ActivityQueues.append(list(map(list, zip(*data))))	

import matplotlib.pyplot as plt

n=1

for i in EventQueues:
	if n==1:
		X=i[0]; Y=i[1]
	else:
		for j, k in zip(i[0], i[1]):
			ind=bisect(X, j)
			if ind==0 or X[ind-1]!=j:
				X=X[:ind]+[j]+X[ind:]
				Y=Y[:ind]+[k]+Y[ind:]
			else:
				Y[ind-1]+=k
	n+=1
Y=[i/50 for i in Y]
x=[X[0]]; y=[Y[0]]
for i in range(1, len(X)):
	for j in range(x[-1]+1, X[i]):
		x.append(j); y.append(0)
	x.append(X[i]); y.append(Y[i])


n=1
for i in ActivityQueues:
	if n==1:
		X=i[0]; Y=i[1]
	else:
		for j, k in zip(i[0], i[1]):
			ind=bisect(X, j)
			if ind==0 or X[ind-1]!=j:
				X=X[:ind]+[j]+X[ind:]
				Y=Y[:ind]+[k]+Y[ind:]
			else:
				Y[ind-1]+=k
	n+=1
Y=[i/50 for i in Y]
x1=[X[0]]; y1=[Y[0]]
for i in range(1, len(X)):
	for j in range(x1[-1]+1, X[i]):
		x1.append(j); y1.append(0)
	x1.append(X[i]); y1.append(Y[i])

x_lim=max(max(x), max(x1))+10

plt.plot(x, y, label='Run'+str(n))	
plt.title('Event Oriented: Avg Queue: Multiple Runs')
plt.ylabel('Queues (#cars)')
plt.xlabel('Time[s]')
plt.xlim([0, x_lim])
plt.savefig('Event_Queues.png', bbox_inches='tight', dpi=600)
plt.clf()
plt.close()	

plt.plot(x1, y1, label='Run'+str(n))	
plt.title('Activity Scanning: Queues Across Multiple Runs')
plt.ylabel('Queues (#cars)')
plt.xlabel('Time[s]')
plt.xlim([0, x_lim])
plt.savefig('Activity_Queues.png', bbox_inches='tight', dpi=600)
plt.clf()
plt.close()	