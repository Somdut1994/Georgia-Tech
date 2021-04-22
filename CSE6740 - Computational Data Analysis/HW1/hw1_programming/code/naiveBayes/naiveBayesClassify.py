import numpy as np
from scipy.io import loadmat as lm
import matplotlib.pyplot as plt
from prior import *
from likelihood import *

def naiveBayesClassify(xTest, M, V, p):
	(N,m)=np.shape(xTest)
	c=np.shape(p)[0]
	classifier=[]
	for i in range(N):
		max_weight=0
		for j in range(c):
			weight=p[j,0]
			for k in range(m):
				weight*=np.exp(-(xTest[i,k]-M[k,j])**2/(2*V[k,j]))/V[k,j]**.5
			if weight>max_weight:
				#print weight, j
				max_weight=weight
				flag=j
		classifier.append([flag+1])
	nb=np.matrix(classifier)
	return nb


xTrain=lm('ecoli.mat')['xTrain']
yTrain=lm('ecoli.mat')['yTrain']
xTest=lm('ecoli.mat')['xTest']
yTest=lm('ecoli.mat')['yTest']
p=prior(yTrain)
M,V=likelihood (xTrain, yTrain)
c=np.shape(p)[0]
y_predicted=naiveBayesClassify(xTest, M, V, p)
error=yTest-y_predicted
N=np.shape(xTest)[0]

TP=[]; FP=[]; FN=[]
for i in range(c):
	TP.append(0); FP.append(0); FN.append(0)

for i in range(N):
	if y_predicted[i,0]==yTest[i,0]:
		TP[y_predicted[i,0]-1]+=1.0
	else:
		FP[y_predicted[i,0]-1]+=1.0
		FN[yTest[i,0]-1]+=1.0

precision=[]; recall=[]
# print TP, FP, FN, N
for i in range(c):
	precision.append(TP[i]/(TP[i]+FP[i]))
	recall.append(TP[i]/(TP[i]+FN[i]))

print np.sum(TP)/N
print precision[0]
print recall[0]
print precision[4]
print recall[4]
