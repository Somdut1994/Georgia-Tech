function [Q,R] = Householder(A)
    n= size(A,1);
    Q = eye(n);
    R = A;
    for j = 1:n
        normx = norm(R(j:end,j));
        s = -sign(R(j,j));
        u1 = R(j,j) - s*normx;
        e = R(j:end,j)/u1; e(1) = 1;
        tau = -s*u1/normx;
        R(j:end,:) = R(j:end,:)-(tau*e)*(e'*R(j:end,:));
        % forming Q
        Q(:,j:end) = Q(:,j:end)-(Q(:,j:end)*e)*(tau*e)';
    end
end
