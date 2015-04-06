import java.io.*;
import java.util.*;

public class MatrixMultiplication {
	public StringTokenizer strtok;
	public BufferedReader inr;
	public PrintWriter out;

	public static void main(String[] args) {
		new MatrixMultiplication().run();
	}

	public static final String taskname = "matrixmult";

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
		// Expected input format in file 'matrixmult.in':
		// <matrix height> <matrix width>: integers
		// <matrix>: [height] rows, [width] columns, integers
		// <vector>: [width] integers
		// Crashes if too few values
		int h = nextInt();
		int w = nextInt();
		int[][] values_matrix = new int[h][w];
		for (int y = 0; y < h; y++) {
			for (int x = 0; x < w; x++) {
				values_matrix[y][x] = nextInt();
			}
		}
		int[][] values_vector = new int[w][1];
		for (int k = 0; k < w; k++) {
			values_vector[k][0] = nextInt();
		}
		Matrix m = new Matrix(values_matrix);
		Matrix v = new Matrix(values_vector);
		Matrix r = m.mul(v);
		out.println(r);
	}
}


class Matrix {
	int[][] values;
	int height, width;
	
	public Matrix(int[][] values) {
		this.values = values;
		this.height = values.length;
		this.width = values[0].length;
	}
	
	public Matrix mul(Matrix m) {
		if (this.width != m.height) {
			throw new IllegalArgumentException("Width of the left matrix does not match the height of the right matrix.");
		}
		int[][] result = new int[this.height][m.width];
		for (int y = 0; y < this.height; y++) {
			for (int x = 0; x < m.width; x++) {
				result[y][x] = 0;
				for (int k = 0; k < this.width; k++) {
					result[y][x] += this.values[y][k] * m.values[k][x];
				}
			}
		}
		return new Matrix(result);
	}
	
	public String toString() {
		StringBuilder sb = new StringBuilder();
		for (int y = 0; y < this.height; y++) {
			for (int x = 0; x < this.width; x++) {
				sb.append(this.values[y][x]);
				sb.append(' ');
			}
			sb.append('\n');
		}
		return sb.toString();
	}
}