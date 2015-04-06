import java.util.*;

class HashClosed<K, V> {
	ArrayList<ClEntry<K, V>> contents;
	
	public HashClosed(int capacity) {
		contents = new ArrayList<ClEntry<K,V>>(capacity);
		for (int i = 0; i < capacity; i++) {
			contents.add(null);
		}
	}
	
	private ClEntry<K, V> getEntry(K key) {
		int start = key.hashCode() % contents.size();
		int i = start;
		do {
			ClEntry<K, V> ent = contents.get(i);
			if (ent == null)
				return null;
			if (ent.isDeleted)
				continue;
			if (ent.key.equals(key)) {
				return ent;
			}
			i = i == contents.size() - 1 ? 0 : i + 1;
		} while (i != start);
		return null;
	}
	
	public boolean contains(K key) {
		ClEntry<K, V> entry = getEntry(key);
		return entry != null;
	}
	
	public V get(K key) {
		ClEntry<K, V> entry = getEntry(key);
		return entry == null ? null : entry.val;
	}
	
	public void put(K key, V val) {
		int start = key.hashCode() % contents.size();
		int i = start;
		do {
			ClEntry<K, V> ent = contents.get(i); 
			if (ent == null || ent.isDeleted) {
				contents.set(i, new ClEntry<K, V>(key, val));
				return;
			}
			i = i == contents.size() - 1 ? 0 : i + 1;
		} while (i != start);
		throw new AssertionError("Hashtable is full"); // no resize
	}
	
	public V remove(K key) {
		int start = key.hashCode() % contents.size();
		int i = start;
		do {
			ClEntry<K, V> ent = contents.get(i);
			if (ent == null)
				return null;
			if (ent.isDeleted)
				continue;
			if (ent.key.equals(key)) {
				V val = ent.val;
				ent.isDeleted = true;
				ent.key = null;
				ent.val = null;
				return val;
			}
			i = i == contents.size() - 1 ? 0 : i + 1;
		} while(i != start);
		return null;
	}
	
	public static void main (String[] args) {
		HashClosed<String, String> tbl = new HashClosed<String, String>(10);
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

class ClEntry<K, V> {
	public K key;
	public V val;
	public boolean isDeleted;
	
	public ClEntry(K key, V val) {
		this.key = key;
		this.val = val;
	}
}