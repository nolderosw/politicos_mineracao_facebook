import org.json.JSONArray;
import org.json.JSONObject;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

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
            final Document document = Jsoup.connect("https://www.fb.com/"+id_user)
                    .userAgent("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0")
                    .header("Accept-Language", "en")
                    .header("Accept-Encoding","gzip,deflate,sdch").get();
           // final Document document = Jsoup.connect("https://www.fb.com/"+id_user).get();
            this.pagina = document;
            return true;
        }
        catch (Exception e){
            return false;
        }

    }
    public Boolean filtra_pagina(String tag){
        try {
            pagina_filtrada = pagina.getElementsByTag(tag).get(3).data();
            userJson = new JSONObject(pagina_filtrada);
            return true;
        }
        catch (Exception e){
            return false;
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
