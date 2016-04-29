#! /usr/local/bin/node
var http = require('http')
  , querystring = require('querystring');

var user = {
  username: "", // 添加用户名
  password: ""  // 添加密码
};

var LoginData = querystring.stringify({
  action: "login",
  ac_id: "1",
  user_ip:"",
  nas_ip: "",
  user_mac: "",
  url: "",
  username: user.username,
  password: user.password
})
  , LogoutData = querystring.stringify({
  "action": "logout",
  "username": user.username,
  "password": user.password,
  "ajax": "1"
});

var LoginOptions = {
  hostname: "ipgw.neu.edu.cn",
  port: "801",
  path: "/srun_portal_pc.php?ac_id=1&",
  method: "POST",
  headers: {
    "Origin": "http://ipgw.neu.edu.cn:801",
    "Referer": "http://ipgw.neu.edu.cn:801/srun_portal_pc.php?ac_id=1&",
    "Content-Length":LoginData.length,
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36"
  }
}
  , LogoutOptions = {
  hostname: "ipgw.neu.edu.cn",
  port: "801",
  path: "/include/auth_action.php",
  method: "POST",
  headers: {
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Accept": "*/*",
    "Host": "ipgw.neu.edu.cn:801",
    "Connection": "keep-alive",
    "User-Agent": "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length":LogoutData.length,
    "Referer": "http://ipgw.neu.edu.cn:802/srun_portal_pc.php?ac_id=1&url=",
    "Origin": "http://ipgw.neu.edu.cn:802",
    "X-Requested-With": "XMLHttpRequest"
  }
};

var req = http.request(LoginOptions, function(res) {
  res.setEncoding("utf8");
  res.resume();
  res.on("end", function(){
    console.log("登陆成功!");
    var cookies = res.headers["set-cookie"];
    console.log("--------------------------");
    console.log("是否断开连接?(Enter)");
    process.stdin.on("data", function(data){
      if(data.toString() == "\n" || data.toString() == "\r\n") {
        // 断开连接
        var cookiee = cookies[0].split("; ")[0];
        LogoutOptions.headers["Cookie"] = cookiee;
        var reql = http.request(LogoutOptions, function(res) {
          res.setEncoding("utf8");
          res.on("data", function(data){
            console.log(data);
          });
          res.on("end", function() {
            process.exit(0);
          });
          res.on("error", function(err){
            console.log("断开连接失败!");
            console.log("Error: "+err.message);
          })
        });
        reql.write(LogoutData);
        reql.end();
      }
    })
  });
  res.on("error", function(err) {
    console.log("连接建立失败!");
    console.log("Error: "+err.message);
  })
});

req.write(LoginData);
req.end();

req.on("error", function(err) {
  console.log(err);
});