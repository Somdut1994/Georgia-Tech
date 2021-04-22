A=[1 2 3;6 5 4;3 4 8;2 -1 6];
[U, S, V ] = svd(A);
S = diag(S);
tol = max(size(A))*eps;
r = sum(S > tol);
S = diag(ones(r, 1)./S(1 : r));
X = V (:, 1 : r) * S * U(:, 1 : r)';
