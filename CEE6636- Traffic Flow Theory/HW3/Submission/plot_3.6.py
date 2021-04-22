import matplotlib.pyplot as plt 

plt.plot([0, .5, 2], [0, 5000, 8000], color='green', label='A(t)')
plt.plot([0, 2], [0, 8000], color='blue', label='D(t)= UO Solution')

x=[]; y=[]
a=2; b=8000; rate=4000
for i in range(23):
    x.append(a); y.append(b)
    a-=1/48; b-=rate/48
    rate+=1000
x.append(a); y.append(b)
plt.plot(x, y, label='D(t)= SO: Initial Trend Line', color='orange', linestyle='--')


k=1.45; n=4
x=[2]; y=[8000]
a=2-k; b=8000-2000*k; rate=4000
for i in range(n):
    x.append(a); y.append(b)
    a-=1/48; b-=rate/48
    rate+=1000
x.append(a); y.append(b)
x.append(0); y.append(0)
plt.plot(x, y, label='D(t)= SO: Final Trial & Error Solution', color='red', linestyle='--')

plt.legend()
plt.xlabel('t(hr)')
plt.ylabel('#')
plt.title('Trial and Error Method to solve SO')
plt.show()
