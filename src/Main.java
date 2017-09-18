/**
* Created by wesley150 on 17/09/17.
*/

import com.mongodb.client.MongoCollection;
import com.restfb.DefaultFacebookClient;
import com.restfb.FacebookClient;
import com.restfb.Version;
import com.restfb.types.Comment;
import com.restfb.types.Post;
import com.mongodb.client.MongoDatabase;
import com.mongodb.MongoClient;
import org.bson.Document;

import java.util.*;


public class Main {
    public static void main(String[] args) throws Exception {
        Scanner in = new Scanner( System.in );
        //Definição do mapa de Políticos com suas respectivas páginas oficiais (Objeto de pesquisa)

        Map<String, String> PoliticosMap = new LinkedHashMap();
        ArrayList<String> TempPoliticosArray = new ArrayList<>();
        PoliticosMap.put("Geraldo Alkmin","96033897836");
        PoliticosMap.put("Joao Doria","144112092312277");
        PoliticosMap.put("Aecio Neves","411754008869486");
        PoliticosMap.put("Lula","267949976607343");
        PoliticosMap.put("Jair Bolsonaro","211857482296579");
        PoliticosMap.put("Marina Silva","126351747376464");
        PoliticosMap.put("Ciro Gomes","1216504185136925");
        PoliticosMap.put("Michel Temer","435464776514810");
        PoliticosMap.put("Alvaro Dias","199599520097304");

        System.out.println("Escolha um dos políticos disponíveis para criação da base de dados:");
        int i = 1;
        for(String key: PoliticosMap.keySet()){
            System.out.println(i+" - "+ key);
            TempPoliticosArray.add(key);
            i++;
        }

        int Itemp_politico;
        String Stemp_politico;

        Itemp_politico = in.nextInt();
        Stemp_politico = TempPoliticosArray.get(Itemp_politico-1);

        //Pegando o Token de acesso

        Autenticadora autenticadora = new Autenticadora("1788401691451796","968d4a0564aa0ee349356b9b194dc945");

        FacebookClient fbClient = new DefaultFacebookClient(autenticadora.gettoken(), Version.LATEST);

        //mineração

        SearchPosts posts = new SearchPosts(fbClient);

        if(posts.createPostConnection(PoliticosMap.get(Stemp_politico))){
            System.out.println("Conexão com Página do Político " + Stemp_politico + " ocorrida com Sucesso");

            //conectando-se com BD
            MongoClient mongo = new MongoClient("localhost", 27017);
            MongoDatabase database = mongo.getDatabase("Politicos_Pages");

            //verificando se existe a collection relacionada ao politico selecionado caso n tenha, cria-se
            try {
                database.getCollection(Stemp_politico);
            }
            catch (Exception e){
                database.createCollection(Stemp_politico);
            }
            MongoCollection<Document> collection = database.getCollection(Stemp_politico);


            //Cria uma data limite para pegar os posts
            Calendar data_comparacao = Calendar.getInstance();
            data_comparacao.set(Calendar.YEAR, 2016);
            data_comparacao.set(Calendar.MONTH, Calendar.JANUARY);
            data_comparacao.set(Calendar.DAY_OF_MONTH, 1);
            Boolean flag_post_velho = false;

            //mineração de posts
            System.out.println("Criando Base de Dados...");
            for (List<Post> postPage: posts.getResults()) {
                for (Post aPost : postPage) {
                    if (aPost.getCreatedTime().before(data_comparacao.getTime())) {
                        System.out.println("POST ANTES DE 2016 DETECTADO");
                        flag_post_velho = true;
                        System.out.println("Base de dados criada!");
                        break;
                    }
                    boolean document_find = false;
                    for (Document id : collection.find()) {
                        if (id.get("Id").equals(aPost.getId())) {
                            document_find = true;
                        }
                    }

                    //se o documento não existir, escreva ele no BD
                    if(!document_find){
                        Document post_doc = new Document("Mensagem", aPost.getMessage())
                                .append("Id", aPost.getId())
                                .append("Data", aPost.getCreatedTime())
                                .append("Url", "fb.com/" + aPost.getId());


                        //mineração de comentários
                        SearchComments comments = new SearchComments(fbClient);
                        ArrayList <Document> array_comments = new ArrayList<>();
                        if (comments.createCommentConnection(aPost.getId())) {
                            for (List<Comment> commentPage : comments.getResults()) {
                                for (Comment comment : commentPage) {
                                    Document comments_doc = new Document("Mensagem", comment.getMessage())
                                            .append("Usuario", comment.getFrom().getName())
                                            .append("Data", comment.getCreatedTime())
                                            .append("Link", "fb.com/"+comment.getId());
                                    array_comments.add(comments_doc);
                                }
                            }
                        }
                        else {
                            System.out.println("Erro ao ler um comentário do POST de ID: " + aPost.getId());
                        }
                        post_doc.append("Comentarios", array_comments);
                        collection.insertOne(post_doc);
                    }

                }
                if(flag_post_velho){
                    break;
                }
            }
        }
        else{
            System.out.println("Erro ao se conectar com a página do político selecionado");
        }
    }
}



//Scrap User
//Problema da IA do facebook limitar após um numero de requisição
/*
SearchUserInfo user = new SearchUserInfo(comment.getFrom().getId(),autenticadora.gettoken());
if(user.ConnectUser()){
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
        System.out.println("\n");
        cont_user_filtrado++;
    }
    else{
        System.out.println("Impossível obter página filtrada do usuário de ID " + comment.getFrom().getId() + "\n");
        user.printa_pagina_use();
        cont_user_erro++;

    }
}
else{
    System.out.println("Pagina do usuário NAO encontrada");
    cont_user_erro++;
}
*/