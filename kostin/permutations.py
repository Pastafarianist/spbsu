import random
 
class Permutation(object):
	def __init__(self, array, offset=1, validate=False):
		if validate and not Permutation.validate(array, offset):
			raise ValueError("Validation failure")
		self.array = list(array)
		self.size = len(array)
		self.offset = offset
 
	@staticmethod
	def random(n, offset=1):
		a = range(offset, n + offset)
		random.shuffle(a)
		return Permutation(a, offset)
 
	@staticmethod
	def validate(array, offset):
		was = [False] * len(array)
		for val in array:
			if not (0 <= val - offset < len(array)) or was[val - offset]:
				return False
			was[val - offset] = True
		return True
 
	@staticmethod
	def from_cycles(cycles, offset=1, validate=False):
		""" Separation of cycles with negative numbers is assumed.
		Therefore, 'offset' cannot be negative. """
		if validate:
			if cycles[0] >= 0:
				raise ValueError("Validation failure")
			absolute = [abs(v) for v in cycles]
			if not Permutation.validate(absolute, offset):
				raise ValueError("Validation failure")
		new_array = [None] * len(cycles)
		cycle_start = abs(cycles[0])
		prev_val = abs(cycles[0])
		for val in cycles[1:]:
			if val < 0:
				# A new cycle has begun
				new_array[prev_val - offset] = cycle_start
				cycle_start = prev_val = abs(val)
			else:
				new_array[prev_val - offset] = val
				prev_val = val
		new_array[prev_val - offset] = cycle_start
		return Permutation(new_array, offset)
 
	def to_cycles(self):
		was = [False] * self.size
		cycles = []
		for cycle_start, val in enumerate(self.array):
			if was[cycle_start]:
				continue
			cycles.append(-(cycle_start + self.offset))
			index_to = val - self.offset
			while index_to != cycle_start:
				was[index_to] = True
				cycles.append(index_to + self.offset)
				index_to = self.array[index_to] - self.offset
		return cycles
 
	def to_canonical(self):
		""" DISCLAIMER: I find this approach absolutely disgusting and strongly
		discourage anyone from using it, should they need. It is AWFUL.
		Converts 'self' to the canonical representation, i.e. cyclic but in all
		cycles the smallest element is the first and the cycles themselves are
		sorted in descending order of their first elements. This way, each
		permutation can be expressed in a unique way (i.e. the mapping is
		bijective).
		The idea is to start with the smallest possible first element (1) and
		walk the entire cycle it is in via a recursive function. As soon as the
		recursion hits the first element again, stop and walk back, putting all
		encountered elements in the resulting list in reverse order. Repeat with
		all elements.
		This sucks because it could potentially result in a stack overflow. A
		less error-prone approach would be to walk all cycles twice: first time
		to measure their length (so that we knew where to put the elements in
		the resulting list) and second time to write the elements. """
		result = [None] * self.size
		was = [False] * self.size
		writing_at = self.size - 1
		def walk_cycle(cycle_elem, writing_at):
			was[cycle_elem] = True
			if cycle_elem != cycle_start:
				next_elem = self.array[cycle_elem] - self.offset
				writing_at = walk_cycle(next_elem, writing_at)
				result[writing_at] = cycle_elem + self.offset
				return writing_at - 1
			return writing_at
		for cycle_start, val in enumerate(self.array):
			if was[cycle_start]:
				continue
			writing_at = walk_cycle(val - self.offset, writing_at)
			result[writing_at] = cycle_start + self.offset
			writing_at -= 1
		return result
 
	@staticmethod
	def from_inversions(inversions, offset=1, validate=False):
		""" Converts the inversion table representation of a permutation to
		the natural one.
		The idea is to put the biggest element first somewhere and then append
		other elements next to or between already existing ones. This is
		achieved through the use of a linked list (represented as an array) for
		storing the permutation. """
		size = len(inversions)
		if validate:
			for i, v in inversions:
				if not (0 <= v < size - i):
					raise ValueError("Validation failure")
		# This will be used to represent the resulting permutation.
		# Indices in this list stand for the elements in the permutation,
		# while values are permutation elements immediately after the index.
		# Zero'th index is used to store the first element, hence total size.
		linked_list = [0] + [None] * size
		for i in reversed(xrange(size)): # for(i = size - 1; i >= 0; i--)
			insert_after = 0
			for _ in xrange(inversions[i]):
				insert_after = linked_list[insert_after]
			# At this moment, linked_list[i] == None.
			# +1 is due to linked_list being shifted one step to the right.
			linked_list[i + 1] = linked_list[insert_after]
			linked_list[insert_after] = i + 1
		current_pos = 0
		result = []
		for _ in xrange(size):
			result.append(linked_list[current_pos] + offset - 1)
			current_pos = linked_list[current_pos]
		return Permutation(result, offset)
 
	def to_inversions(self):
		""" Calculates a representation of the permutation as a table of
		inversions. Brute-force approach. """
		inversions = [0] * self.size
		for i, val in enumerate(self.array):
			for elem in self.array[:i]:
				if elem > val:
					inversions[val - self.offset] += 1
		return inversions
 
	def __str__(self):
		return '[%s]' % ' '.join(str(v) for v in self.array)
 
	def __call__(self, val):
		return self.array[val - self.offset]
 
	def __eq__(self, perm):
		return self.array == perm.array
 
	def __ne__(self, perm):
		return self.array != perm.array
 
	def __mul__(self, perm):
		if self.offset != perm.offset or self.size != perm.size:
			raise TypeError("Permutations are incompatible")
		new_array = [self(perm(v)) for v in xrange(self.offset, self.size + self.offset)]
		return Permutation(new_array, self.offset)
 
	def __invert__(self):
		new_array = [None] * self.size
		for i, v in enumerate(self.array, self.offset):
			new_array[v - self.offset] = i
		return Permutation(new_array, self.offset)
 
	def invert(self):
		""" Inverts the permutation in-place.
		The idea is to walk through all cycles (pieces like a -> b -> c
		-> ... -> x -> a) and shift them, i.e. make from (a -> b, b -> c,
		c -> a) (a -> c, b -> a, c -> b).
		In other words, cycles can be interpreted as pairs (domain, image)
		and the image is shifted: (abc, bca) becomes (abc, cab). """
		was = [False] * self.size
		for cycle_start, val in enumerate(self.array):
			if was[cycle_start]:
				continue
			was[cycle_start] = True
			index_from = cycle_start
			index_to = val - self.offset
			while index_to != cycle_start:
				was[index_to] = True
				# The following 4 lines can be written as a one-liner.
				# Unreadable, though.
				current_image = self.array[index_to]
				self.array[index_to] = index_from + self.offset
				index_from = index_to
				index_to = current_image - self.offset
			self.array[cycle_start] = index_from + self.offset
 
	def parity(self):
		""" Calculates parity (oddness or evenness) of the permutation
		in linear time.
		There is a theorem that a permutation is even iff it has an even
		number of cycles of even length. Note: the two variables is_even_*
		may be replaced with a single one which would be modified only within
		the 'while' loop. It would greatly affect readability, though.
		Note: 'iff' is not a typo. It stands for 'if and only if'. """
		was = [False] * self.size
		is_even_number = True
		for cycle_start, val in enumerate(self.array):
			if was[cycle_start]:
				continue
			# this is not necessary and done only for consistency
			was[cycle_start] = True
			index_to = val - self.offset
			is_even_length = False
			while index_to != cycle_start:
				was[index_to] = True
				index_to = self.array[index_to] - self.offset
				is_even_length = not is_even_length
			if is_even_length:
				is_even_number = not is_even_number			
		return 'even' if is_even_number else 'odd'
 
	def compose_with_cyclic(self, cycles):
		""" Modifies this Permutation in-place so that it becomes a composition
		of the form [x -> cyclic(self(x))]. Equal offsets are assumed. The
		equality of lengths is verified.
		The idea is to walk through the 'cyclic' permutation in reverse order,
		i.e. from end to beginning. On each step, we perform a brute-force
		substitution in 'self' by directly looking up the current number and
		replacing it with the stored next number. If no next number is known,
		a None is used to signify the end-of-cycle. When we reach the beginning
		of the current cycle, the stored position of None is retrieved and the
		None there is replaced with the number at the beginning. """
		if self.size != len(cycles):
			raise TypeError("Permutations are incompatible")
		prev_val = None # None is an end-of-cycle marker
		cycle_end_index = None # Will be set on the first iteration
		for i in reversed(xrange(self.size)): # for(i = size - 1; i >= 0; i--)
			curr_val = abs(cycles[i])
			# Replace first (and only) occurrence of curr_val with prev_val
			curr_val_index = self.array.index(curr_val)
			self.array[curr_val_index] = prev_val
			if prev_val == None:
				cycle_end_index = curr_val_index
			if cycles[i] < 0: # The beginning of the current cycle is reached
				self.array[cycle_end_index] = curr_val
				prev_val = None
			else:
				prev_val = curr_val
 
	def print_inversion_matrix(self):
		result = [['.' for __ in xrange(self.size)] for _ in xrange(self.size)]
		for i, val in enumerate(self.array):
			v = val - self.offset
			result[v][i] = 'x'
			for j, prev_val in enumerate(self.array[:i]):
				if prev_val > val:
					result[v][j] = '1'
		print '\n'.join(''.join(row) for row in result)
 
	@staticmethod
	def invert_cyclic(cycles):
		""" Inverts the cyclic representation of a permutation in-place.
		The procedure consists of 2 parts: first, we walk through the
		permutation and move all '-' signs one step to the left and second,
		we reverse the order.
		The validity of the input is assumed. """
		cycles[0] = -cycles[0]
		# Actually, this is Python, so cycles[-1] could refer to the last
		# element of the permutation and the line above would not be necessary.
		for i in xrange(1, len(cycles)):
			if cycles[i] < 0:
				cycles[i - 1] = -cycles[i - 1]
				cycles[i] = -cycles[i]
		cycles[-1] = -cycles[-1]
		cycles.reverse()
 
	@staticmethod
	def parity_cyclic(cycles):
		""" Calulates the parity of the cyclic representation of a permutation.
		The idea is the same as with the natural representation. """
		is_even = True
		for v in cycles:
			if v > 0:
				is_even = not is_even
		return 'even' if is_even else 'odd'
 
	@staticmethod
	def parity_inversions(inversions):
		return 'even' if sum(inversions) % 2 == 0 else 'odd'
 
	@staticmethod
	def invert_inversions(inversions):
		""" Inverts a permutation represented as a table of inversions and
		returns the result as another table of inversions.
		The idea is to consider the inversion matrix of a permutation. In
		order to calculate the inverted permutation, one needs to count the
		number of 1's in each column (as opposed to the counting them in the
		rows for the original, non-inverted permutation). To do that, first
		observe that the first row always looks like 11111x..., since every
		element that is in front of the smallest one forms a transposition.
		Also, no 1's can be	 below x's (a smaller element cannot form a
		transposition with a bigger one). Therefore, we have to track the
		columns in which an x has already occurred earlier. This can be done
		by using a linked list, in which for each column we store the next one.
		On each step, we jump through the row, increasing the accumulator every
		time we visit a cell. """
		n = len(inversions)
		result = [0] * n
		# Column indices start from 1, and at the 0 next_column stores the first
		# remaining column index.
		next_column = range(1, n + 2) # [1..n+1]
		for num_inv in inversions[:-1]:
			prev_col = 0
			curr_col = next_column[0]
			for _ in xrange(num_inv):
				result[curr_col - 1] += 1
				prev_col = curr_col
				curr_col = next_column[curr_col]
			# After the following line, curr_col will never be visited again.
			# Before: prev_col -> curr_col -> something
			# After: prev_col -> something
			next_column[prev_col] = next_column[curr_col]
		return result
 
 
