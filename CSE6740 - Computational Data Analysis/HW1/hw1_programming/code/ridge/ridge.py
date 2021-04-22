import numpy as np

def ridge (X, y, Lambda):
	(n,m)=np.shape(X) 
	matrix1=[]; matrix2=[]
	for i in range(m):
		matrix2.append([(np.transpose(y)*X[:,i])[0,0]/n])
		mat=[]
		for j in range(m):
			mat.append((np.transpose(X[:,j])*X[:,i])[0,0]/n)
		mat[i]+=2*Lambda
		matrix1.append(mat)
	matrix1=np.matrix(matrix1); matrix2=np.matrix(matrix2)
	beta=np.linalg.inv(matrix1)*matrix2
	return beta

def ten_fold (X, y, Lambdas):
	error=1000000
	(n,m)=np.shape(X)
	n_10=int(n/10)
	for L in Lambdas:
		err=0.0
		for i in range(0,n,n_10):
			a=X[0:i,:]; b=X[i+n_10:n,:]; X_train=np.concatenate((a, b), axis=0)
			a=y[0:i,:]; b=y[i+n_10:n,:]; y_train=np.concatenate((a, b), axis=0)
			X_test=X[i:i+n_10,:]; y_test=y[i:i+n_10,:]
			beta1=ridge (X_train, y_train, L)
			err_mat=y_test-X_test*beta1
			err+=np.linalg.norm(err_mat)**2/(10*n_10)
		print (L,err**.5)
		if err<error:
			error=err
			beta=ridge (X, y, L)
			Lambda=L
	return beta, Lambda


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

X_train=np.matrix(X); y_train=np.matrix(y); Lambdas=[0.0125,0.025,0.05,0.1,0.2]

beta,Lambda=ten_fold (X_train, y_train, Lambdas)
print beta, Lambda

m=0; X=[]; y=[]
with open('test-matrix.txt') as file:
	for line in file:
		m+=1
		if m>2:
			f=line.split('\n')[0]
			f=[float(x) for x in f.split()]
			if len(f)>1:
				X.append(f)
			else:
				y.append(f) 

X_test=np.matrix(X); y_test=np.matrix(y)
error_matrix=y_test-X_test*beta
error=(np.linalg.norm(error_matrix)**2/np.shape(beta)[0])**.5

m=0; beta_star=[]
with open('true-beta.txt') as file:
	for line in file:
		m+=1
		if m>1:
			f=line.split('\n')[0]
			f=[float(x) for x in f.split()]
			beta_star.append(f)		
			
beta_2_norm=np.linalg.norm(beta-np.matrix(beta_star))

print "Prediction error on test-matrix is "+str(error)
print "2-norm squared of beta error is "+str(beta_2_norm**2)

