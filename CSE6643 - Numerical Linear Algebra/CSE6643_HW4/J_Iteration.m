function x = J_Iteration(A,b)
    n = length(b);
    tol = 1e-6;
    x = rand(n,1);
    x_old = zeros(n,1);
    while norm(x-x_old) > tol
        x_old = x;
        for i=1:n
            sigma = 0;
            for j=1:n
                if i~=j
                    sigma = sigma+A(i,j)*x_old(j);
                end
            end
            x(i) = (b(i)-sigma)/A(i,i);
        end
    end
end