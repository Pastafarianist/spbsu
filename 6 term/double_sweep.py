from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

def sweep(A, B, C, D):
	B = -B

	n = len(D) - 1
	S = np.empty(n + 1)
	T = np.empty(n + 1)
	Y = np.empty(n + 1)
	
	S[0] = -C[0] / B[0]
	T[0] = D[0] / B[0]

	for i in xrange(1, n + 1):
		denom = B[i] + A[i] * S[i - 1]
		S[i] = -C[i] / denom
		T[i] = (-A[i] * T[i - 1] + D[i]) / denom

	Y[n] = T[n]

	for i in xrange(n - 1, -1, -1):
		Y[i] = S[i] * Y[i + 1] + T[i]

	# Testing
	for i, (a, b, c, g) in enumerate(zip(A, B, C, D)):
		ss = b * Y[i] - g
		if i >= 1:
			ss += a * Y[i - 1]
		if i <= len(Y) - 2:
			ss += c * Y[i + 1]
		if abs(ss) > 1e-8:
			print 'Failure at i=%d: %.4f' % (i, ss)

	S = -S
	T = -T

	return S, T, Y

def make_coefficients(p, q, r, f, a, b, alphas, betas, n, prec):
	num_points = (n + 1) + (1 if prec == 2 else 0)
	h = (b - a) / n

	A = np.zeros(num_points)
	B = np.zeros(num_points)
	C = np.zeros(num_points)
	D = np.zeros(num_points)

	if prec == 1:
		xs = np.linspace(a, b, num_points)
		
		B[0] = alphas[0] * h - alphas[1]
		C[0] = alphas[1]
		D[0] = alphas[2] * h

		A[-1] = -betas[1]
		B[-1] = betas[0] * h + betas[1]
		D[-1] = betas[2] * h

	elif prec == 2:
		raise NotImplementedError
		xs = np.linspace(a - h / 2, b + h / 2, num_points)

		B[0] = -(alphas[1] / 2 + alphas[2] / h)
		C[0] = (alphas[1] / 2 - alphas[2] / h)
		D[0] = alphas[0]

		A[-1] = (betas[1] / 2 - betas[2] / h)
		B[-1] = -(betas[1] / 2 + betas[2] / h)
		D[-1] = betas[0]

	# print(B[0], C[0], D[0])
	# print(A[-1], B[-1], D[-1])

	for i in xrange(1, num_points - 1):
		pi, qi, ri, fi = p(xs[i]), q(xs[i]), r(xs[i]), f(xs[i])
		A[i] = pi / h**2 - qi / (2*h)
		B[i] = -2*pi / h**2 + ri
		C[i] = pi / h**2 + qi / (2*h)
		D[i] = fi

	B = -B

	return xs, A, B, C, D

def plot_for(p, q, r, f, a, b, alphas, betas, exact, n, prec, refine, color):
	xs, A, B, C, D = make_coefficients(p, q, r, f, a, b, alphas, betas, n, prec)
	S, T, Y = sweep(A, B, C, D)

	if prec == 2:
		# moving to the original grid
		xs = np.linspace(a, b, n + 1)
		Y = (Y[1:] + Y[:-1]) / 2

	# if refine:
	# 	error = 

	exact_y = exact[1][::((len(exact[1]) - 1) // (len(Y) - 1))]

	print('Solution with n=%d nodes and precision O(h^%d)' % (n, prec))
	print(''.join('%12s' % s for s in ('xabcdstye')))
	for vals in zip(xs, A, B, C, D, S, T, Y, exact_y):
		print ''.join('%12.5f' % v for v in vals)

	plt.plot(xs, Y, color=color)


a, b = -1, 1

p = lambda x: - (4 + x) / (5 + 2*x)
q = lambda x: (1 - x / 2)
r = lambda x: 1 + np.exp(x / 2)
f = lambda x: 2 + x

alphas = 0, 1, 0 # a0 y(a) + a1 y(b) = a2
betas  = 2, 1, 0 # b0 y(a) + b1 y(b) = b2

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
# plot_for(p, q, r, f, a, b, alphas, betas, exact, n=10, prec=2, refine=False, color='c')
# plot_for(p, q, r, f, a, b, alphas, betas, exact, n=20, prec=2, refine=True, color='m')

plt.show()
