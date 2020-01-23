
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
from Event_Engine import *

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

delays=[]
print('VehID  |  Arrival  |  Delay  |  Departure')

i=0
while i<len(Log_14):
	delay=Log_14[i+1][0]-Log_14[i+1][3]-Log_14[i][0]
	print(Log_14[i][1], ' | ', Log_14[i][0], ' | ', delay, ' | ', Log_14[i+1][0])
	delays.append(delay)
	i+=2

print('Average Delay at 14th Street=', sum(delays)/len(delays))


