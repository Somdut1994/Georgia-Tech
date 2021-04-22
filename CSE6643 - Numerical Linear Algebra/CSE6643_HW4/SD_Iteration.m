function x = SD_Iteration(A,b)
    n = length(b);
    tol = 1e-6;
    x = rand(n,1);
    x_old = zeros(n,1);
    while norm(x_old-x)>tol
        x_old = x;
        p = b-A*x;
        alpha = (p'*p)/(p'*A*p);
        x = x + alpha*p;
    end
end