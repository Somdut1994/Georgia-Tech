from random import random
import csv

no_vel=[]; TT=[]; TT1=[]
for run in range(10):
	print('Run', run+1)

	n=0; vehst=[]; vehN=[]

	simTime=1800
	T=0
	i=0
	vmax=4
	vehRecords=[['Time-stamp(s)', 'VehNr' ,'Origin-Time(s)', 'Position (ft)', 'SegID', 'Speed(ft/s)', 'Direction', 'Lane']]
	vehNr=[]
	vehSt=[]

	n=0
	cells_not_empty=[]
	cells_LT_not_empty=[]
	cells_LT_not_empty1=[]
	vnr=[]
	while T<=simTime:
		num=0
		#print('t =',T)
		# generate vehicles at first corridor
		if random()<0.77:
			if len(cells_not_empty)==0 or cells_not_empty[0][0]>0:
				n+=1
				if random()>0.1: # through
					vehNr.append(n); vehSt.append(T)
					cells_not_empty=[(0, n, int(1+2*random()))]+cells_not_empty
				else:
					# left turn
					vehNr.append(n); vehSt.append(T)
					cells_LT_not_empty=[(0, n, int(1+2*random()))]+ cells_LT_not_empty

		# generate vehicles entering from EB left-turn during (green+yellow) phase
		if (T-87.6)%(9.8+89.4)<9.8:
			if random()<0.25:
				flag=0
				for i in cells_not_empty:
					#if i[0]==38:
					if i[0]==29:
						flag=1
						break
				if flag==1:
					n+=1
					vehNr.append(n); vehSt.append(T)
					cells_not_empty.append((29, n, int(1+2*random())))
					cells_not_empty=sorted(cells_not_empty, key=lambda x: x[0])

		# give velocity to vehicles
		if len(cells_not_empty)>0:
			new_cells_not_empty=[]
			for j in range(len(cells_not_empty)-1, -1, -1):
				cell, vN, v=cells_not_empty[j]
				# First corridor Through
				if cell<28:
					segID=0
					timeblock=T%100.4
					# Green and Yellow Time
					if timeblock<38.3:
						# trying to reach vmax
						if (v==vmax-1 and random()<0.5) or (v==vmax-2 and random()<0.85) or v<vmax-2:
							v+=1
						# maintaining gap
						if new_cells_not_empty!=[]:
							v=max(0,min(v, new_cells_not_empty[0][0]-cell-1))
						# random decceleration
						u_rand=random()
						if timeblock<34.7:
							# 5% at green time
							if u_rand<.05:
								if v>1:
									v-=1
						else:
							# 20% at yellow time
							if u_rand<.2:
								if v>1:
									v-=1					

					# Red Time
					else:
						# trying to reach vmax
						if (v==vmax-1 and random()<0.5) or (v==vmax-2 and random()<0.85) or v<vmax-2:
							v+=1					
						# maintaining gap
						if new_cells_not_empty!=[]:
							v=max(0,min(v, new_cells_not_empty[0][0]-cell-1))						
						# reaching the signal head and stopping there
						v=max(0,min(v, 27-cell))

				# Second corridor Through
				elif cell<67:
					segID=1
					timeblock=(T-12.5)%100.1
					# Green and Yellow Time
					if timeblock<44.7:
						# trying to reach vmax
						if (v==vmax-1 and random()<0.5) or (v==vmax-2 and random()<0.85) or v<vmax-2:
							v+=1
						# maintaining gap
						if new_cells_not_empty!=[]:
							v=max(0,min(v, new_cells_not_empty[0][0]-cell-1))
						# random decceleration
						u_rand=random()
						if T<41.5:
							# 5% at green time
							if u_rand<.05:
								if v>1:
									v-=1
						else:
							# 20% at yellow time
							if u_rand<.2:
								if v>1:
									v-=1					

					# Red Time
					else:
						# trying to reach vmax
						if (v==vmax-1 and random()<0.5) or (v==vmax-2 and random()<0.85) or v<vmax-2:
							v+=1					
						# maintaining gap
						if new_cells_not_empty!=[]:
							v=max(0,min(v, new_cells_not_empty[0][0]-cell-1))											
						# reaching the signal head and stopping there
						v=max(0,min(v, 66-cell))

				# Third Corridor Through
				elif cell<101:
					segID=2
					timeblock=(T-25)%99.8
					# Green and Yellow Time
					if timeblock<64.1:
						# trying to reach vmax
						if (v==vmax-1 and random()<0.5) or (v==vmax-2 and random()<0.85) or v<vmax-2:
							v+=1
						# maintaining gap
						if new_cells_not_empty!=[]:
							v=max(0,min(v, new_cells_not_empty[0][0]-cell-1))
						# random decceleration
						u_rand=random()
						if T<60.9:
							# 5% at green time
							if u_rand<.05:
								if v>1:
									v-=1
						else:
							# 20% at yellow time
							if u_rand<.2:
								if v>1:
									v-=1					

					# Red Time
					else:
						# trying to reach vmax
						if (v==vmax-1 and random()<0.5) or (v==vmax-2 and random()<0.85) or v<vmax-2:
							v+=1					
						# maintaining gap
						if new_cells_not_empty!=[]:
							v=max(0,min(v, new_cells_not_empty[0][0]-cell-1))											
						# reaching the signal head and stopping there
						v=max(0,min(v, 100-cell))

				# Fourth Corridor Through
				elif cell<158:
					segID=3
					timeblock=(T-50)%99.9
					# Green and Yellow Time
					if timeblock<37.8:
						# trying to reach vmax
						if (v==vmax-1 and random()<0.5) or (v==vmax-2 and random()<0.85) or v<vmax-2:
							v+=1
						# maintaining gap
						if new_cells_not_empty!=[]:
							v=max(0,min(v, new_cells_not_empty[0][0]-cell-1))
						# random decceleration
						u_rand=random()
						if T<34.6:
							# 5% at green time
							if u_rand<.05:
								if v>1:
									v-=1
						else:
							# 20% at yellow time
							if u_rand<.2:
								if v>1:
									v-=1					

					# Red Time
					else:
						# trying to reach vmax
						if (v==vmax-1 and random()<0.5) or (v==vmax-2 and random()<0.85) or v<vmax-2:
							v+=1					
						# maintaining gap
						if new_cells_not_empty!=[]:
							v=max(0,min(v, new_cells_not_empty[0][0]-cell-1))											
						# reaching the signal head and stopping there
						v=max(0,min(v, 157-cell))					

				if v<0:
					raise ValueError('v negative')
				vehRecords.append([T, vN, vehSt[vehNr.index(vN)], 7+cell*14, segID, v*14, 'TR', 0])
				num+=1
				if cell+v<159:
					flag=0
					if cell<101 and cell+v>=101 and random()<0.05:
						if len(cells_LT_not_empty1)==0 or cells_LT_not_empty1[0][0]>cell+v:
							cells_LT_not_empty1=[(cell+v, vN, v)]+cells_LT_not_empty1
							flag=-1
					if flag==0:
						new_cells_not_empty=[(cell+v, vN, v)]+new_cells_not_empty
			cells_not_empty=new_cells_not_empty

		#  First Corridor Left-turn Lane
		if len(cells_LT_not_empty)>0:
			new_cells_LT_not_empty=[]
			for j in range(len(cells_LT_not_empty)-1, -1, -1):
				cell, vN, v=cells_LT_not_empty[j]
				# First corridor Left-Turn
				timeblock=(T-87.6)%100.4
				# Green and Yellow Time
				if timeblock<10.6:
					# trying to reach vmax
					if (v==vmax-1 and random()<0.5) or (v==vmax-2 and random()<0.85) or v<vmax-2:
						v+=1
					# maintaining gap
					if new_cells_LT_not_empty!=[]:
						v=max(0,min(v, new_cells_LT_not_empty[0][0]-cell-1))
					# random decceleration
					u_rand=random()
					if timeblock<7:
						# 5% at green time
						if u_rand<.05:
							if v>1:
								v-=1
					else:
						# 20% at yellow time
						if u_rand<.2:
							if v>1:
								v-=1					

				# Red Time
				else:
					# trying to reach vmax
					if (v==vmax-1 and random()<0.5) or (v==vmax-2 and random()<0.85) or v<vmax-2:
						v+=1				
					# maintaining gap
					if new_cells_LT_not_empty!=[]:
						v=max(0,min(v, new_cells_LT_not_empty[0][0]-cell-1))
					#getting towards signal-head and stop				
					v=max(0,min(v, 27-cell))
				if v<0:
					raise ValueError('v negative')				
				vehRecords.append([T, vN, vehSt[vehNr.index(vN)], 7+cell*14, 0, v*14, 'LT', 1])
				num+=1
				if cell+v<28:
					new_cells_LT_not_empty=[(cell+v, vN, v)]+new_cells_LT_not_empty
			cells_LT_not_empty=new_cells_LT_not_empty

		#  Fourth Corridor Left-turn Lane
		if len(cells_LT_not_empty1)>0:
			new_cells_LT_not_empty1=[]
			for j in range(len(cells_LT_not_empty1)-1, -1, -1):
				cell, vN, v=cells_LT_not_empty1[j]
				# First corridor Left-Turn
				timeblock=(T-83.9-25)%99.9
				# Green and Yellow Time
				if timeblock<12.4:
					# trying to reach vmax
					if (v==vmax-1 and random()<0.5) or (v==vmax-2 and random()<0.85) or v<vmax-2:
						v+=1
					# maintaining gap
					if new_cells_LT_not_empty1!=[]:
						v=max(0,min(v, new_cells_LT_not_empty1[0][0]-cell-1))
					# random decceleration
					u_rand=random()
					if timeblock<8.8:
						# 5% at green time
						if u_rand<.05:
							if v>1:
								v-=1
					else:
						# 20% at yellow time
						if u_rand<.2:
							if v>1:
								v-=1					

				# Red Time
				else:
					# trying to reach vmax
					if (v==vmax-1 and random()<0.5) or (v==vmax-2 and random()<0.85) or v<vmax-2:
						v+=1				
					# maintaining gap
					if new_cells_LT_not_empty1!=[]:
						v=max(0,min(v, new_cells_LT_not_empty1[0][0]-cell-1))
					#getting towards signal-head and stop				
					v=max(0,min(v, 157-cell))
				if v<0:
					raise ValueError('v negative')				
				vehRecords.append([T, vN, vehSt[vehNr.index(vN)], 7+cell*14, 3, v*14, 'LT', 1])
				num+=1
				if cell+v<158:
					new_cells_LT_not_empty1=[(cell+v, vN, v)]+new_cells_LT_not_empty1
			cells_LT_not_empty1=new_cells_LT_not_empty1		
		T+=1
		vnr.append(num)
	for i in range(1, len(vnr)):
		vnr[i]+=vnr[i-1]
	for i in range(1, len(vnr)):
		vnr[i]/=(i+1)
	no_vel.append(vnr)

	with open("Trajectory.csv", "w", newline='') as f:
	    writer = csv.writer(f)
	    writer.writerows(vehRecords)
	
	m=0; stnr=[]; stt=[]; stt1=[]
	with open('Trajectory.csv') as file:
		for line in file:
			m+=1
			if m>1:
				f=line.split('\n')[0].split(',')
				if int(f[4])==0:
					if not int(f[1]) in stnr:
						stnr.append(int(f[1]))
						stt.append(0)
						stt1.append(0)
				if int(f[4])==3 and int(f[-1])==0:
					if int(f[1]) in stnr:
						stt[stnr.index(int(f[1]))]=int(f[0])-int(f[2])+1
						stt1[stnr.index(int(f[1]))]=int(f[0])
	tt=[]; tt1=[]
	for i in range(len(stnr)):
		if stt[i]!=0:
			tt.append(stt[i])
			tt1.append(stt1[i])
	for i in range(1, len(tt)):
		tt[i]+=tt[i-1]
	for i in range(1, len(tt)):
		tt[i]/=(i+1)
	TT.append(tt); TT1.append(tt1)

