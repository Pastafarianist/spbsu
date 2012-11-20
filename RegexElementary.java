import java.util.regex.*;

public class RegexElementary {
	static Pattern p1, p2, p3, p4, p5, p6;
	
	public static boolean ex1(String s) {
		return p1.matcher(s).matches();
	}
	
	public static boolean ex2(String s) {
		return p2.matcher(s).matches();
	}
	
	public static boolean ex3(String s) {
		return p3.matcher(s).matches();
	}
	
	public static String ex4(String s) {
		return p4.matcher(s).replaceAll(" ");
	}
	
	public static String ex5(String s) {
		return p5.matcher(s).replaceAll("<b>$1</b>");
	}
	
	public static String ex6(String s) {
		return p6.matcher(s).replaceAll("<mytag>$1</mytag>");
	}
	
	public static void main(String[] args) {
		p1 = Pattern.compile("\\d{1,239}");
		p2 = Pattern.compile("[A-Za-z+_-]{5,20}");
		p3 = Pattern.compile("\\.(.)\\1{3,}\\.");
		p4 = Pattern.compile(" +");
		p5 = Pattern.compile("\\b(word)\\b", Pattern.CASE_INSENSITIVE);
		p6 = Pattern.compile("<title>(.*)</title>", Pattern.CASE_INSENSITIVE);
		
		System.out.println(ex5("word Word wOrD WORD wordd wword"));
		System.out.println(ex6("<html><head><title>aaa</title></head><body><p>bbb</p></body></html>"));
	}
}
