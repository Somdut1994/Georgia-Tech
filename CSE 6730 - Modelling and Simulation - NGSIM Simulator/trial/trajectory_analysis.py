vehNr=[]
vehT=[]; vehD=[] 
vehNr1=[]
vehT1=[]; vehD1=[] 
vehNr2=[]
vehT2=[]; vehD2=[] 
n=0
with open('Trajectory.csv') as file:
	for line in file:
		n+=1
		if n>1:
			f=line.split('\n')[0].split(',')
			if f[6]=='TR':
				if  not int(f[1]) in vehNr:
					vehNr.append(int(f[1]))
					vehT.append([int(f[0])])
					vehD.append([int(f[3])])
				else:
					ind=vehNr.index(int(f[1]))
					vehT[ind].append(int(f[0]))
					vehD[ind].append(int(f[3]))
			elif int(f[4])==0:
				if  not int(f[1]) in vehNr1:
					vehNr1.append(int(f[1]))
					vehT1.append([int(f[0])])
					vehD1.append([int(f[3])])
				else:
					ind=vehNr1.index(int(f[1]))
					vehT1[ind].append(int(f[0]))
					vehD1[ind].append(int(f[3]))
			else:
				if  not int(f[1]) in vehNr2:
					vehNr2.append(int(f[1]))
					vehT2.append([int(f[0])])
					vehD2.append([int(f[3])])
				else:
					ind=vehNr2.index(int(f[1]))
					vehT2[ind].append(int(f[0]))
					vehD2[ind].append(int(f[3]))				


import matplotlib.pyplot as plt
'''
for j in range(10):
	for i in range(len(vehNr)):
		if vehNr[i]%10==j:
			plt.plot(vehT[i], vehD[i], label=vehNr[i])
	plt.xlabel('Time[s]')
	plt.ylabel('Distance[ft]')
	plt.yticks((399, 600, 945, 1200, 1421, 1800, 2219), ('10th St', 600, '11th St', 1200, '12th St', 1800, '14th St'))
	plt.title('Trajectory for Through Vehicles: Sample '+str(j+1))
	plt.savefig('Traj_TR_'+str(j+1)+'.png', bbox_inches='tight', dpi=600)
	plt.clf()
	plt.close()

for i in range(len(vehNr)):
	plt.plot(vehT[i], vehD[i], label=vehNr[i])
plt.xlabel('Time[s]')
plt.ylabel('Distance[ft]')
plt.yticks((399, 600, 945, 1200, 1421, 1800, 2219), ('10th St', 600, '11th St', 1200, '12th St', 1800, '14th St'))
plt.title('Trajectory for All Through Vehicles')
plt.savefig('Traj_TR.png', bbox_inches='tight', dpi=600)
plt.clf()
plt.close()	
'''
for i in range(len(vehNr1)):
	plt.plot(vehT1[i], vehD1[i], label=vehNr1[i])
plt.xlabel('Time[s]')
plt.ylabel('Distance[ft]')
plt.yticks((250, 399, 500), (250, '10th St', 500))
plt.title('Trajectory for 10th St LT-only Vehicles')
plt.savefig('Traj_LT_10.png', bbox_inches='tight', dpi=600)
plt.clf()
plt.close()

for i in range(len(vehNr2)):
	plt.plot(vehT2[i], vehD2[i], label=vehNr2[i])
plt.xlabel('Time[s]')
plt.ylabel('Distance[ft]')
plt.yticks((1200, 1421, 1800, 2219), (1200, '12th St', 1800, '14th St'))
plt.title('Trajectory for 14th St LT-only Vehicles')
plt.savefig('Traj_LT_14.png', bbox_inches='tight', dpi=600)
plt.clf()
plt.close()

