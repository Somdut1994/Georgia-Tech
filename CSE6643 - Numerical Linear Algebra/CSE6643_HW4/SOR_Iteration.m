function x = SOR_Iteration(A,b,w)
    n = length(b);
    tol = 1e-6;
    D = diag(diag(A));
    U = triu(A-D);
    L = tril(A-D);
    x = rand(n,1);
    x_old = zeros(n,1);
    while norm(x_old-x)>tol
        x_old = x;
        x = (inv(D+w*L))*(((1-w)*D-w*U)*x +w*b);
    end
end