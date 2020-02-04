#!/home/fyang/.virtualenvs/base/bin/python
# !encoding:utf8

from pyperclip import copy, paste
from optparse import OptionParser
from utils import __pwd_input
from utils import *
from db import *
from log import *
from os import path


__config = {
    "user": "litepwd",
    "password": None,
    "target": None,
    "key": None,
    "is_clip": True,
    "length": 16,
    "data": None,
    "out": 1,
}

__mode = {
    "set_default": False,
    "list_users": False,
    "register": False,
    "update": False,
    "backup": False,
    "shell": False,
    "random": False,
    "set_account_password": False,
}


def connect() -> SqlcipherExecutor:
    pwd = __pwd_input("password:")
    # 通过文件检查用户是否第一次登录
    _init = False
    if not path.isfile(f".db/{__config['user']}"):
        _init = True
        repeat_pwd = __pwd_input("repeat:")
        if pwd != repeat_pwd:
            print_red("incorrect input! please try again.")
            exit(0)
    pwd_hash = gen_hash(__config['user'], pwd)
    db = f".db/{__config['user']}"
    try:
        sqlcipher = SqlcipherExecutor(db, pwd_hash, debug=True)
        if _init:
            print_cyan("[*] init db...")
            print_cyan("[*] successfully!")
            while True:
                choose = input("do you want read clipboard?[Y/n]:")
                if choose == '' or choose.startswith('y') or choose.startswith('Y'):
                    # __config['target'] = paste()
                    break
                elif choose.startswith("N") or choose.startswith("n"):
                    print("bye~")
                    exit(0)
                print_error("incorrect input! please try again.")
        return sqlcipher
    except SqlcipherExecutor.SqlcipherException:
        print(TERMINAL_COLORS['RED'], "Login Failed!", TERMINAL_COLORS['RESET'])
        print("please check your password or account.")
        exit(0)
    except Exception as e:
        print_error(e)


def check() -> bool:
    mode_count = 0
    for _ in __mode.values():
        mode_count += 1 if _ else 0
    return mode_count < 2


def init(options):

    # init __config
    if options.display:
        __config['is_clip'] = False
    if options.list_users:
        __mode['list_users'] = True
    if options.register:
        __mode['register'] = True
    if options.random:
        __mode['random'] = True
    if options.user:
        __config['user'] = options.user
    if options.set_default:
        __mode['set_default'] = True
    if options.update:
        __mode['update'] = True
    if options.backup:
        __mode['backup'] = True
    if options.length:
        if options.length < 8 or options.length > 64:
            print(f"{TERMINAL_COLORS['RED']} length out of range: 8-64!{TERMINAL_COLORS['RESET']}")
            print(ERROR_MSG)
            exit(0)
        __config["length"] = options.length
    if options.new_password:
        __mode['set_account_password'] = True
    if options.is_shell:
        __mode["shell"] = True


def option_handle():
    usage = "usage: %prog mode:-[l|r|s|u|b|c|-set-password] arg"
    opt_parser = OptionParser(usage)
    opt_parser.add_option(  # 控制是否在终端打印
        "-d", "--display",
        action="store_true",
        dest="display",
        help=f"{TERMINAL_COLORS['RED']}Warning{TERMINAL_COLORS['RESET']}: display your password in terminal."
    )
    opt_parser.add_option(
        "-l", "--list",
        action="store_true",
        dest="list_users",
        help="List all registered user and exit."
    )
    opt_parser.add_option(
        "-r", "--register",
        action="store_true",
        dest="register",
        help="register one account to db."
    )
    opt_parser.add_option(
        "--random",
        action="store_true",
        dest="random",
        help="Generate random string. default length is 16. use --length to custom length."
    )
    opt_parser.add_option(
        "-a", "--account",
        dest="user",
        help="using this account."
    )
    opt_parser.add_option(
        "-s", "--set-default",
        action="store_true",
        dest="set_default",
        help="set default account."
    )
    opt_parser.add_option(
        "-u", "--update",
        action="store_true",
        dest="update",
        help="update password to db."
    )
    opt_parser.add_option(
        "-b", "--backup",
        action="store_true",
        dest="backup",
        help="backup your all password to file.example: litepwd -b password[.txt/.xls/.cvs/.json/.xml]"
    )
    opt_parser.add_option(
        "--length",
        dest="length",
        help="custom length. min:8-max:64"
    )
    opt_parser.add_option(
        "--set-password",
        action="store_true",
        dest="new_password",
        help="update account password."
    )
    opt_parser.add_option(
        "-c", "--command",
        action="store_true",
        dest="is_shell",
        help="get into the shell."
    )
    (options, args) = opt_parser.parse_args()
    if len(args) > 1:
        opt_parser.error(ERROR_MSG)
        exit(0)
    if len(args) == 1:
        __config['target'] = args[0]
    else:
        __config['target'] = paste()
    return options


def main():
    options = option_handle()
    init(options)
    if not check():
        print(TERMINAL_COLORS['RED'], "incorrect option!", TERMINAL_COLORS['RESET'])
        print("usage: -[l|r|s|u|b|c|-set-password] arg")
        exit(0)
    sqlcipher = connect()
    if not sqlcipher:
        print(TERMINAL_COLORS['RED'], "Unknown error.", TERMINAL_COLORS['RESET'])
        exit(0)


if __name__ == '__main__':
    main()
