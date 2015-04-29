from __future__ import division
import numpy as np
import unittest

def eigen_jacobi(a, eps):
	n = len(a)
	if n <= 1:
		return a

	eigenvectors = np.identity(len(a), dtype=np.float32)
	while True:
		max_a = float('-inf')
		max_i, max_j = None, None
		for i in xrange(n):
			for j in xrange(i + 1, n):
				if np.abs(a[i, j]) > max_a:
					max_i = i
					max_j = j
					max_a = np.abs(a[i, j])

		if max_a < eps:
			break

		diff = a[max_i, max_i] - a[max_j, max_j]
		d = np.sqrt(np.abs(diff)**2 + 4 * a[max_i, max_j]**2)
		c = np.sqrt(0.5 * (1 + np.abs(diff) / d))
		s = (1 if (a[max_i, max_j] * diff) >= 0 else -1) * np.sqrt(0.5 * (1 - np.abs(diff) / d))

		new_aii = c**2 * a[max_i, max_i] + 2 * c * s * a[max_i, max_j] + s**2 * a[max_j, max_j]
		new_ajj = s**2 * a[max_i, max_i] - 2 * c * s * a[max_i, max_j] + c**2 * a[max_j, max_j]

		old_max_i = a[:, max_i].copy()
		old_max_j = a[:, max_j].copy()

		for i in xrange(n):
			new_val = c * a[i, max_i] + s * a[i, max_j]
			a[i, max_i] = new_val
			a[max_i, i] = new_val

		for i in xrange(n):
			new_val = -s * old_max_i[i] + c * old_max_j[i]
			a[i, max_j] = new_val
			a[max_j, i] = new_val

		a[max_i, max_i] = new_aii
		a[max_j, max_j] = new_ajj
		a[max_i, max_j] = 0
		a[max_j, max_i] = 0

		old_max_i = eigenvectors[max_i, :].copy()
		old_max_j = eigenvectors[max_j, :].copy()

		for j in xrange(n):
			eigenvectors[j, max_i] = c * old_max_i[j] + s * old_max_j[j]

		for j in xrange(n):
			eigenvectors[j, max_j] = -s * old_max_i[j] + c * old_max_j[j]

	# eigenvalues = np.float32([a[i, i] + sum(a[i, j] / (a[i, i] - a[j, j]) for j in xrange(n) if j != i) for i in xrange(n)])
	eigenvalues = np.float32([a[i, i] for i in xrange(n)])

	return a, eigenvalues, eigenvectors


class TestAll(unittest.TestCase):
	def setUp(self):
		np.set_printoptions(precision=6)
		self.eps =  0.000001

	def go(self, a):
		print('Original matrix:')
		print(a)

		print('Numpy\'s eigenvalues and eigenvectors:')
		w, v = np.linalg.eig(a)
		idx = w.argsort()   
		w = w[idx]
		v = v[:,idx]

		print(w)
		print(v)

		print('My eigenvalues and eigenvectors:')
		a, eigenvalues, eigenvectors = eigen_jacobi(a, self.eps)
		idx = eigenvalues.argsort()   
		eigenvalues = eigenvalues[idx]
		eigenvectors = eigenvectors[:,idx]

		print(eigenvalues)
		print(eigenvectors)

		print('Transformed matrix:')
		print(a)
		print('')

	def testSimple(self):
		a = np.float32([
			[1, 2],
			[2, 1]
		])
		self.go(a)

	def testStandard(self):
		# matrix #6
		a = np.float32([
			[-0.93016, -0.25770, 0.45254],
			[-0.25770, 0.65022, 0.07193],
			[0.45255, 0.07193, -0.97112]
		])
		self.go(a)
		

if __name__ == '__main__':
	unittest.main()