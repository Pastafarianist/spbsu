import java.util.*;

class HashOpen<K, V> {
	ArrayList<ArrayList<OpEntry<K, V>>> contents;
	
	public HashOpen(int capacity) {
		contents = new ArrayList<ArrayList<OpEntry<K,V>>>(capacity);
		for (int i = 0; i < capacity; i++) {
			contents.add(new ArrayList<OpEntry<K, V>>());
		}
	}
	
	private OpEntry<K, V> getEntry(K key) {
		int h = key.hashCode() % contents.size();
		ArrayList<OpEntry<K, V>> bucket = contents.get(h);
		for (int i = 0; i < bucket.size(); i++) {
			OpEntry<K, V> entry = bucket.get(i); 
			if (entry.getKey().equals(key))
				return entry;
		}
		return null;
	}
	
	public boolean contains(K key) {
		OpEntry<K, V> entry = getEntry(key);
		return entry != null;
	}
	
	public V get(K key) {
		OpEntry<K, V> entry = getEntry(key);
		return entry == null ? null : entry.getValue();
	}
	
	public void put(K key, V val) {
		int h = key.hashCode() % contents.size();
		ArrayList<OpEntry<K, V>> bucket = contents.get(h);
		bucket.add(new OpEntry<K, V>(key, val));
	}
	
	public V remove(K key) {
		int h = key.hashCode() % contents.size();
		ArrayList<OpEntry<K, V>> bucket = contents.get(h);
		for (int i = 0; i < bucket.size(); i++) {
			OpEntry<K, V> entry = bucket.get(i); 
			if (entry.getKey().equals(key)) {
				V val = entry.getValue();
				bucket.remove(i);
				return val;
			}
		}
		return null;
	}
	
	public static void main (String[] args) {
		HashOpen<String, String> tbl = new HashOpen<String, String>(10);
		tbl.put("1", "one");
		tbl.put("2", "two");
		tbl.put("3", "three");
		System.out.println(tbl.contains("1"));
		System.out.println(tbl.contains("4"));
		System.out.println(tbl.get("1"));
		System.out.println(tbl.get("4"));
		System.out.println(tbl.remove("1"));
		System.out.println(tbl.remove("4"));
		System.out.println(tbl.contains("1"));
		System.out.println(tbl.contains("4"));
		System.out.println(tbl.contains("2"));
	}
}

class OpEntry<K, V> implements Map.Entry<K, V> {
	private final K key;
	private V val;
	
	public OpEntry(K key, V val) {
		this.key = key;
		this.val = val;
	}
	
	public K getKey() {
		return key;
	}
	
	public V getValue() {
		return val;
	}
	
	public V setValue(V val) {
		V oldv = this.val;
		this.val = val;
		return oldv;
	}
}