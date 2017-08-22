import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Main {

    public static void main(String[] args) throws Exception {

        /*final Document document = Jsoup.connect("http://www.imdb.com/chart/top").get();

        for (Element row : document.select("table.chart.full-width tr")) {

            final String title = row.select(".titleColumn a").text();
            final String rating = row.select(".imdbRating").text();

            System.out.println(title + " -> Rating: " + rating);
        }*/
        final Document document = Jsoup.connect("https://www.facebook.com/Rafaela.Souza97").get();
        String teste = "script type"+"="+"\"application/ld+json\"";
        //Elements job1 = document.getElementsByTag("script type"+"="+"\"application/ld+json\"");
        Elements job1 = document.getElementsByTag("script");
        Element selection = job1.get(3);
        //System.out.println(teste);
        //System.out.println(document);
        //System.out.println(job1);
        System.out.println(selection);
    }
}
