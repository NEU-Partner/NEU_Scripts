#!/usr/bin/env python
import pickle
import sys
import getopt

try:
    import requests
except ImportError:
    SystemExit("Python package 'requests' required.\nPlease try 'pip install requests' and try again.")

cookie_store_file = "cookie.txt"


def logout(username: str, password: str) -> str:
    """
    logout all connections within given username and password
    :param username: username str
    :param password: password str
    :return: message str
    """
    cookie = pickle.load(open(cookie_store_file, "rb"))
    url = r"http://ipgw.neu.edu.cn:801/include/auth_action.php"
    headers = {
        "Host": "ipgw.neu.edu.cn:801",
        "Connection": "keep-alive",
        "Content-Length": "61",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "*/*",
        "Origin": "http://ipgw.neu.edu.cn:801",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "DNT": "1",
        "Referer": "http://ipgw.neu.edu.cn:801/srun_portal_pc.php?ac_id=1&",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en",
        "Cookie": str(cookie)
    }
    data = {
        "action": "auto_logout",
        "usernanme": username,
        "password": password,
        "ajax": "1",
    }
    rsp = requests.post(url, data=data, headers=headers)
    return rsp.content


def check(username: str, password: str) -> str:
    """
    check current account status, like used quota
    :param username: username str
    :param password: password str
    :return: the raw status str
    """
    cookie = pickle.load(open(cookie_store_file, "rb"))
    url = r"http://ipgw.neu.edu.cn:801/include/auth_action.php?k=26907"
    headers = {
        "Host": "ipgw.neu.edu.cn:801",
        "Connection": "keep-alive",
        "Content-Length": "32",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "*/*",
        "Origin": "http://ipgw.neu.edu.cn:801",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "DNT": "1",
        "Referer": "http://ipgw.neu.edu.cn:801/srun_portal_pc.php?ac_id=1&",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en",
        "Cookie": str(cookie)
    }
    data = {
        "action": "get_online_info",
        "key": 26907,
    }
    rsp = requests.post(url, data=data, headers=headers)
    return rsp.text


def login(username: str, password: str) -> str:
    """
    login with username and password
    :param username: username str
    :param password: password str
    :return: message str
    """
    url = r"http://ipgw.neu.edu.cn:804/srun_portal_pc.php?ac_id=1&"
    headers = {
        "Host": "ipgw.neu.edu.cn:804",
        "Connection": "keep-alive",
        "Content-Length": "103",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Origin": "http://ipgw.neu.edu.cn:804",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "DNT": "1",
        "Referer": "http://ipgw.neu.edu.cn:804/srun_portal_pc.php?ac_id=1&",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en",

    }
    data = {
        "action": "login",
        "ac_id": "1",
        "user_ip": "",
        "nas_ip": "",
        "user_mac": "",
        "url": "",
        "save_me": "0",
        "username": username,
        "password": password,
    }
    rsp = requests.post(url, data=data, headers=headers)
    cookie = rsp.cookies
    pickle.dump(cookie, open(cookie_store_file, 'wb'))
    return "登录成功."


def get_config():
    '''get configs from command line'''
    config = {}
    args, args2 = getopt.getopt(sys.argv[1:], "hc:u:p:", [])
    for k, v in args:
        if k == "-c":
            config["command"] = v
        elif k == "-u":
            config["username"] = v
        elif k == "-p":
            config["password"] = v
        else:
            raise Exception("Unknown option: {}".format(k))
    return config


def check_config(config: dict):
    '''check configs'''
    if "username" not in config:
        SystemExit("username required!")
    if "password" not in config:
        SystemExit("password required!")
    if "command" not in config:
        SystemExit("command required!")
    return config


def main():
    config = check_config(get_config())
    result = ""
    if config["command"] == "login":
        result = login(config["username"], config["password"])
    elif config["command"] == "logout":
        result = logout(config["username"], config["password"])
    elif config["command"] == "status":
        result = check(config["username"], config["password"])
    print(result)


if __name__ == '__main__':
    main()
