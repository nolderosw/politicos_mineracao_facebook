/**
 * Created by wesley150 on 14/08/17.
 */
import com.restfb.Connection;
import com.restfb.FacebookClient;
import com.restfb.types.Comment;

public class SearchComments {
    private FacebookClient fbClient;
    private Connection<Comment> results;

    public SearchComments(FacebookClient fbClient){
        this.fbClient = fbClient;
    }
    public void createCommentConnection(String postID){
        Connection<Comment> results = fbClient.fetchConnection(postID+"/comments",Comment.class);

        this.results = results;
    }
    public Connection<Comment> getResults(){
        return results;
    }

}
