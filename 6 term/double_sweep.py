from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

def sweep(A, B, C, G):
	n = len(G) - 1
	S = np.empty(n + 1)
	T = np.empty(n + 1)
	Y = np.empty(n + 1)
	
	S[0] = C[0] / B[0]
	T[0] = -G[0] / B[0]

	for i in xrange(1, n + 1):
		denom = B[i] - A[i] * S[i - 1]
		S[i] = C[i] / denom
		T[i] = (A[i] * T[i - 1] - G[i]) / denom

	Y[n] = T[n]

	for i in xrange(n - 1, -1, -1):
		Y[i] = S[i] * Y[i + 1] + T[i]

	for i, (a, b, c, g) in enumerate(zip(A, B, C, G)):
		ss = - b * Y[i] - g
		if i >= 1:
			ss += a * Y[i - 1]
		if i <= len(Y) - 2:
			ss += c * Y[i + 1]
		if abs(ss) > 1e-8:
			print 'Failure at i=%d: %.4f' % (i, ss)

	return S, T, Y

def make_coefficients(p, q, r, f, a, b, alphas, betas, n, prec):
	num_points = (n + 1) + (1 if prec == 2 else 0)
	h = (b - a) / n

	A = np.zeros(num_points)
	B = np.zeros(num_points)
	C = np.zeros(num_points)
	G = np.zeros(num_points)

	if prec == 1:
		xs = np.linspace(a, b, num_points)
		
		B[0] = -(alphas[1] + alphas[2] / h)
		C[0] = -(alphas[2] / h)
		G[0] = alphas[0]

		A[-1] = -(betas[2] / h)
		B[-1] = -(betas[1] + betas[2] / h)
		G[-1] = betas[0]

	elif prec == 2:
		xs = np.linspace(a - h / 2, b + h / 2, num_points)

		B[0] = -(alphas[1] / 2 + alphas[2] / h)
		C[0] = (alphas[1] / 2 - alphas[2] / h)
		G[0] = alphas[0]

		A[-1] = (betas[1] / 2 - betas[2] / h)
		B[-1] = -(betas[1] / 2 + betas[2] / h)
		G[-1] = betas[0]

	# print(B[0], C[0], G[0])
	# print(A[-1], B[-1], G[-1])

	for i in xrange(1, num_points - 1):
		G[i] = f(xs[i])
		A[i] = -p(xs[i]) / h**2 - q(xs[i]) / (2*h)
		B[i] = -(2*p(xs[i]) / h**2 + r(xs[i]))
		C[i] = -p(xs[i]) / h**2 + q(xs[i]) / (2*h)

	return xs, A, B, C, G

def plot_for(p, q, r, f, a, b, alphas, betas, exact, n, prec, refine, color):
	xs, A, B, C, G = make_coefficients(p, q, r, f, a, b, alphas, betas, n, prec)
	S, T, Y = sweep(A, B, C, G)

	if prec == 2:
		# moving to the original grid
		xs = np.linspace(a, b, n + 1)
		Y = (Y[1:] + Y[:-1]) / 2

	# if refine:
	# 	error = 

	exact_y = exact[1][::((len(exact[1]) - 1) // (len(Y) - 1))]

	print('Solution with n=%d nodes and precision O(h^%d)' % (n, prec))
	print(''.join('%12s' % s for s in ('xabcgstye')))
	for vals in zip(xs, A, B, C, G, S, T, Y, exact_y):
		print ''.join('%12.5f' % v for v in vals)

	plt.plot(xs, Y, color=color)


a, b = -1, 1

p = lambda x: - (4 + x) / (5 + 2*x)
q = lambda x: (1 - x / 2)
r = lambda x: 1 + np.exp(x / 2)
f = lambda x: 2 + x

alphas = 0, 0, -1 # a1 y(a) - a2 y(b) = a0
betas  = 0, 2, 1  # b1 y(a) + b2 y(b) = b0

exact_x = np.linspace(a, b, 21)
exact_y = [
	0.792652687899232,
	0.793975084414089,
	0.797749914679873,
	0.803657498604232,
	0.811334431253817,
	0.820370146741282,
	0.830302096587725,
	0.840609228831236,
	0.850703312815609,
	0.859917430959906,
	0.867490798166806,
	0.872548887919095,
	0.874077624353127,
	0.870889750233535,
	0.861581531576143,
	0.844476987975402,
	0.817556181903231,
	0.778363536462625,
	0.723890317314835,
	0.650424585398997,
	0.553359085653240
]
exact = (exact_x, exact_y)
plt.plot(exact_x, exact_y, color='r')

plot_for(p, q, r, f, a, b, alphas, betas, exact, n=10, prec=1, refine=False, color='b')
plot_for(p, q, r, f, a, b, alphas, betas, exact, n=20, prec=1, refine=True, color='g')
plot_for(p, q, r, f, a, b, alphas, betas, exact, n=10, prec=2, refine=False, color='c')
plot_for(p, q, r, f, a, b, alphas, betas, exact, n=20, prec=2, refine=True, color='m')

plt.show()
