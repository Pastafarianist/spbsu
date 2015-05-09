from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

ys = [0.1494, 0.2474, 0.3428, 0.4349, 0.5226, 0.6051, 0.6816, 0.7512, 0.8134]
ys = np.asarray(ys)
x1 = 0.15
h = 0.1
xs = np.linspace(x1, x1 + h * (len(ys) - 1), len(ys))

def product(lst):
	result = 1
	for v in lst:
		result *= v
	return result

# def lagrange_polynomial(xs, k):
# 	# expecting k < len(xs)
# 	n = len(xs)
# 	denom = product(xs[k] - xs[i] for i in xrange(n) if i != k)
# 	return lambda x: product(x - xs[i] for i in xrange(n) if i != k) / denom

# def reverse_interpolate(xs, ys):
# 	# expecting ys to be sorted in ascending order
# 	n = len(ys)
# 	lp = [lagrange_polynomial(ys, k) for k in xrange(n)]
# 	return lambda y: sum(lp[k](y) * xs[k] for k in xrange(n))

def interpolate(xs, ys):
	n = len(xs)
	def result(xval):
		P = np.zeros((n, n))
		P[0, :] = ys
		for j in xrange(0, n - 1):
			for i in xrange(j+1, n):
				P[j+1, i] = (P[j, i]*(xval - xs[j]) - P[j, j]*(xval - xs[i])) / (xs[i] - xs[j])
		return P[n-1, n-1]
	return result

def reverse_interpolate(xs, ys):
	return interpolate(ys, xs)

y = np.linspace(0, 1, 100)
rev = reverse_interpolate(xs, ys)
print rev(0.65)

vRev = np.vectorize(rev)
plt.plot(y, vRev(y), '-')
plt.plot(ys, xs, 'ro')
plt.ylim([0, 1])
plt.show()