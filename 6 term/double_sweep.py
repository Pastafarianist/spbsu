from __future__ import division
import numpy as np

def sweep(A, B, C, G):
	n = len(G) - 1
	s = np.empty(n + 1, dtype=np.float)
	t = np.empty(n + 1, dtype=np.float)
	s[0] = C[0] / B[0]
	t[0] = -G[0] / B[0]

	for i in xrange(1, n + 1):
		s[i] = C[i] / (B[i] - A[i] * s[i - 1])
		t[i] = (A[i] * t[i - 1] - G[i]) / (B[i] - A[i] * s[i - 1])

	y = np.empty(n + 1, dtype=np.float)
	y[n] = t[n]

	for i in xrange(n - 1, -1, -1):
		y[i] = s[i] * y[i + 1] + t[i]

	return s, t, y

def make_coefficients(p, q, r, f, a, b, n, prec, alphas, betas):
	num_points = n + 1 + (prec - 1)

	A = np.zeros(num_points, dtype=np.float)
	B = np.zeros(num_points, dtype=np.float)
	C = np.zeros(num_points, dtype=np.float)
	G = np.zeros(num_points, dtype=np.float)

	h = (b - a) / n

	if prec == 1:
		xs = np.arange(0, num_points) * h + a
		
		B[0] = -(alphas[1] + alphas[2] / h)
		C[0] = -(alphas[2] / h)
		G[0] = alphas[0]

		A[-1] = -(betas[2] / h)
		B[-1] = -(betas[1] + betas[2] / h)
		G[-1] = betas[0]

	elif prec == 2:
		xs = np.arange(0, num_points) * h + a - h / 2

		B[0] = -(alphas[1] / 2 + alphas[2] / h)
		C[0] = (alphas[1] / 2 - alphas[2] / h)
		G[0] = alphas[0]

		A[-1] = (betas[1] / 2 - betas[2] / h)
		B[-1] = -(betas[1] / 2 + betas[2] / h)
		G[-1] = betas[0]

	for i in xrange(1, num_points - 1):
		G[i] = f(xs[i])
		A[i] = -p(xs[i]) / h**2 + q(xs[i]) / (2*h)
		B[i] = -((2*p(xs[i]) / h**2 + r(xs[i])))
		C[i] = A[i]

	return xs, A, B, C, G

n = 10
a, b = -1, 1

p = lambda x: (x - 2) / (x + 2)
q = lambda x: x
r = lambda x: 1 - np.sin(x)
f = lambda x: x**2

alphas = 0, 1, 0 # al1 y(a) - al2 y(b) = alpha
betas  = 0, 1, 0 # be1 y(a) + be2 y(b) = beta

prec = 2

xs, A, B, C, G = make_coefficients(p, q, r, f, a, b, n, prec, alphas, betas)
S, T, Y = sweep(A, B, C, G)

print(''.join('%12s' % s for s in ('xabcgsty')))
for vals in zip(xs, A, B, C, G, S, T, Y):
	print ''.join('%12.5f' % v for v in vals)