def test():
	n = 4
	p1 = Permutation.random(n)
	p2 = Permutation.random(n)
	print 'p1 = %s' % p1
	print 'p2 = %s' % p2
	print 'p1 * p2 = %s' % (p1 * p2)
	print 'p2 * p1 = %s' % (p2 * p1)
	print '~p1 = %s' % (~p1)
	print '~p2 = %s' % (~p2)
	p1.invert()
	print 'inverted p1: %s' % p1
	p1.invert()
	print 'p1 is %s' % p1.parity()
	print 'p2 is %s' % p2.parity()
	cyc_1 = p1.to_cycles()
	cyc_2 = p2.to_cycles()
	print 'p1 = %s, cyclic = %s, back = %s' % (p1, cyc_1, Permutation.from_cycles(cyc_1))
	print 'p2 = %s, cyclic = %s, back = %s' % (p2, cyc_2, Permutation.from_cycles(cyc_2))
	p1.compose_with_cyclic(cyc_2)
	print 'cyc_2 * p1 = %s' % p1
	Permutation.invert_cyclic(cyc_2)
	p1.compose_with_cyclic(cyc_2)
	Permutation.invert_cyclic(cyc_2)
	print 'p1 again = %s' % p1
	print 'cyc_1 is %s' % Permutation.parity_cyclic(cyc_1)
	print 'cyc_2 is %s' % Permutation.parity_cyclic(cyc_2)
	print 'canonical p1 = %s' % p1.to_canonical()
	print 'canonical p2 = %s' % p2.to_canonical()
	inv_1 = p1.to_inversions()
	inv_2 = p2.to_inversions()
	print 'inversions of p1 = %s' % inv_1
	print 'inversions of p2 = %s' % inv_2
	print 'p1 from inv_1 = %s' % Permutation.from_inversions(inv_1)
	print 'p2 from inv_2 = %s' % Permutation.from_inversions(inv_2)
	print 'inv_1 is %s' % Permutation.parity_inversions(inv_1)
	print 'inv_2 is %s' % Permutation.parity_inversions(inv_2)
	print 'Inversion matrix of p1:'
	p1.print_inversion_matrix()
	iinv_1 = Permutation.invert_inversions(inv_1)
	print 'inverse of inv_1 = %s' % iinv_1
	print '~p1 from iinv_1 = %s' % Permutation.from_inversions(iinv_1)
 
if __name__ == '__main__':
	test()
