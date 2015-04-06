import java.io.*;
import java.util.*;

public class RectangleIntersection {
	public StringTokenizer strtok;
	public BufferedReader inr;
	public PrintWriter out;

	public static void main(String[] args) {
		new RectangleIntersection().run();
	}

	public static final String taskname = "rectangles";

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
		// Any rectangle with sides parallel to axes can be uniquely described by 2 points.
		// Here, leftmost&bottommost and rightmost&topmost points are expected.
		// Expected input format ('rectangles.in'):
		// <x-first> <y-first> <x-second> <y-second>: integers
		// There should be 3 lines with the above formatting 
		int xl = nextInt(), yl = nextInt(), xr = nextInt(), yr = nextInt();
		Rectangle r = new Rectangle(xl, yl, xr, yr);
		for (int i = 0; i < 2; i++) {
			xl = nextInt(); yl = nextInt(); xr = nextInt(); yr = nextInt();
			r = r.intersect(new Rectangle(xl, yl, xr, yr));
		}
		if (r.empty) {
			out.print("empty");
		}
		else {
			out.printf("(%d, %d) (%d, %d)", r.xl, r.yl, r.xr, r.yr); 
		}
	}
}

class Rectangle {
	int xl, yl, xr, yr;
	boolean empty;
	
	public Rectangle(int xl, int yl, int xr, int yr) {
		this.xl = xl;
		this.yl = yl;
		this.xr = xr;
		this.yr = yr;
		this.empty = (xl >= xr) || (yl >= yr);
	}
	
	public Rectangle intersect(Rectangle r) {
		int nxl = Math.max(this.xl, r.xl);
		int nyl = Math.max(this.yl, r.yl);
		int nxr = Math.min(this.xr, r.xr);
		int nyr = Math.min(this.yr, r.yr);
		Rectangle res = new Rectangle(nxl, nyl, nxr, nyr);
		return res;
	}
}