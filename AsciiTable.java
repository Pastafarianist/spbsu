import java.io.*;

public class AsciiTable {
	public static void main(String[] args) throws IOException {
		PrintWriter out = new PrintWriter(new FileWriter("ascii.txt"));
		out.print("   |");
		String hex = "0123456789abcdef";
		for (int i = 0; i < 16; i++) {
			out.printf(" %c |", hex.charAt(i));
		}
		out.println();
		// ASCII is actually defined only for values in [0..127]
		for (int i = 0; i < 8; i++) {
			out.printf(" %c |", hex.charAt(i));
			for (int j = 0; j < 16; j++) {
				int c = i * 16 + j;
				if (c == 9 || c == 10 || c == 13) {
					c = (char)'?';
				}
				out.printf(" %c |", c);
			}
			out.println();
		}
		out.flush();
		out.close();
	}

}
