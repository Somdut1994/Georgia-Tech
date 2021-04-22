import numpy as np

#question 3, part (a)
x=[94,96,94,95,104,106,108,113,115,121,131]
y=[.47,.75,.83,.98,1.18,1.29,1.4,1.6,1.75,1.9,2.23]
cov_mat=np.cov(x,y)
w1=cov_mat[0][1]/cov_mat[0][0]
w0=np.average(y)-w1*np.average(x)
N=len(x)
print w0, w1
sigma_sq=np.sum([(y[i]-w1*x[i]-w0)**2 for i in range(N)])/(N-2)
print sigma_sq

#question 3, part (c)
#using equations derived in 7.6.1 of textbook
w1_var=sigma_sq/(sigma_sq+N*cov_mat[0][0])
w1_mean=w1_var*w0+w1_var*cov_mat[0][1]*N/sigma_sq
print w1_mean, w1_var

#question 3, part (d)
# +/- 1.96 for 95% confidence interval
low_bound, high_bound=w1_mean-1.96*w1_var**.5, w1_mean+1.96*w1_var**.5
print "confidence interval =["+str(low_bound)+', '+str(high_bound)+']'