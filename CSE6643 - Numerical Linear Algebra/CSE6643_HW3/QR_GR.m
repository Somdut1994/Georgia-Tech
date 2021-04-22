function [Q,R] = QR_GR(A)
  n = size(A,1);
  Q = eye(n);
  R = A;
  for j = 1:n
    for i = n:-1:(j+1)
      G = eye(n);
      [c,s] = GR( R(i-1,j),R(i,j) );
      G([i-1, i],[i-1, i]) = [c -s; s c];
      R = G'*R;
      Q = Q*G;
    end
  end
end
