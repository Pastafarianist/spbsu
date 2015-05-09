from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

def build_simpson(a, b, subdivisions):
	n = subdivisions * 2
	num_nodes = n + 1
	xs = np.linspace(a, b, num_nodes)
	A = np.empty(num_nodes)
	A[0] = 1
	for j in xrange(1, n // 2):
		A[2*j] = 2
	for j in xrange(1, n // 2 + 1):
		A[2*j - 1] = 4
	h = (b - a) / n
	A[-1] = 1
	A *= h / 3
	return xs, A

def solve_fredholm(a, b, H, f, xs, A):
	m = len(xs)

	D = np.empty((m, m))
	for j in xrange(m):
		for k in xrange(m):
			D[j, k] = (1 if j == k else 0) - A[k] * H(xs[j], xs[k])

	# np.set_printoptions(precision=2)
	# print D

	g = np.array([f(x) for x in xs])
	z = np.linalg.solve(D, g)
	u = lambda x: f(x) + sum(A[k] * H(x, xs[k]) * z[k] for k in xrange(m))
	return u
	

a, b = 0, 1
H = lambda x, y: 0.5 * np.tanh(x * y)
f = lambda x: x - 0.5

subdivisions = 5

xs, A = build_simpson(a, b, subdivisions)
u = solve_fredholm(a, b, H, f, xs, A)

plt_xs = np.linspace(a, b, 50)
plt.plot(plt_xs, u(plt_xs))
plt.ylim((-1, 1))
plt.grid(True)
plt.show()