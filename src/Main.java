import com.restfb.DefaultFacebookClient;
import com.restfb.FacebookClient;
import com.restfb.Version;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import org.json.*;

public class Main {

    public static void main(String[] args) throws Exception {

        Autenticadora autenticadora = new Autenticadora("1788401691451796","968d4a0564aa0ee349356b9b194dc945");

        FacebookClient fbClient = new DefaultFacebookClient(autenticadora.gettoken(), Version.LATEST);

        //scrap!!!!!!

        SearchUserInfo user = new SearchUserInfo("100000452297269",autenticadora.gettoken());
        if(user.ConnectUser()){
            //System.out.println(user.getPagina());
            if(user.filtra_pagina("script")) {
                System.out.println("Nome: " + user.getNome());
                System.out.println("Cargo: " + user.getCargo());
                System.out.print("Endereço: ");
                for(Object enderecos: user.getEndereco()){
                    System.out.println(enderecos);
                }
                System.out.print("Locais de Trabalho/Estudo: ");
                for(Object trabalhos: user.getTrabalho()){
                    System.out.print(trabalhos+"; ");
                }
            }
            else{
                System.out.println("Impossível obter página filtrada!");

            }
        }
        else{
            System.out.println("Pagina NAO encontrada");
        }

        //mineração

        /*
        Autenticadora autenticadora = new Autenticadora("1788401691451796","968d4a0564aa0ee349356b9b194dc945");

        FacebookClient fbClient = new DefaultFacebookClient(autenticadora.gettoken(), Version.LATEST);

        FacebookClient fbClient2 = new DefaultFacebookClient("EAACEdEose0cBABRE2sRYBzQdZAtHaUDHgJX67ZCWYde1syPCCrOHlNL6RWGIUMMXanBNJKrGCqhU5czJ7FFB4exr3njubv3wq16ZBdqZCtWtVPZCBM3mgm392MZCx7oZAiFhNHF8O1GG6anfO34t7YmxzCMdHyenZATPwY2Oh3CdA13ZA5TI7EUWZAlL51dwZCK2Aw9SovOoRogFwZDZD",Version.LATEST);

        SearchPosts posts = new SearchPosts(fbClient);

        posts.createPostConnection("267949976607343");

        int cont_posts = 0;
        for (List<Post> postPage: posts.getResults()) {
            for (Post aPost : postPage) {
                System.out.println("Post "+ cont_posts);
                System.out.println("Mensagem do Post: " + aPost.getMessage());
                System.out.println("Link do Post: fb.com/" + aPost.getId()+"\n");
                cont_posts ++;
                ids_posts.add(aPost.getId());
            }
        }*/

        //bd

        /*
        Connection c = null;
        try {
            Class.forName("org.sqlite.JDBC");
            c = DriverManager.getConnection("jdbc:sqlite:bd/test.db");
        } catch ( Exception e ) {
            System.err.println( e.getClass().getName() + ": " + e.getMessage() );
            System.exit(0);
        }
        System.out.println("Opened database successfully");
        */
    }
}
