import org.json.JSONArray;
import org.json.JSONObject;
import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

/**
 * Created by wesley150 on 11/09/17.
 */
public class SearchUserInfo {
    private Collection<JSONArray> CollectionTrabalhos = new ArrayList<>();
    private Collection<JSONObject> CollectionEnderecos = new ArrayList<>();
    private List <String> Enderecos = new ArrayList<>();
    private List <String> Trabalhos = new ArrayList<>();
    private String Nome;
    private String Cargo;
    private String id_user;
    private Document pagina;
    private String pagina_filtrada;
    private JSONObject userJson;
    private String fb_token;

    public SearchUserInfo(String id_user, String fb_token){
        this.id_user = id_user;
        this.fb_token = fb_token;
    }

    public boolean ConnectUser(){
        try {
            //Manda um get pra pegar o cookie de uma requisição de login
            Connection.Response reachPageInitially = Jsoup.connect("https://www.facebook.com/login.php?login_attempt=1")
                    .method(Connection.Method.GET)
                    .execute();
            //Da um post com minhas credenciais de usuario e senha
            Connection.Response res = Jsoup.connect("https://www.facebook.com/login.php?login_attempt=1")
                    .data("email", "wesley150wow@gmail.com", "pass", "741wesley")
                    .method(Connection.Method.POST)
                    .cookies(reachPageInitially.cookies())
                    .execute();

            //Cria um documento temporario com a intenção de pegar o verdadeiro nome do usuario
            final Document document_temp = Jsoup.connect("https://www.fb.com/"+id_user).cookies(res.cookies()).cookies(reachPageInitially.cookies()).userAgent("Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0").referrer("http://www.google.com").get();
            //Element temp1 = document_temp.getElementsByTag("noscript").get(0);
            //Elements temp2 = document_temp.getElementsByTag("script");
            //Element temp3 = document_temp.getElementsByTag("script").get(36);
            //System.out.print(temp2);
            //System.out.println(temp1);
            //System.out.println(temp3);
            this.pagina = document_temp;

            //Finalmente cria uma conexao com a pagina do usuario pelo seu nome de usuario verdadeiro
            //final Document document = Jsoup.connect("https://www.fb.com"+temp1.getElementsByTag("meta").get(0).toString().split(";")[1].split("=")[1].split("\\?")[0]).get();
            //this.pagina = document;
            return true;
        }
        catch (Exception e){
            return false;
        }

    }
    public void printa_pagina_use(){
        Elements temp = pagina.getElementsByTag("script");
        System.out.println(pagina);

    }
    public Boolean filtra_pagina(String tag){
        try {
            pagina_filtrada = pagina.getElementsByTag(tag).get(36).data();
            userJson = new JSONObject(pagina_filtrada);
            return true;
        }
        catch (Exception e){
            try {
                pagina_filtrada = pagina.getElementsByTag(tag).get(27).data();
                userJson = new JSONObject(pagina_filtrada);
                return true;
            }
            catch (Exception j){
                return false;
            }
        }
    }

    public String getPagina_filtrada(){
        return pagina_filtrada;
    }

    public JSONObject getUserJson(){
        return userJson;
    }

    public List getEndereco(){
        try {
            CollectionEnderecos.clear();
            CollectionEnderecos.add((JSONObject) userJson.get("address"));
            for (JSONObject objects : CollectionEnderecos) {
                Enderecos.add((String) objects.get("addressLocality"));
            }
        }
        catch (Exception e){
            Enderecos.add("Vazio");
        }
        return Enderecos;
    }

    public List getTrabalho(){
        try {
            CollectionTrabalhos.clear();
            CollectionTrabalhos.add((JSONArray) userJson.get("affiliation"));
            for (JSONArray objects : CollectionTrabalhos) {
                for (int i = 0; i < objects.length(); i++) {
                    JSONObject temp_json = (JSONObject) objects.get(i);
                    Trabalhos.add((String) temp_json.get("name"));
                }
            }
        }
        catch (Exception e){
            Trabalhos.add("Vazio");
        }
        if(Trabalhos.size() <= 0){
            Trabalhos.add("Vazio");
        }
        return Trabalhos;
    }


    public String getNome(){
        try {
            Nome = (String) userJson.get("name");
            return Nome;
        }
        catch (Exception e){
            return "Vazio";
        }
    }

    public String getCargo(){
        try{
            Cargo = (String) userJson.get("jobTitle");
            return Cargo;
        }
        catch (Exception e){
            return "Vazio";
        }
    }
    public Document getPagina(){
        return pagina;
    }
}
