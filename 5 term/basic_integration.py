from __future__ import division, print_function
# import numpy as np
# import matplotlib.pyplot as plt

def integrate_rectangle(f, a, b, eps, max_d2):
	C, d = 1/24, 1
	n = 1
	while C * (b - a) * ((b - a) / n)**(d + 1) * max_d2 > eps:
		n *= 2
	print('n = %d' % n)
	h = (b - a) / n
	return h * sum(f(a + h/2 + k * h) for k in xrange(n))

def integrate_simpson(f, a, b, eps, max_d4):
	C, d = 1/2880, 3
	n = 1
	while C*(b - a) * ((b - a) / n)**(d + 1) * max_d4 > eps:
		n *= 2
	print('n = %d' % n)
	h = (b - a) / (2*n)
	g = lambda k: f(a + k*h)
	s_odd = sum(g(j) for j in xrange(1, 2*n, 2))
	s_even = sum(g(j) for j in xrange(2, 2*n-1, 2))
	return ((b - a)/(6*n)) * (g(0) + 4*s_odd + 2*s_even + g(2*n))


f = lambda x: 1/(1 + x**3)
max_d2 = 1.580246913580247
max_d4 = 29.49794238683128
a, b = 0.5, 1.5
eps = 0.00001

print('Exact value: 0.5238896176636051')
print(integrate_rectangle(f, a, b, eps, max_d2))
print(integrate_simpson(f, a, b, eps, max_d4))
exit()

vf = np.vectorize(f)
xs = np.linspace(0, 2, 100)
ys = vf(xs)
plt.plot(xs, ys, 'b-')
plt.vlines([0.5, 1.5], 0, 2)
plt.ylim([0, 1.5])
plt.show()