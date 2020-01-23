
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

# # Plot Inter-arrival cumulative distribution
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches 

# fig,ax=plt.subplots(1)
# y=[0]+bin_val

# for j in range(len(bin_ind)):
# 	ax.add_patch(patches.Rectangle((intervals[j], 0),  bin_width, bin_ind[j]))
# ax.plot(intervals, y, color='r')
# plt.xlabel('Inter-arrival Time(s)')
# plt.ylabel('Frequency(%)')
# plt.title('Cumulative and Histogram of Inter-arrrival Time')
# plt.savefig('Inter-arrival_Distribution.png',bbox_inches='tight')
# plt.clf()
# plt.close() 

n_cars=200

# # 10th St intersection

# Creating First Future Event List (FEL)
from random import random
bin_val=[0]+bin_val
FEL_10=[]
for i in range(n_cars):
	u_rand=random()
	j=bisect(bin_val, u_rand)
	t=intervals[j-1]+bin_width*(u_rand-bin_val[j-1])/bin_ind[j-1]
	if i>0:
		t+=FEL_10[-1][0]
	FEL_10.append([t,i+1, 10+random()*5])

# Go-Time (Green+Yellow), No-Go Time (Red), min-serving time, max-serving time
ServerInfo_10=[0, 38.3, 62.1, .1, .3]

from EventOriented_QSim import *
Clients=Event_QSim(FEL_10, ServerInfo_10)

# Printing info for 10th intersection Creating First Future Event List (FEL) for 11th intersection
a=input("\nPrint Data for 10th Street NB (True/False)? ")
if a:
	print('\nVehNr, Corridor Entry, Intersection Reached, Intersection Service Time, Interection Pass Time, Delay')
n=1
FEL_11=[]
for i in Clients:
	if a:
		print(n, i.entry_date, i.arrival_date, i.service_start_date, i.service_time, i.service_end_date, i.wait)
	FEL_11.append([i.service_end_date, n, 10+random()*5])
	n+=1


# # 11th St intersection

# Go-Time (Green+Yellow), No-Go Time (Red), min-serving time, max-serving time and offset from previous intersection
ServerInfo_11=[0, 44.7, 55.4, .1, .3]

Clients=Event_QSim(FEL_11, ServerInfo_11)

# Printing info for 11th intersection Creating First Future Event List (FEL) for 12th intersection
a=input("\nPrint Data for 11th Street NB (True/False)? ")
if a:
	print('\nVehNr, Corridor Entry, Intersection Reached, Intersection Service Time, Interection Pass Time, Delay')
n=1
FEL_12=[]
for i in Clients:
	if a:
		print(n, i.entry_date, i.arrival_date, i.service_start_date, i.service_time, i.service_end_date, i.wait)
	FEL_12.append([i.service_end_date, n, 10+random()*5])
	n+=1


