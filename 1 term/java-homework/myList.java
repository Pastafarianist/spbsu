public class myList {
	// ************ FIELDS ************ //
	private myElem l;
	

	// ************ CONSTRUCTORS ************ //
	public myList() {
		l = null;
	}
	
	public myList(myElem _l) {
		l = _l;
	}
	
	
	// ************ METHODS ************ //
	private myElem nth_elem(int n) {
		myElem cur = l;
		while(n > 0) {
			assert(cur != null);
			cur = cur.next;
			n--;
		}
		return cur;
	}
	
	public int length() {
		int len = 0;
		myElem cur = l;
		while(cur != null) {
			len++;
			cur = cur.next;
		}
		return len;
	}
	
	public String nth(int n) {
		return nth_elem(n).v;
	}
	
	public void insert(int n, String s) {
		if (n == 0) {
			myElem next = l == null ? null : l.next;
			myElem newElem = new myElem(next, s);
			l = newElem;
		}
		else {
			myElem elem = nth_elem(n-1);
			myElem newElem = new myElem(elem.next, s);
			elem.next = newElem;
		}
	}
	
	public String delete(int n) {
		if (n == 0) {
			String result = l.v;
			l = l.next;
			return result;
		}
		else {
			myElem elem = nth_elem(n-1);
			assert(elem.next != null);
			String result = elem.next.v;
			elem.next = elem.next.next;
			return result;
		}
	}
	
	public int find (String s) {
		// -1 if not found
		myElem cur = l;
		int result = 0;
		while(cur != null) {
			if (cur.v.equals(s))
				return result;
			else {
				cur = cur.next;
				result += 1;
			}
		}
		return -1;
	}
	
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append('[');
		myElem cur = l;
		while(cur != null) {
			sb.append(cur.v);
			cur = cur.next;
			if (cur == null) {
				break;
			}
			else {
				sb.append(", ");
			}
		}
		sb.append(']');
		return sb.toString();
	}
	
	
	// ************ TEST ************ //
	public static void main(String[] args) {
		myList list = new myList();
		System.out.println(list);
		
		list.insert(0, "first");
		list.insert(1, "second");
		list.insert(2, "third");
		list.insert(3, "fourth");
		list.insert(4, "fifth");
		System.out.println(list);
		
		System.out.print("Length: "); System.out.println(list.length());
		
		System.out.printf("3rd: ");   System.out.println(list.nth(2));
		System.out.printf("5th: ");   System.out.println(list.nth(4));
		
		System.out.printf("first: "); System.out.println(list.find("first"));
		System.out.printf("third: "); System.out.println(list.find("third"));
		
		list.delete(3);
		System.out.printf("4th: %s\n", list.nth(3));
		System.out.println(list);
	}

}

class myElem {
	public myElem next;
	public String v;
	
	public myElem(myElem _next, String _v) {
		next = _next;
		v = _v;
	}
}