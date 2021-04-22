 function x = CG_Iteration(A, b)
    n = length(b);
    tol = 1e-6;
    x = rand(n,1);
    x_old = zeros(n,1);
    r = b - A*x;
    p = r;         
    rho = r'*r;
    while norm(x_old-x)>tol
        x_old = x;
        a = A*p;
        alpha = rho/(a'*p);
        x = x + alpha*p;
        r = r - alpha*a;
        rho_new = r'*r;
        p = r + rho_new/rho * p;
        rho = rho_new;
    end
end