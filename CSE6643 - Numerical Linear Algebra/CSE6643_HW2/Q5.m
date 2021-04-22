for trial=1:3
    T1=[];T2=[];T3=[];
    for n=100:100:500
        clearvars -except n T1 T2 T3 trial;
        % creating random A based on d=single value information
        [U, X] = qr(randn(n));   
        [V, X] = qr(randn(n));    
        S = diag(3.^(-1:-1:-n));  
        A = U*S*V; 

        % Classical Gram-Schmidt Algorithm
        t1=cputime;
        Q=zeros(n,n); 
        R=zeros(n,n);
        for j=1:n
            v=A(:,j);
            for i=1:j-1
                R(i,j)=Q(:,i)'*A(:,j);
                v=v-R(i,j)*Q(:,i);
            end
            R(j,j)=norm(v);
            Q(:,j)=v/R(j,j);
        end
        T1=[T1,cputime-t1];
        clearvars v;
        q=Q; r=R;

        % Modified Gram-Schmidt Algorithm
        t2=cputime;
        Q=zeros(n,n); 
        R=zeros(n,n);
        v=zeros(n,n);
        for j=1:n
            v(:,j)=A(:,j);
        end
        for j=1:n
            R(j,j)=norm(v(:,j));
            Q(:,j)=v(:,j)/R(j,j);
            for i=j+1:n
                R(j,i)=Q(:,j)'*v(:,i);
                v(:,i)=v(:,i)-R(j,i)*Q(:,j);
            end
        end
        T2=[T2,cputime-t2];
        t3=cputime;
        [Q1,R1]=Householder(A);
        T3=[T3,cputime-t3];
    end

    hold on
    f=figure('units','normalized','outerposition',[0 0 1 1]);
    plot(100:100:500,T1,'--',100:100:500,T2,100:100:500,T3,'-.');
    xlabel('Dimension n-->');
    ylabel('CPU Time-->');
    legend('Classical Gram Schmidt','Modified Gram Schmidt','Householder QR');
    title(['CPU time Comparison for Different QR: Trial ',num2str(trial)]);
    saveas(f,['CPUTime_QR',num2str(trial),'.jpg']);
    hold off
    close all
end

