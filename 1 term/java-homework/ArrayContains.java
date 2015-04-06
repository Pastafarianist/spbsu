import java.io.*;
import java.util.*;

public class ArrayContains {
	public StringTokenizer strtok;
	public BufferedReader inr;
	public PrintWriter out;

	public static void main(String[] args) {
		new ArrayContains().run();
	}

	public static final String taskname = "contains";

	public void run() {
		Locale.setDefault(Locale.US);
		try {
			inr = new BufferedReader(new FileReader(taskname + ".in"));
			out = new PrintWriter(new FileWriter(taskname + ".out"));
			solve();
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(9000);
		} finally {
			out.flush();
			out.close();
		}
	}

	public String nextToken() throws IOException {
		while (strtok == null || !strtok.hasMoreTokens()) {
			strtok = new StringTokenizer(inr.readLine());
		}
		return strtok.nextToken();
	}

	public int nextInt() throws NumberFormatException, IOException {
		return Integer.parseInt(nextToken());
	}

	public long nextLong() throws NumberFormatException, IOException {
		return Long.parseLong(nextToken());
	}

	public double nextDouble() throws NumberFormatException, IOException {
		return Double.parseDouble(nextToken());
	}

	// Solution
	
	public boolean contains(short[] a, short v) {
		for (int i = 0; i < a.length; i++) {
			if (a[i] == v) {
				return true;
			}
		}
		return false;
	}

	public void solve() throws NumberFormatException, IOException {
		// Assuming the array being unordered, hence no binary search.
		// Instead perform a simple bruteforce.
		// Expected input format (in 'contains.in'):
		// <length of array> <element>: integers
		// <array>: space-separated shorts
		int n = nextInt();
		short v = (short)nextInt();
		short[] a = new short[n];
		for (int i = 0; i < n; i++) {
			a[i] = (short)nextInt();
		}
		out.print(contains(a, v) ? "contains" : "does not contain");
	}
}