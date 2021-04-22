import numpy as np
from scipy.special import lambertw
import matplotlib.pyplot as plt 

vc=50/3 # 60km/hr to m/s
v0=0
x0=0


def v_a_t(vc, v0, beta, t):
	return vc-np.exp(-beta*t)*(vc-v0), beta*np.exp(-beta*t)*(vc-v0)

def v_a_x(vc, v0, beta, x):
	A=(vc-v0+beta*x)/vc; B=(v0-vc)*np.exp(-A)/vc
	return vc*(lambertw(B)+1), -beta*vc*lambertw(B)


def VSP(a, v):
	A=.156461; B=.00200193; C=.000492646; M=1.4788
	return v*(a+A/M+B*v/M+C*v**2/M)

def CO(VSP):
	return np.exp(.051*VSP-2.664)

linestyles=['-', '--', '-']
Beta=[.06, .02, 1]

'''
## Emission vs Time
k=0
for beta in Beta:
	Em_t=[[0], [0]]

	for i in range(850):
		t=(i+1)/10.0
		v, a=v_a_t(vc, v0, beta, t)
		vsp=VSP(a, v)
		Em_t[0].append(Em_t[0][-1]+0.1)
		Em_t[1].append(Em_t[1][-1]+CO(vsp)*0.1)

	plt.plot(Em_t[0], Em_t[1], label=r'$\beta$='+str(beta), linestyle=linestyles[k])
	k+=1	

plt.legend()
plt.xlabel('time, s')
plt.ylabel('CO Emission, gr/tonne')
plt.title('CO Emission vs Time')               
plt.savefig('CO_t.png', bbox_inches='tight', dpi=600) 
plt.clf()     
plt.close() 
'''


## Emission vs Distance
k=0
for beta in Beta:
	Em_x=[[0], [0]]

	for i in range(11000):
		x=(i+1)/10.0
		v, a=v_a_x(vc, v0, beta, x)
		vsp=VSP(a, v)
		Em_x[0].append(Em_x[0][-1]+0.1)
		Em_x[1].append(Em_x[1][-1]+CO(vsp)*0.1/v)	

	plt.plot(Em_x[0], Em_x[1], label=r'$\beta$='+str(beta), linestyle=linestyles[k])
	k+=1	

plt.legend()
plt.xlabel('distance, m')
plt.ylabel('CO Emission, gr/tonne')
plt.title('CO Emission vs  Distance')               
plt.savefig('CO_x.png', bbox_inches='tight', dpi=600) 
plt.clf()     
plt.close() 






