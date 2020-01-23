from random import random
import csv

simtTime=600
T=0
i=0
vmax=7
vehRecords=[['Time-stamp(s)', 'VehNr' ,'Origin-Time(s)', 'Position (ft)', 'Speed(ft/s)', 'Direction', 'Lane']]
vehNr=[]
vehSt=[]

n=0
cells_not_empty=[]
cells_LT_not_empty=[]
while T<=simtTime:
	print('t =',T)
	# generate vehicles at first corridor
	if random()<0.3:
		if len(cells_not_empty)==0 or cells_not_empty[0][0]>0:
			n+=1
			if random()>.05: # through
				vehNr.append(n); vehSt.append(T)
				cells_not_empty=[(0, n, int(2+5*random()))]+cells_not_empty
			else:
				# left turn
				vehNr.append(n); vehSt.append(T)
				cells_LT_not_empty=[(0, n, int(2+5*random()))]+ cells_LT_not_empty

	# generate vehicles entering from EB left-turn during (green+yellow) phase
	if (T-87.6)%(9.8+89.4)<9.8:
		if random()<0.25:
			flag=0
			for i in cells_not_empty:
				if i[0]==67:
					flag=1
					break
			if flag==1:
				n+=1
				vehNr.append(n); vehSt.append(T)
				cells_not_empty.append((67, n, int(2+5*random())))
				cells_not_empty=sorted(cells_not_empty, key=lambda x: x[0])

	# give velocity to vehicles
	if len(cells_not_empty)>0:
		new_cells_not_empty=[]
		for j in range(len(cells_not_empty)-1, -1, -1):
			cell, vN, v=cells_not_empty[j]
			# First corridor Through
			if cell<68:
				timeblock=T%100.4
				# Green and Yellow Time
				if timeblock<38.3:
					# trying to reach vmax
					if v<vmax:
						v+=1
					# maintaining gap
					if new_cells_not_empty!=[]:
						v=max(0,min(v, new_cells_not_empty[0][0]-cell-1))
					# random decceleration
					u_rand=random()
					if T<34.7:
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
					if v<vmax:
						v+=1	
					# maintaining gap
					if new_cells_not_empty!=[]:
						v=max(0,min(v, new_cells_not_empty[0][0]-cell-1))						
					# reaching the signal head and stopping there
					v=max(0,min(v, 65-cell))

			# Second corridor Through
			else:
				timeblock=T%100.1
				# Green and Yellow Time
				if timeblock<44.7:
					# trying to reach vmax
					if v<vmax:
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
					if v<vmax:
						v+=1
					# maintaining gap
					if new_cells_not_empty!=[]:
						v=max(0,min(v, new_cells_not_empty[0][0]-cell-1))											
					# reaching the signal head and stopping there
					v=max(0,min(v, 133-cell))	
			if v<0:
				raise ValueError('v negative')
			vehRecords.append([T, vN, vehSt[vehNr.index(vN)], 4+cell*8, v*8, 'TR', 0])
			if cell+v<135:
				new_cells_not_empty=[(cell+v, vN, v)]+new_cells_not_empty
		cells_not_empty=new_cells_not_empty

	if len(cells_LT_not_empty)>0:
		new_cells_LT_not_empty=[]
		for j in range(len(cells_LT_not_empty)-1, -1, -1):
			cell, vN, v=cells_LT_not_empty[j]
			# First corridor Left-Turn
			timeblock=(T-89.8)%100.4
			# Green and Yellow Time
			if timeblock<10.6:
				# trying to reach vmax
				if v<vmax:
					v+=1
				# maintaining gap
				if new_cells_LT_not_empty!=[]:
					v=max(0,min(v, new_cells_LT_not_empty[0][0]-cell-1))
				# random decceleration
				u_rand=random()
				if T<7:
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
				if v<vmax:
					v+=1
				# maintaining gap
				if new_cells_LT_not_empty!=[]:
					v=max(0,min(v, new_cells_LT_not_empty[0][0]-cell-1))
				#getting towards signal-head and stop				
				v=max(0,min(v, 65-cell))
			if v<0:
				raise ValueError('v negative')				
			vehRecords.append([T, vN, vehSt[vehNr.index(vN)], 4+cell*8, v*8, 'LT', 1])
			if cell+v<66:
				new_cells_LT_not_empty=[(cell+v, vN, v)]+new_cells_LT_not_empty
		cells_LT_not_empty=new_cells_LT_not_empty
	T+=1

with open("Trajectory.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(vehRecords)