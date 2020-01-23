from random import random

#define a class called 'Client'
class Client:
	def __init__(self,entry_date,arrival_date,service_start_date,service_time):
		self.entry_date=entry_date
		self.arrival_date=arrival_date
		self.service_start_date=service_start_date
		self.service_time=service_time
		self.service_end_date=self.service_start_date+self.service_time
		self.wait=self.service_start_date-self.arrival_date


def Event_QSim(FEL, ServerInfo):

	#Initialise empty list to hold all data
	Clients=[]

	#Simulation Code:
	while len(FEL)>0:

		#calculate arrival date and service time for new customer
		entry_date=FEL[0][0]
		if len(Clients)==0:
			arrival_date=FEL[0][0]+FEL[0][2]
			service_start_date=arrival_date
		else:
			arrival_date=max(FEL[0][0]+FEL[0][2], arrival_date)
			service_start_date=max(arrival_date,Clients[-1].service_end_date)
		timeblock=(service_start_date-ServerInfo[0]) %(ServerInfo[1]+ServerInfo[2])
		if timeblock>=ServerInfo[1]:
			service_start_date+=(ServerInfo[1]+ServerInfo[2]-timeblock)
		service_time=ServerInfo[3]+(ServerInfo[4]-ServerInfo[3])*random()

		#create new customer
		Clients.append(Client(entry_date,arrival_date,service_start_date,service_time))

		#dequeue from FEL
		FEL.pop(0)


	return Clients
