#!/home/fyang/.virtualenvs/base/bin/python
# ! encoding:utf8


from db import *
from hashlib import pbkdf2_hmac
import binascii
import base64
from utils import *
from utils import __pwd_input, __user_choose
from log import *
from litepwd import *
import subprocess


def t() -> list:
    return [dict()]


def main():
    pass


if __name__ == '__main__':
    # sqlcipher_login("demo.db", "demo1")
    # sqlcipher = SqlcipherExecutor("/bin/demo.db", "demo")
    # print(gen_hash("litepwd", 'demo'))
    # main() 6e4eaf0f1179a7f8de4d0fb991cd9d48f5bbf274bba6be7eb9f45c2e903731be
    main()
    # print(gen_password(16))
    # ipt = getche()
    # print(ipt)
    # res = __user_choose([
    #         "www.baidu.com",
    #         "www.github.com",
    #         "www.google.com",
    #         "api.fyangami.com.cn",
    #         "fyangami.org",
    # ])
    # print(res)
    # print(type(res))
    # __pwd_input("password:")
    # print(SqlcipherExecutor('litepwd', "123", debug=True).insert(name="'fyang"))
    # with open("./.db/user.default", "r+") as f:
    #     user = f.readline()
    #     print(type(user))
