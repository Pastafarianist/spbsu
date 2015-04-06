
public class myDoubleList {
	//************ FIELDS ************//
	private myDoubleElem l;
	private myDoubleElem first, last;
	private int len_left, len_right;
	
	
	//************ CONSTRUCTORS ************ //
	public myDoubleList() {
		l = null;
		first = last = null;
		len_left = len_right = 0;
	}
	
	
	//************ METHODS ************//
	public int length_left() {
		return len_left;
	}
	
	public int length_right() {
		return len_right;
	}
	
	public int length() {
		return len_left + 1 + len_right;
	}
	
	public myDoubleElem nth_elem(int n) {
		assert(l != null);
		if (n == 0)
			return l;
		else {
			myDoubleElem cur = l;
			if (n > 0) {
				while(n > 0) {
					assert(cur != null);
					cur = cur.next;
					n--;
				}
				assert(cur != null);
				return cur;
			}
			else {
				while(n < 0) {
					assert(cur != null);
					cur = cur.prev;
					n++;
				}
				assert(cur != null);
				return cur;
			}	
		}
	}
	
	
	public String nth(int n) {
		return nth_elem(n).v;
	}
	
	
	public void insert(int n, String s) {
		if (l == null) {
			assert(n == 0);
			l = new myDoubleElem(null, null, s);
			first = last = l;
		}
		else {
			if (n == 0) {
				l = new myDoubleElem(l.prev, l, s);
				len_right += 1;
			}
			else if (n > 0) {
				len_right += 1;
				myDoubleElem elem = nth_elem(n - 1);
				if (elem.next == null) {
					elem.next = new myDoubleElem(elem, null, s);
					last = elem.next;
				}
				else {
					myDoubleElem newElem = new myDoubleElem(elem, elem.next, s); 
					elem.next.prev = newElem;
					elem.next = newElem;
				}
			}
			else {
				len_left += 1;
				myDoubleElem elem = nth_elem(n + 1);
				if (elem.prev == null) {
					elem.prev = new myDoubleElem(null, elem, s);
					first = elem.prev;
				}
				else {
					myDoubleElem newElem = new myDoubleElem(elem.prev, elem, s);
					elem.prev.next = newElem;
					elem.prev = newElem;
				}
			}
		}
	}
	
	
	public void insert_first(String s) {
		if (first == null) {
			// This means that the list is empty and l == last == null.
			l = new myDoubleElem(null, null, s);
			first = last = l;
		}
		else {
			assert(len_left == 0); // This is because this method is purely for implementing the queue.
			myDoubleElem newElem = new myDoubleElem(null, l, s);
			l = newElem;
			l.next.prev = newElem;
			first = l; // This actually breaks the connection with the left part of the list.
					   // The GC is supposed to destroy it later.
			len_right += 1;
		}
	}
	
	
	public String delete(int n) {
		if (n == 0) {
			assert(l != null);
			String result = l.v;
			if (l.prev == null) {
				if (l.next == null) {
					l = null;
					first = last = null;
				}
				else {
					l = l.next;
					l.prev = null;
					len_right -= 1;
					first = l;
				}
			}
			else {
				if (l.next == null) {
					l = l.prev;
					l.next = null;
					len_left -= 1;
					last = l;
				}
				else {
					l.next.prev = l.prev;
					l.prev.next = l.next;
					l = l.next;
					len_right -= 1;
				}
			}
			return result;
		}
		else {
			myDoubleElem elem = nth_elem(n);
			if (n > 0) {
				len_right -= 1;
				if (elem.next == null) {
					elem.prev.next = null;
					last = elem.prev;
				}
				else {
					elem.prev.next = elem.next;
					elem.next.prev = elem.prev;
				}
			}
			else {
				len_left -= 1;
				if (elem.prev == null) {
					elem.next.prev = null;
					first = elem.next;
				}
				else {
					elem.prev.next = elem.next;
					elem.next.prev = elem.prev;
				}
			}
			return elem.v;
		}
	}
	
	
	public String delete_last() {
		assert(last != null);
		String result = last.v;
		if (last.prev == null) {
			// This means that the length of the list is 1 and l == last == prev.
			// len_left == len_right == 0 anyway, so we don't need to touch them.
			l = null;
			first = last = null;
		}
		else {
			last.prev.next = null;
			last = last.prev;
			len_right -= 1;
		}
		return result;
	}
	
	
	public static void main(String[] args) {
		myDoubleList list = new myDoubleList();
		
		list.insert(0, "zero");
		list.insert(1, "one");
		list.insert(2, "two");
		list.insert(-1, "minus one");
		list.insert(-2, "minus two");
		
		System.out.printf("0: %s\n", list.nth(0));
		System.out.printf("1: %s\n", list.nth(1));
		System.out.printf("2: %s\n", list.nth(2));
		System.out.printf("-1: %s\n", list.nth(-1));
		System.out.printf("-2: %s\n", list.nth(-2));
		System.out.print("\n");
		
		System.out.printf("first: %s\n", list.first.v);
		System.out.printf("last: %s\n", list.last.v);
		System.out.print("\n");
		
		System.out.printf("Left length: %d\n", list.length_left());
		System.out.printf("Right length: %d\n", list.length_right());
		System.out.print("\n");
		
		list.delete(1); System.out.println("Deleted: 1");
		System.out.printf("1: %s\n", list.nth(1));
		System.out.printf("Right length: %d\n", list.length_right());
		System.out.printf("last: %s\n", list.last.v);
		System.out.print("\n");
		
		list.delete(-1); System.out.println("Deleted: -1");
		System.out.printf("-1: %s\n", list.nth(-1));
		System.out.printf("Left length: %d\n", list.length_left());
		System.out.printf("first: %s\n", list.first.v);
		System.out.print("\n");
		
		list.insert(1, "one"); System.out.println("Inserted: 1, one");
		System.out.printf("1: %s\n", list.nth(1));
		System.out.printf("2: %s\n", list.nth(2));
		System.out.printf("Right length: %d\n", list.length_right());
		System.out.printf("last: %s\n", list.last.v);
		System.out.print("\n");
		
		list.insert(-1, "minus one"); System.out.println("Inserted: -1, minus one");
		System.out.printf("-1: %s\n", list.nth(-1));
		System.out.printf("-2: %s\n", list.nth(-2));
		System.out.printf("Left length: %d\n", list.length_left());
		System.out.printf("first: %s\n", list.first.v);
		System.out.print("\n");
		
		list.delete(2); System.out.println("Deleted: 2");
		System.out.printf("Right length: %d\n", list.length_right());
		System.out.printf("last: %s\n", list.last.v);
		System.out.print("\n");
		
		list.delete(-2); System.out.println("Deleted: -2");
		System.out.printf("Left length: %d\n", list.length_left());
		System.out.printf("first: %s\n", list.first.v);
	}

}


class myDoubleElem {
	public myDoubleElem prev, next;
	public String v;
	
	public myDoubleElem(myDoubleElem _prev, myDoubleElem _next, String _v) {
		prev = _prev;
		next = _next;
		v    = _v;
	}
}