function x = Naive_Gaussian(A,b)
n = length(b); x = zeros(n,1);
% forward-elimination
for k=1:n-1 
      for i=k+1:n
           xmult = A(i,k)/A(k,k);
           for j=k+1:n
             A(i,j) = A(i,j)-xmult*A(k,j);
           end
           b(i) = b(i)-xmult*b(k);
      end
end
 % back-substitution
x(n) = b(n)/A(n,n);
for i=n-1:-1:1
   sum = b(i);
   for j=i+1:n
     sum = sum-A(i,j)*x(j);
   end
   x(i) = sum/A(i,i);
end
end