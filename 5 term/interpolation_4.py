from __future__ import division
from math import factorial
import numpy as np
import matplotlib.pyplot as plt

# x=0: 4, 12, 18, -24
# x=1: 16, 0, -48

conditions = [
    [0, 4, 12, 18, -24],
    [1, 16, 0, -48]
]

def product(lst):
	result = 1
	for v in lst:
		result *= v
	return result

def flatten(lst):
	return [item for sublist in lst for item in sublist]

def find_pt(x, conditions):
	for pt in conditions:
		if pt[0] == x:
			return pt

def make_deltas(conditions):
	xs = flatten([pt[0]] * (len(pt) - 1) for pt in conditions)
	print xs
	n = len(xs)
	deltas = [flatten([pt[1]] * (len(pt) - 1) for pt in conditions)]
	print deltas
	for k in xrange(1, n):
		new_deltas = []
		for j in xrange(n - k):
			denom = xs[j + k] - xs[j]
			if denom == 0:
				pt = find_pt(xs[j], conditions)
				new_delta = pt[k + 1] / factorial(k)
			else:
				new_delta = (deltas[k - 1][j + 1] - deltas[k - 1][j]) / denom
			new_deltas.append(new_delta)
		deltas.append(new_deltas)
	return deltas

def hermitian_interpolation(conditions):
	xs = flatten([pt[0]] * (len(pt) - 1) for pt in conditions)
	n = len(xs)
	deltas = make_deltas(conditions)
	diag = [layer[0] for layer in deltas]
	def kterm(k, x):
		prod = product(x - xs[j] for j in xrange(k))
		return diag[k] * prod
	return lambda x: sum(kterm(k, x) for k in xrange(n))

def print_deltas(conditions):
	deltas = make_deltas(conditions)
	for layer in deltas:
		print '\t'.join('%.4f' % v for v in layer)
	print '[' + ', '.join('%.4f' % layer[0] for layer in deltas) + ']'

print_deltas(conditions)
deltas = make_deltas(conditions)
diag = [layer[0] for layer in deltas]
print 'diag', diag

herm = hermitian_interpolation(conditions)
vHerm = np.vectorize(herm)
x = np.linspace(-1, 2, 100)

plt.plot(x, vHerm(x), '-')
plt.plot([0, 1], [4, 16], 'ro')
plt.ylim([0, 20])
plt.show()