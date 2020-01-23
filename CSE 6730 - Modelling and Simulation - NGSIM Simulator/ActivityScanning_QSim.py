__metaclass__=type
from random import random



def Activity_QSim(B_list, ServerInfo):
	#intitialize time
	T=0
	l=len(B_list)
	RecordedActivities=[]

	#simulation starts here
	while len(B_list)>0:
		#setting current time to the oldest B-event time-stamp
		T=B_list[0][0]
		t_max=B_list[0][0]
		if B_list[0][2]=='arrival':
			RecordedActivities.append(B_list[0])
			for j in B_list:
				if B_list[0][1]==j[1] and j[2]=='waitTill':
					# removing wait events to avoid redundant steps
					try:
						B_list.remove(j)
					except ValueError:
						pass
					t_max=j[0]
			timeblock=(t_max-ServerInfo[0]) %(ServerInfo[1]+ServerInfo[2])
			t=t_max+(ServerInfo[1]+ServerInfo[2]-timeblock)*(timeblock>=ServerInfo[1])
			t1=t+ServerInfo[3]+(ServerInfo[4]-ServerInfo[3])*random()

			# Future Events schedule by C-event that checks for next active Server time
			B_list.append([t, B_list[0][1], 'GotGreen'])
			B_list.append([t1, B_list[0][1], 'Passed'])
			for j in range(B_list[0][1]+1, l+1):
				B_list.append([t1, j, 'waitTill'])

		elif B_list[0][2]!='waitTill':
			RecordedActivities.append(B_list[0])
		
		# dequeue the oldest event after implementing
		B_list.pop(0)
		B_list=sorted(B_list, key=lambda x: x[0])


	return RecordedActivities
