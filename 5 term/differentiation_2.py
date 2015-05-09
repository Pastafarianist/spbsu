from __future__ import division, print_function
from math import exp, sqrt

# http://www.intuit.ru/studies/courses/1012/168/lecture/4590?page=5

# e^x, [0, 1], x0=1/2, eps=10^(-4)

eps = 0.0001
x0 = 0.5

# right derivative
# trunc_error = h/2 * [max f''(x)]
# round_error = (2*eps*[max f(x)]) / h
# h_opt = 2 * sqrt( (eps*[max f(x)]) / [max f''(x)] )
h_opt = 2 * sqrt(eps)
for h in (h_opt/2, h_opt, 3/2 * h_opt):
	exact = exp(x0)
	approx = (exp(x0+h) - exp(x0))/h

	trunc_error = (h/2)*exp(x0+h)
	round_error = (2*eps*exp(x0+h))/h
	total_error = trunc_error + round_error
	real_error = approx - exact

	print("%.5f %.5f %.5f %.5f %.5f %.5f" % (exact, approx, trunc_error, round_error, total_error, real_error))

print()

# center derivative
# trunc_error = [max f'''(x)]*(h^2 / 3)
# round_error = eps*[max f(x)] / h
h_opt = ( (3*eps) )**(1/3)
for h in (h_opt/2, h_opt, 3/2 * h_opt):
	exact = exp(x0)
	approx = (exp(x0+h) - exp(x0-h))/(2*h)

	trunc_error = ((h**2)/3)*exp(x0+h)
	round_error = (eps*exp(x0+h))/h
	total_error = trunc_error + round_error
	real_error = approx - exact

	print("%.5f %.5f %.5f %.5f %.5f %.5f" % (exact, approx, trunc_error, round_error, total_error, real_error))