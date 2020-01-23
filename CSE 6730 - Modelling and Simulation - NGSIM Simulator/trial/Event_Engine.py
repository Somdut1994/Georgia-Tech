from random import random

def getColor(t, ServerInfo):
	cycle_time=(t-ServerInfo[0])%(ServerInfo[1]+ServerInfo[2])
	if cycle_time<ServerInfo[1]:
		return 'Go'
	else:
		return 'No-Go'

def Event_QSim(FEL, ServerInfo):
	queue=[]
	ProcessedLog=[]
	signal='No-Go'
	t=0
	#Simulation Code:
	while len(FEL)>0:
		if FEL[0][1]=='Signal':
			if FEL[0][2]=='No-Go':
				signal='No-Go'
			else:
				signal='Go'
				q1=queue[:]
				for i in range(len(q1)):
					serve_time=ServerInfo[3]+(ServerInfo[4]-ServerInfo[3])*random()
					if i==0:
						t=FEL[0][0]+serve_time
						FEL.append([t, q1[0], 'departure', serve_time])
						queue.pop(0)
					else:
						if getColor(t, ServerInfo)=='Go':
							t+=serve_time
							FEL.append([t, q1[i], 'departure', serve_time])
							queue.pop(0)
						else:
							break

		elif FEL[0][2]=='arrival':
			ProcessedLog.append(FEL[0])
			if signal=='Go':
				serve_time=ServerInfo[3]+(ServerInfo[4]-ServerInfo[3])*random()
				t=max(FEL[0][0],t)+serve_time
				FEL.append([t, FEL[0][1], 'departure', serve_time])
			else:
				queue.append(FEL[0][1])
		else:
			ProcessedLog.append(FEL[0])

		FEL.pop(0)
		FEL.sort(key=lambda x: x[0])

	return ProcessedLog
