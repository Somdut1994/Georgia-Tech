clear 
tol=1e-3;
w=0.5;
fileID = fopen('ResultPrecision_Q4.txt','w');
for mu=-5:10:5
    T1=[]; T2=[]; T3=[]; M=[];
    m=100;
    while m<=800
        r=[10,3,2,1];
        for i=5:m
            r=[r,0];
        end
        A=toeplitz(r);
        A=A+mu*eye(m);
        b=rand(m,1);
        x_actual=A\b;
        t1=cputime;
        x=J_Iteration(A,b);
        T1=[T1,cputime-t1];
        if(norm(x-x_actual)<tol)
            fprintf(fileID,['Jacobian Iteration gives accurate result for m = ',num2str(m),' and mu = ',num2str(mu),'\n']);
        else
            fprintf(fileID,['Jacobian Iteration does not give accurate result for m = ',num2str(m),' and mu = ',num2str(mu),'\n']);
        end
        t2=cputime;
        x=GS_Iteration(A,b);
        T2=[T2,cputime-t2];
        if(norm(x-x_actual)<tol)
            fprintf(fileID,['Gauss Seidel Iteration gives accurate result for m = ',num2str(m),' and mu = ',num2str(mu),'\n']);
        else
            fprintf(fileID,['Gauss Seidel Iteration does not give accurate result for m = ',num2str(m),' and mu = ',num2str(mu),'\n']);
        end        
        t3=cputime;
        x=SOR_Iteration(A,b,w);
        T3=[T3,cputime-t3];
        if(norm(x-x_actual)<tol)
            fprintf(fileID,['SOR Iteration gives accurate result for m = ',num2str(m),' and mu = ',num2str(mu),'\n']);
        else
            fprintf(fileID,['SOR Iteration does not give accurate result for m = ',num2str(m),' and mu = ',num2str(mu),'\n']);
        end          
        M=[M,m];
        m=m*2;
    end
    hold on
    f=figure('units','normalized','outerposition',[0 0 1 1]);
    plot(M,T1,'--',M,T2,':',M,T3);
    xlabel('Dimension m-->');
    ylabel('CPU Time-->');
    legend('Jacobian Iteration','Gauss Seidel Iteration','SOR Iteration');
    title(['CPU time Comparison for Different Iterative methods for \mu = ',num2str(mu)]);
    saveas(f,['CPUTime_Iteration_mu_',num2str(mu),'.jpg']);
    hold off
    close all        
end
fclose(fileID);