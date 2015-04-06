import java.io.*;
import java.util.*;

public class template {
	public StringTokenizer strtok;
	public BufferedReader inr;
	public PrintWriter out;

	public static void main(String[] args) {
		new template().run();
	}

	public static final String taskname = "template";

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

	public void solve() throws NumberFormatException, IOException {
		
	}
}