import matplotlib.pyplot as plt

n=0
for i in no_vel:
	n+=1
	plt.plot(range(1801), i, label='Run '+str(n))
plt.xlabel('Simulation Time [s]')
plt.ylabel('Average Number of Vehicles in Network')
plt.title('Mean #Vehicles with Simulation Time')
plt.savefig('CA_converge_number.png',bbox_inches='tight')
plt.clf()
plt.close() 

n=0
for i, j in zip(TT1, TT):
	n+=1
	plt.plot(i, j, label='Run '+str(n))
plt.xlabel('Simulation Time [s]')
plt.ylabel('Average Travel time [s]')
plt.title('Average Travel time with Simulation Time')
plt.savefig('CA_converge_TT.png',bbox_inches='tight')
plt.clf()
plt.close() 	


Y=[]
for i in range(60):
	Y.append([])

for i in no_vel:
	n=0
	for k in i:
		Y[min(int(n/30), 59)].append(k)
		n+=1

for i in range(len(Y)):
	if Y[i]!=[]:
		Y[i]=sum(Y[i])/len(Y[i])
	else:
		Y[i]=Y[i-1]
plt.plot(range(15, 1800, 30), Y, label='Run '+str(n))
plt.xlabel('Simulation Time [s]')
plt.ylabel('Mean #Vehicles with Simulation Time')
plt.title('Welch\'s: Moving Average #Vehicles')
plt.savefig('CA_Welch_number.png',bbox_inches='tight')
plt.clf()
plt.close() 

Y=[]
for i in range(60):
	Y.append([])

for i, j in zip(TT1, TT):
	for k, l in zip(i, j):
		Y[min(int(k/30), 59)].append(l)

pops=0
Y1=Y[:]
for i in range(len(Y1)):
	if Y[i]!=[]:
		break
	else:
		Y1.pop(0)
		pops+=1
Y=Y1
for i in range(len(Y)):
	if Y[i]!=[]:
		Y[i]=sum(Y[i])/len(Y[i])
	else:
		Y[i]=Y[i-1]

print(Y[0], len(Y))
plt.plot(range(15+30*pops, 1800, 30), Y, label='Run '+str(n))
plt.xlabel('Simulation Time [s]')
plt.ylabel('Average Travel time [s]')
plt.title('Welch\'s: Moving Average Travel time')
plt.savefig('CA_Welch_TT.png',bbox_inches='tight')
plt.clf()
plt.close() 