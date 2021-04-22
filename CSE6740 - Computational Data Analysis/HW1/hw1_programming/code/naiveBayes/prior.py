import numpy as np
from scipy.io import loadmat as lm

def prior(yTrain):
	classes=[]; prob=[]
	N=np.shape(yTrain)[0]
	for i in range(N):
		if not yTrain[i,0] in classes:
			classes.append(yTrain[i,0])
			prob.append(1.0/N)
		else:
			prob[classes.index(yTrain[i,0])]+=1.0/N

	#print prob
	c=len(classes)
	for i in range(c):
		for j in range(c-i-1):
			if classes[j]>classes[j+1]:
				classes[j], classes[j+1], prob[j], prob[j+1]=classes[j+1], classes[j], prob[j+1], prob[j]
	p=np.transpose(np.matrix(prob))
	#return classes, prob, p
	return p

# yTrain=lm('ecoli.mat')['yTrain']
# print prior(yTrain)