import numpy as np 
from scipy.io import loadmat as lm
from prior import *

def likelihood (xTrain, yTrain):
	(n,m)=np.shape(xTrain)
	p=prior(yTrain)
	values=[]; c=np.shape(p)[0]
	for i in range(m):
		dum=[]
		for j in range(c):
			dum.append([])
		values.append(dum)
	for k in range(n):
		for i in range(m):
			values[i][yTrain[k,0]-1].append(xTrain[k,i])

	M=np.matrix(np.zeros((m,c))); V=np.matrix(np.zeros((m,c)))
	
	for i in range(m):
		for j in range(c):
			(M[i,j], V[i,j])=(np.average(values[i][j]),np.var(values[i][j]))

	#return classes, M, V
	return M, V

# xTrain=lm('ecoli.mat')['xTrain']
# yTrain=lm('ecoli.mat')['yTrain']
# print likelihood (xTrain, yTrain)