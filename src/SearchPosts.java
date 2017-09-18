
/**
 * Created by wesley150 on 10/08/17.
 */

import com.restfb.Connection;
import com.restfb.FacebookClient;
import com.restfb.types.Post;

public class SearchPosts {
    private FacebookClient fbClient;
    private Connection<Post> results;

    public SearchPosts(FacebookClient fbClient){
        this.fbClient = fbClient;
    }
    public boolean createPostConnection(String string){
        try {
            Connection<Post> results = fbClient.fetchConnection(string + "/feed", Post.class);

            this.results = results;
            return true;
        }
        catch (Exception e){
            return false;
        }
    }
    public Connection<Post> getResults(){
        return results;
    }
}
