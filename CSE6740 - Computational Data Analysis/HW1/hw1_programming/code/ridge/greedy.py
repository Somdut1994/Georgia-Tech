import numpy as np

def greedy (X, y, K):
	A=[]; beta=[]
	beta=np.matrix(np.zeros((np.shape(X)[1], 1)))
	for k in range(1,K+1):
		i_exp=np.linalg.det(np.transpose(X[:,0])*(X*beta-y))
		flag=0
		for j in range(1,np.shape(X)[1]):
			j_exp=np.linalg.det(np.transpose(X[:,j])*(X*beta-y))
			if j_exp>i_exp:
				i_exp=j_exp
				flag=j
		if not flag in A:
			A.append(flag)
			A.sort()
			N=len(A)    
			matrix1=[]; matrix2=[]
			for i in range(N):
				matrix2.append([(np.transpose(y)*X[:,A[i]])[0,0]])
				mat=[]
				for j in range(N):
					mat.append((np.transpose(X[:,A[j]])*X[:,A[i]])[0,0])
				matrix1.append(mat)
			matrix1=np.matrix(matrix1); matrix2=np.matrix(matrix2)
			beta1=np.linalg.inv(matrix1)*matrix2
			beta=np.matrix(np.zeros((np.shape(X)[1], 1)))
			for i in range(N):
				beta[A[i],0]=beta1[i,0]
	return A, beta

m=0; X=[]; y=[]
with open('train-matrix.txt') as file:
	for line in file:
		m+=1
		if m>2:
			f=line.split('\n')[0]
			f=[float(x) for x in f.split()]
			if len(f)>1:
				X.append(f)
			else:
				y.append(f)

X=np.matrix(X); y=np.matrix(y); K=6

print greedy (X, y, K)
