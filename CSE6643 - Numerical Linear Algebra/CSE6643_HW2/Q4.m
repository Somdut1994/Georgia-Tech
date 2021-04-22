clear 
T1=[]; T2=[];
for m=100:100:1000
    r=[10,3,2,1];
    if m>4
        for i=4:m
            r=[r,0];
        end
    end
    A=toeplitz(r);
    t1=cputime;
    [Q,R]=Householder(A);
    T1=[T1,cputime-t1];
    t2=cputime;
    [Q1,R1]=HH_Band(A,3,3);
    T2=[T2,cputime-t2];
end

hold on
f=figure('units','normalized','outerposition',[0 0 1 1]);
plot(100:100:1000,T1,'--',100:100:1000,T2);
xlabel('Dimension m-->');
ylabel('CPU Time-->');
legend('Normal Householder','Householder for Band Matrix');
title('CPU time Comparison for Householder QR');
saveas(f,'CPUTime_HH.jpg');
hold off
close all


    