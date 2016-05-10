package ipgw.neu.androidneuloger;


import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import com.material.widget.FloatingEditText;
import com.material.widget.PaperButton;
import com.squareup.okhttp.Request;
import com.zhy.http.okhttp.OkHttpUtils;
import com.zhy.http.okhttp.callback.StringCallback;



import butterknife.BindView;
import butterknife.ButterKnife;

public class MainActivity extends AppCompatActivity implements View.OnClickListener{

     @BindView(R.id.user_name_input) FloatingEditText mUsername;
     @BindView(R.id.password_input) FloatingEditText mPassword;
     @BindView(R.id.login_on_button) PaperButton mLoginOnButton;
     @BindView(R.id.login_off_button) PaperButton mLoginOffButton;

     private SharedPreferences mSharedPreferences;
     private SharedPreferences.Editor mEditor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ButterKnife.bind(this);

        Log.i("Activity","onCreate");

        mSharedPreferences = getSharedPreferences("login_info",MODE_PRIVATE);
        mEditor = mSharedPreferences.edit();
        mLoginOffButton.setOnClickListener(this);
        mLoginOnButton.setOnClickListener(this);
        mUsername.setText(mSharedPreferences.getString("username",""));
        mPassword.setText(mSharedPreferences.getString("password",""));
    }



    @Override
    public void onClick(View v) {
        switch (v.getId()){
            case R.id.login_on_button:
                if(isInputEmpty()) break;
                OkHttpUtils.post().url("http://ipgw.neu.edu.cn:801/srun_portal_pc.php?ac_id=1&")
                        .addParams("action", "login").addParams("ac_id", "1").addParams("user_ip","")
                        .addParams("nas_ip","").addParams("user_mac","").addParams("url","")
                        .addParams("username",mUsername.getText().toString())
                        .addParams("password",mPassword.getText().toString())
                        .addParams("save_me","0")
                        .build()
                        .execute(new StringCallback() {
                            @Override
                            public void onError(Request request, Exception e) {
                                e.printStackTrace();

                            }
                            @Override
                            public void onResponse(String response) {
                    //            Log.i("Login_Info",response);
                                if(response.contains("网络已连接")){
                                    showInfo("网络已连接");
                                    mEditor.putString("username",mUsername.getText().toString()).commit();
                                    mEditor.putString("password",mPassword.getText().toString()).commit();
                                } else if(response.contains("密码错误")){
                                    showInfo("密码错误");
                                } else if(response.contains("用户不存在")){
                                    showInfo("用户名错误");
                                }
                            }
                        });
                break;
            case R.id.login_off_button:
                if(isInputEmpty()) break;
                OkHttpUtils.post().url("http://ipgw.neu.edu.cn:803/include/auth_action.php")
                        .addParams("action", "logout")
                        .addParams("username",mUsername.getText().toString())
                        .addParams("password",mPassword.getText().toString())
                        .addParams("ajax","1")
                        .build()
                        .execute(new StringCallback() {
                            @Override
                            public void onError(Request request, Exception e) {
                                e.printStackTrace();

                            }
                            @Override
                            public void onResponse(String response) {
                                Log.i("Login_out_Info",response);
                                if(response.contains("网络已断开")){
                                    showInfo("网络已断开");
                                    mEditor.putString("username",mUsername.getText().toString()).commit();
                                    mEditor.putString("password",mPassword.getText().toString()).commit();
                                } else if(response.contains("您似乎未曾连接到网络...")){
                                    showInfo("您似乎未曾连接到网络...");
                                } else if(response.contains("注销失败：Password is error.")){
                                    showInfo("密码错误");
                                }
                            }
                        });
        }
    }


    private boolean isInputEmpty(){
       if(TextUtils.isEmpty(mUsername.getText())){
           showInfo("用户名不能为空");
           return true;
       }
        if(TextUtils.isEmpty(mPassword.getText())){
            showInfo("密码不能为空");
            return true;
        }
        return false;
    }


    private void showInfo(String info){
        Toast.makeText(MainActivity.this,info,Toast.LENGTH_SHORT).show();
    }

}
