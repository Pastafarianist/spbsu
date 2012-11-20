import java.io.*;
import java.util.*;
import java.util.regex.*;

public class RegexEmailPhone {
	public StringTokenizer strtok;
	public BufferedReader inr;
	public PrintWriter out;

	public static void main(String[] args) {
		new RegexEmailPhone().run();
	}

	public static final String taskname = "regex-email-phone";

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

	// Solution

	public void solve() throws NumberFormatException, IOException {
		// Expected input format ('regex-email-phone.in'):
		// <number of test cases>: integer
		// <test cases, separated by line breaks> 
		String s_email = "[A-Za-z0-9]+@[A-Za-z0-9]+\\.[A-Za-z]+";
		String s_phone = "(8|\\+7)\\d{10,10}";
		String s_both = String.format("(%s\\s+%s)|(%s\\s+%s)", s_email, s_phone, s_phone, s_email);
		Pattern p = Pattern.compile(s_both);
		int n = nextInt();
		for (int i = 0; i < n; i++) {
			String s = inr.readLine();
			Matcher m = p.matcher(s);
			System.out.println(m.matches() ? "good" : "bad");
		}
	}
}