/**
 * Created by wesley150 on 29/08/17.
 */
import com.restfb.DefaultFacebookClient;


public class Autenticadora extends DefaultFacebookClient{

    private String token;

    public Autenticadora(String appId, String appSecret) {
        AccessToken accessToken = this.obtainAppAccessToken(appId, appSecret);
        token = accessToken.getAccessToken();
    }
    public String gettoken(){
        return token;
    }


}