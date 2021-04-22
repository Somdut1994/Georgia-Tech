clear
GTID=903241855;
Norm=[];
Ratio=[];
Cond=[];
for m=100:100:6000
    A=normrnd(0,sqrt(m),m,m);
    N_2=max(abs(eig(A'*A)));
    N_i=0;
    for i=1:m
        sum=0;
        for j=1:m
            sum=sum+abs(A(i,j));
        end
        if N_i<sum
            N_i=sum;
        end
    end
    N_1=0;
    for j=1:m
        sum=0;
        for i=1:m
            sum=sum+abs(A(i,j));
        end
        if N_1<sum
            N_1=sum;
        end
    end
    Norm=[Norm;[N_1 N_2 N_i]];
    Ratio=[Ratio,N_2/N_i];
    Cond=[Cond,cond(A,1)];
end

csvwrite('NormList.csv',Norm)
csvwrite('2norm_infnorm_ratioList.csv',Ratio)
csvwrite('ConditionNumberList.csv',Cond)

f=figure('units','normalized','outerposition',[0 0 1 1]);
plot(100:100:6000,Ratio);
xlabel('m-->');
ylabel('Ratio-->');
title('Ratio of 2-norm and infinite norm');
saveas(f,'Ratio_m.jpg');
close all

f=figure('units','normalized','outerposition',[0 0 1 1]);
plot(100:100:6000,Cond);
xlabel('m-->');
ylabel('1-norm Condition Number-->');
title('1-norm Condition Number versus m');
saveas(f,'ConditionNumber_m.jpg');
close all
figure;
 