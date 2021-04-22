clear
lambda=2;
% lambda=0;
MatrixSize=[200;400;800;1000;2000;4000;8000];
T=[];
% real solution
syms u(x)
uSol(x)=dsolve(-diff(u,x,2)+lambda*u==3*x-.5,[u(0)==0 u(1)==-2]);
uSol=simplify(uSol);
for N=1:size(MatrixSize)
    initime = cputime;
    %initializing 
    n=MatrixSize(N);
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

    U=Naive_Gaussian(A,F);
    for i=1:n-1
        U1(i,1)=double(uSol(i*h));
    end
    fintime = cputime;
    T=[T,fintime-initime];
    X=(a+h:h:b-h)';
    hold on
    f=figure('units','normalized','outerposition',[0 0 1 1]);
    plot(X,U,'ro',X,U1,'bx');
    legend('U: FD','U: Real');
    xlabel('x-->');
    title(['Comparative Study for n = ',num2str(n),' and \lambda = ',num2str(lambda)]);
    saveas(f,['U_Lambda_',num2str(lambda),'_n_',num2str(n),'.jpg']);
    hold off
    close all
end
f=figure('units','normalized','outerposition',[0 0 1 1]);
plot(MatrixSize,T);
xlabel('n-->');
ylabel('CPU Time-->');
title(['CPU time Study for \lambda = ',num2str(lambda)]);
saveas(f,['Time_Lambda_',num2str(lambda),'.jpg']);
hold off
close all

    
   