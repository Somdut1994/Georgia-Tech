clear 
for lambda=0:2:2
    T=[]; N=[]; n=256;
    while (n<=1024)
        t=cputime;
        b=1; a=0;
        h=(b-a)/n;
        A=zeros(n-1);
        F=zeros(n-1,1);
        A(1,1)=2/h^2;
        A(1,2)=-h^(-2)+lambda/(2*h);
        for i=2:n-2
            A(i,i-1)=-h^(-2)-lambda/(2*h);
            A(i,i)=2/h^2;
            A(i,i+1)=-h^(-2)+lambda/(2*h);
        end
        A(n-1,n-2)=-h^(-2)-lambda/(2*h);
        A(n-1,n-1)=2/h^2;
        check=0;
        A1=A;
        EV=eye(n-1);
        while(check<(n-2)*(n-1)/2)
            [Q,R]=Householder(A);
            EV=EV*Q;
            A=R*Q;
            check=0;
            for i =1:n-1
                for j=1:i
                    if abs(A(i,j))<=10^-6
                        check=check+1;
                    end
                end
            end
        end 

        EI=zeros(n-1,1);
        for i =1:n-1
            EI(i)=A(i,i);
        end
        T=[T,cputime-t];
        N=[N,n];
        n=n*2;
    end

    hold on
    f=figure('units','normalized','outerposition',[0 0 1 1]);
    plot(N,T);
    xlabel('Dimension n-->');
    ylabel('CPU Time-->');
    title(['QR Eigenvalue Problem CPU Time vs Dimension for \lambda=',num2str(lambda)]);
    saveas(f,['CPUTime_QR_Lambda_',num2str(lambda),'.jpg']);
    hold off
    close all
end

    
        
        
        



    


