clear
lambda=0;
T1=[];T2=[];M=[];n=100;
while n<=1600
    b=1; a=0;
    h=(b-a)/n;
    A=zeros(n-1);
    F=zeros(n-1,1);
    A(1,1)=2/h^2;
    A(1,2)=-h^(-2)+lambda/(2*h);
    F(1)=3*h-.5;
    for i=2:n-2
        A(i,i-1)=-h^(-2)-lambda/(2*h);
        A(i,i)=2/h^2;
        A(i,i+1)=-h^(-2)+lambda/(2*h);
        F(i)=3*i*h-.5;
    end
    A(n-1,n-2)=-h^(-2)-lambda/(2*h);
    A(n-1,n-1)=2/h^2;
    F(n-1)=3*(n-1)*h-.5-(-2)*(-h^(-2)+lambda/(2*h));
    t1=cputime;
    X=SD_Iteration(A,F);
    T1=[T1,cputime-t1];
    t2=cputime;
    X=CG_Iteration(A,F);
    T2=[T2,cputime-t2];
    M=[M,n];
    n=n*2;
end
f=figure('units','normalized','outerposition',[0 0 1 1]);
plot(M,T1,'--',M,T2,'-');
xlabel('Dimension n-->');
ylabel('CPU Time-->');
legend('Steepest Descent Method','Conjugate Gradient Method');
title(['CPU time Comparison for Different methods for \lambda = ',num2str(lambda)]);
saveas(f,['1_CPUTime_Q5_lambda_',num2str(lambda),'.jpg']);
hold off
close all 