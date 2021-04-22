import numpy as np

def flow(v):
	return 9800*v/(v+20)


s = np.random.uniform(40,80,10000000)

flows=[]
for v in s:
	flows.append(flow(v))

print(np.mean(flows), np.std(flows, ddof=1))	
