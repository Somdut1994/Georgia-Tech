clear
T=[];
N=[];
n=100;
while n<=800
    A=rand(n)*10-5;
    for i=1:n
        for j=1:n
            if (i>1 && i>2 && j>i)||(i>1 && i>2 && j>i)
                A(i,j)=0;
            end
        end
    end
    t=cputime;
    [Q,R]=QR_GR(A);
    T=[T,cputime-t];
    N=[N,n];
    n=n*2;
end

hold on
f=figure('units','normalized','outerposition',[0 0 1 1]);
plot(N,T);
xlabel('Dimension n-->');
ylabel('CPU Time-->');
title('Givens Rotation CPU Time vs Dimension');
saveas(f,'CPUTime_GR.jpg');
hold off
close all
            