require 'matrix'

class Vector
	public :"[]="#, :set_element, :set_component

	def norm_inf
		return (self.map {|x| x.abs}).max
	end

	def clone
		return Marshal.load(Marshal.dump(self))
	end
end

class Matrix
	public :"[]="#, :set_element, :set_component

	def pretty
		return to_a.map(&:inspect)
	end

	def norm_inf
		best = 0
		0.upto(self.row_count - 1) do |k|
			s = self.row(k).reduce {|sum, x| sum + x.abs}
			if s > best
				best = s
			end
		end
		return best
	end

	def eigenvalues
		v, d, v_inv = self.eigensystem
		a = Array.new(d.column_count, 0)
		0.upto(d.column_count - 1) do |i|
			a[i] = d[i, i]
		end
		return a
	end

	def spectral_radius
		eig = self.eigenvalues
		return (eig.map! {|v| v.abs}).max
	end

	def clone
		return Marshal.load(Marshal.dump(self))
	end
end

def solveGaussian(matrix, vector)
	matrix = matrix.clone
	vector = vector.clone
	0.upto(matrix.row_count - 1) do |k|
		# not doing row selection / swapping / normalization
		(k+1).upto(matrix.row_count - 1) do |i|
			anchor = matrix[i, k] / matrix[k, k]
			# puts "i=#{i}, anchor=#{anchor}"
			k.upto(matrix.column_count - 1) do |j|
				matrix[i, j] -= anchor * matrix[k, j]
			end
			vector[i] -= anchor * vector[k]
		end
	end
	result = Vector.elements(Array.new(matrix.column_count, 0))
	(matrix.row_count - 1).downto(0) do |k|
		result[k] = vector[k]
		(k+1).upto(matrix.column_count - 1) do |j|
			result[k] -= matrix[k, j] * result[j]
		end
		result[k] /= matrix[k, k]
	end
	return result
end

def iteratify(a, b)
	invDiag = Array.new(a.column_count)
	0.upto(a.column_count - 1) do |i|
		invDiag[i] = 1 / a[i, i]
	end
	invD = Matrix.diagonal(*invDiag)
	mHD = Matrix.I(a.column_count) - invD * a
	vgD = invD * b
	return mHD, vgD
end

def iterate(a, b, n, x = nil)
	if x == nil
		x = Vector[*Array.new(a.column_count, 0)]
	end
	mHD, vgD = iteratify(a, b)
	# puts "#{mHD.norm_inf}"
	n.times do
		x = mHD * x + vgD
	end
	return x
end

def aposteriori_error(a, b, n)
	xn = iterate(a, b, n)
	xn1 = iterate(a, b, n - 1)
	mHD, vgD = iteratify(a, b)
	normH = mHD.norm_inf
	return (normH / (1 - normH)).abs * (xn - xn1).norm_inf
end

def seidelify(a, b)
	mHD, vgD = iteratify(a, b)
	mHL = Matrix.zero(mHD.column_count)
	1.upto(mHD.row_count - 1) do |i|
		0.upto(i - 1) do |j|
			mHL[i, j] = mHD[i, j]
		end
	end
	mHR = Matrix.zero(mHD.column_count)
	0.upto(mHD.row_count - 1) do |i|
		i.upto(mHD.column_count - 1) do |j|
			mHR[i, j] = mHD[i, j]
		end
	end
	mEHL = (Matrix.identity(mHL.row_count) - mHL).inverse
	mHseid = mEHL * mHR
	vgseid = mEHL * vgD
	return mHseid, vgseid
end

def seidel(a, b, n, x = nil, doLusternik = false)
	if x == nil
		x = Vector[*Array.new(a.column_count, 0)]
	end
	mHseid, vgseid = seidelify(a, b)
	# puts "#{mHseid.norm_inf}"
	prev = x
	n.times do
		prev = x
		x = mHseid * x + vgseid
	end
	if doLusternik
		rho = mHseid.spectral_radius
		x = prev + (1/(1 - rho)) * (x - prev)
	end
	return x
end

def upperRelaxation(a, b, eps, x = nil)
	if x == nil
		x = Vector[*Array.new(a.column_count, 0)]
	end
	mHD, vgD = iteratify(a, b)
	rho = mHD.spectral_radius
	normH = mHD.norm_inf
	q = 2 / (1 + Math.sqrt(1 - rho**2))
	n = 0
	while true do
		n += 1
		prev = x.clone
		0.upto(x.size - 1) do |i|
			sum1 = 0
			0.upto(i - 1) do |j|
				sum1 += mHD[i, j] * x[j]
			end
			sum2 = 0
			(i + 1).upto(mHD.column_count - 1) do |j|
				sum2 += mHD[i, j] * prev[j]
			end
			x[i] = prev[i] + q * (sum1 + sum2 - prev[i] + vgD[i])
		end
		finalDifference = (x - prev).norm_inf
		if finalDifference < eps
			puts "Exiting after #{n} iterations, error estimate is: #{finalDifference}"
			break
		end
	end
	return x
end


coefficients = [
	[9.016024, 1.082197, -2.783575],
	[1.082197, 6.846595, 0.647647],
	[-2.783575, 0.647647, 5.432541]
]

constants = [-1.340873, 4.179164, 5.478007]

# coefficients = [[2, 10, 8], [0, 7, 4], [5, 5, 5]].map! do |row|
# 	row.map! { |x| Rational(x) }
# end

# constants = [54, 30, 35].map! {|x| Rational(x)}

coefficients = Matrix[*coefficients]
constants = Vector[*constants]
puts "A ="
puts coefficients.pretty
puts "b = #{constants}"

solution = coefficients.inverse * constants
puts "x = #{solution}"

x8 = iterate(coefficients, constants, 8)
puts "x8 = #{x8}"

puts "aposteriori error: #{aposteriori_error(coefficients, constants, 8)}"
puts "actual error: #{(solution - x8).norm_inf}"

x8seid = seidel(coefficients, constants, 8)
puts "x8seid = #{x8seid}"
puts "seidel error: #{(solution - x8seid).norm_inf}"

# Never managed to guess how to call methods from submodules,
# and neither had any idea how to google that

# puts coefficients.eigenvalues
# puts coefficients.EigenvalueDecomposition.eigenvalues
# puts Matrix.eigenvalues(coefficients)
# puts Matrix.EigenvalueDecomposition.eigenvalues(coefficients)
# puts EigenvalueDecomposition.eigenvalues(coefficients)
# puts coefficients.eigenvalue_decomposition.eigenvalues
# puts Matrix::EigenvalueDecomposition.eigenvalues[coefficients]
# puts coefficients.eigensystem
# puts eigenvalues(coefficients)

mHseid, vgseid = seidelify(coefficients, constants)
puts "spectral radius of mHseid is: #{mHseid.spectral_radius}"

x8seidLusternik = seidel(coefficients, constants, 8, nil, true)
puts "x8seidLusternik = #{x8seid}"
puts "seidel error with Lusternik: #{(solution - x8seidLusternik).norm_inf}"

x8relax = upperRelaxation(coefficients, constants, 10**(-5))
puts "x8relax = #{x8relax}"
puts "upper relaxation error: #{(solution - x8relax).norm_inf}"
