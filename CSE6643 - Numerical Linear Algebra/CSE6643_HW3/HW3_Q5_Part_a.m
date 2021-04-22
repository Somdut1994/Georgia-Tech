clear
for lambda=0:2:2
    n=256;T=[]; N=[]; CN=[];
    while (n<=1024)
        t=cputime;
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
        CN=[CN,cond(A)];
        A1=inv(A);
        v=(zeros(n-1,1)+1)/sqrt(n-1);
        L=v'*A*v; error=1;
        while(abs(error)>10^-6)
            w=A*v;
            v=w/norm(w);
            error=L-v'*A*v;
            L=v'*A*v;
        end
        v=(zeros(n-1,1)+1)/sqrt(n-1);
        l=v'*A1*v; error=1;
        while(abs(error)>10^-6)
            w=A1*v;
            v=w/norm(w);
            error=l-v'*A1*v;
            l=v'*A1*v;
        end
        l=1/l;
        T=[T,cputime-t];
        N=[N,n];
        n=n*2;
    end

    hold on
    f=figure('units','normalized','outerposition',[0 0 1 1]);
    plot(N,T);
    xlabel('Dimension n-->');
    ylabel('CPU Time-->');
    title(['Power Iteration Eigenvalue Problem CPU Time vs Dimension for \lambda=',num2str(lambda)]);
    saveas(f,['CPUTime_PI_Lambda_',num2str(lambda),'.jpg']);
    hold off
    close all

    hold on
    f=figure('units','normalized','outerposition',[0 0 1 1]);
    plot(N,CN);
    xlabel('Dimension n-->');
    ylabel('CPU Time-->');
    title(['Condition Number of A vs Dimension for \lambda=',num2str(lambda)]);
    saveas(f,['CN_A_Lambda_',num2str(lambda),'.jpg']);
    hold off
    close all
end
