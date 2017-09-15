
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
    public void createPostConnection(String string){
        Connection<Post> results = fbClient.fetchConnection(string+"/feed",Post.class);

        this.results = results;
    }
    public Connection<Post> getResults(){
        return results;
    }
}
