import matplotlib.pyplot as plt 

def At(t):
	if t<.16:
		return 7000
	else:
		return 5000

def Dt(t):
	if t<.04:
		return 0
	elif t<.32:
		return 3000
	else:
		return 6000

A=[[0], [0]]
D=[[0], [0]]
tshiftU=(2-0)/100
FU=[[tshiftU], [0]]
tshiftD=(4-2)/20; NshiftD=600*(4-2)
FD=[[tshiftD], [NshiftD]] 

for i in range(10000):
	t=(i+1)/10000
	ra, rd=At(t), Dt(t)
	A[0].append(t)
	A[1].append(A[1][-1]+.0001*ra)
	D[0].append(t)
	D[1].append(D[1][-1]+.0001*rd)
	tu=t+tshiftU
	if tu<1:
		FU[0].append(tu)
		FU[1].append(A[1][i+1])
	td=t+tshiftD
	Nd=D[1][i+1]+NshiftD
	if td<1:
		FD[0].append(td)
		FD[1].append(Nd)


from bisect import bisect

iU1=bisect(FU[0], .2776)
iD1=bisect(FD[0], .2776)

iU2=bisect(FU[0], .6995)
iD2=bisect(FD[0], .6995)




plt.plot(A[0], A[1], color='blue', label='A(t)')
plt.plot(D[0], D[1], color='orange', label='D(t)')
plt.plot(FU[0][:iU1]+FD[0][iD1:iD2]+FU[0][iU2:], FU[1][:iU1]+FD[1][iD1:iD2]+FU[1][iU2:], color='darkgrey', linewidth=3, label='N(t, $x_{0}$)')
plt.plot(FU[0], FU[1], color='blue', linestyle='--', label='f($t_{U}$)=V(t)')
plt.plot(FD[0], FD[1], color='orange', linestyle='--', label='f($t_{D}$)')
plt.xlabel('time, hr')
plt.ylabel('veh #')
plt.legend()
plt.plot([.2776, .2776], [0, FU[1][iU1]], color='green', linewidth=3, linestyle='--')
plt.plot([.6995, .6995], [0, FU[1][iU2]], color='green', linewidth=3, linestyle='--')
plt.ylim([0, 6000])
plt.savefig('plot_comparison.png', dpi=600)
plt.clf()
plt.close()
