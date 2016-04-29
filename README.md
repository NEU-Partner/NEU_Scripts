## 介绍
东北大学网站登陆每次都需要输入用户名密码,体验相当之差,没办法,写了点脚本,方便登陆.

## 脚本类型
写了一下语言的脚本:
- python
- node.js

## 使用

### Node.js

1 安装[node.js](https://nodejs.org), 最好安装最新版本

2 拷贝文件
```shell
> git clone https://github.com/NEU-Partner/NEU_Scripts.git
```

3 拷贝文件内的`neu.js`到`home`目录下
```shell
> cp ./NEU-Scripts/neu.js ~/neu.js
```

4 改变`neu.js`的chmod
```shell
> sudo chmod 0777 ~/neu.js
```

5 配置用户名和密码
```
修改neu.js内的内容,在 `user`处添加用户名和密码
```

6 启动脚本
```shell
> ~/neu.js
```