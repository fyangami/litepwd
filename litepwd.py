#!/home/fyang/.virtualenvs/base/bin/python
# !encoding:utf8

from pyperclip import copy, paste
from optparse import OptionParser
from utils import __pwd_input, __user_choose
from utils import *
from db import *
from log import logger
from os import path
from time import time, sleep
# from shell import LitepwdShell

__config = {
    "user": None,
    "password": None,
    "target": None,
    "input": False,  # 默认从剪切板读取
    "key": None,
    "is_clip": True,
    "length": 16,
    "data": None,
    "out": 1,
    "init": False,
    "group": None,
    "default_user_path": "./.db/user.default"
}

__mode = {
    "set_default": False,   # 设置默认账户
    "list_users": False,   # 列出所有账户
    # "register": False,   # 注册一个账户
    "update": False,  # 更新一个store
    "backup": False,  # 备份数据
    "shell": False,  # 进入shell
    "random": False,  # 获取一个随机字符串
    "set_account_password": False,  # 设置账户密码
    "generate": False,  # 生成密码
    "list_store": False,  # 列出所有store
    "join_group": False,  # 更改store的group字段
}


def init_after():
    while True:
        choose = input("do you want read clipboard to generate password?[Y/n]:")
        if choose == '' or choose.startswith('y') or choose.startswith('Y'):
            # __config['target'] = paste()
            break
        elif choose.startswith("N") or choose.startswith("n"):
            print("bye~")
            exit(0)
        print_red("incorrect input! please try again.")


def connect() -> SqlcipherExecutor:
    pwd = __pwd_input("password:")
    # 通过文件检查用户是否第一次登录
    if not path.isfile(f".db/{__config['user']}"):
        __config['init'] = True
        repeat_pwd = __pwd_input("repeat:")
        if pwd != repeat_pwd:
            error_exit("incorrect input! please try again.")
        # 设置默认用户
        # if not path.exists(".db/user.default"):
        #     with open(".db/user.default", "w") as f:
        #         f.write(__config['user'])
    pwd_hash = gen_hash(__config['user'], pwd)
    db = f".db/{__config['user']}"
    try:
        sqlcipher = SqlcipherExecutor(db, pwd_hash, debug=True)
        return sqlcipher
    except SqlcipherExecutor.SqlcipherException:
        error_exit("Login Failed!\nplease check your password or account.")
    except Exception as e:
        logger.error(e)


def check() -> bool:
    mode_count = 0
    for _ in __mode.values():
        mode_count += 1 if _ else 0
    return mode_count < 2


def init(options):
    # init __config
    if options.is_generate:
        __mode['generate'] = True
    if options.display:
        __config['is_clip'] = False
    if options.list_users:
        __mode['list_users'] = True
    # if options.register:
    #     __mode['register'] = True
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
        try:
            length = int(options.length)
            if length < 8 or length > 64:
                error_exit(f"length out of range: 8-64!\n{ERROR_MSG}")
            __config["length"] = length
        except ValueError:
            error_exit("Input not regular number!")
    if options.new_password:
        __mode['set_account_password'] = True
    if options.is_shell:
        __mode["shell"] = True
    if options.group:
        __config['group'] = options.group
    if options.list_store:
        __mode['list_store'] = True


def option_handle():
    usage = "usage: %prog mode:-[g|l|s|u|b|c|-set-password] arg"
    opt_parser = OptionParser(usage)
    opt_parser.add_option(
        "-g", "--generate",
        action="store_true",
        dest="is_generate",
        help="generate password to arg. use --length"
    )
    opt_parser.add_option(  # 控制是否在终端打印
        "-d", "--display",
        action="store_true",
        dest="display",
        help=f"{TERMINAL_COLORS['RED']}Warning{TERMINAL_COLORS['RESET']}: display your password in terminal."
    )
    opt_parser.add_option(
        "--list-user",
        action="store_true",
        dest="list_users",
        help="List all registered user and exit."
    )
    # opt_parser.add_option(
    #     "-r", "--register",
    #     action="store_true",
    #     dest="register",
    #     help="register one account to db."
    # )
    opt_parser.add_option(
        "--random",
        action="store_true",
        dest="random",
        help="Generate random string. default length is 16. use --length to custom length."
    )
    opt_parser.add_option(
        "-a", "--account",
        dest="user",
        help="using this account (auto create)."
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
        help="backup your all password to file.  example: litepwd -b my_password.txt"
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
        "-c", "--command-line",
        action="store_true",
        dest="is_shell",
        help="get into the shell."
    )
    opt_parser.add_option(
        "--group",
        dest="group",
        help="add to group using same password."
    )
    opt_parser.add_option(
        "-l", "--list-store",
        action="store_true",
        dest="list_store",
        help="list all store data for (default)account."
    )
    # opt_parser.add_option(
    #     "j", "--join",
    #     dest="join_group",
    #     help="join store to group. waring: old password will overwrite!"
    # )
    (options, args) = opt_parser.parse_args()
    if len(args) > 1:
        error_exit(ERROR_MSG)
    if len(args) == 1:
        __config['target'] = args[0]
        __config['input'] = True
    else:
        __config['target'] = paste()
    return options


# 列出所有用户
def list_user():
    files = os.listdir("./.db")
    if not os.path.exists(__config['default_user_path']):
        error_exit("default user not found!")
    _f = open(__config['default_user_path'], "r")
    default_user = _f.readline()
    _f.close()
    for f in files:
        if f != __config['default_user_path'].split("/")[-1]:
            if default_user == f:
                print_green(f" {f} [*]")
            else:
                print(" ", f)


# 更改默认用户
def set_default(shell=False):
    user = __config['target']
    if not os.path.exists(f".db/{user}"):
        error_exit("user does not exist!", shell=shell)
    with open(__config['default_user_path'], "w") as f:
        f.write(user)
    print_green("[*] successfully!")


# # 注册用户
# def register():
#     pass


# 更新某个密码
def update(sqlcipher, shell=False):
    _pwd = gen_password(__config['length'])
    if __config['group']:
        if sqlcipher.update_store_pwd(_pwd, group=__config['group']):
            print("\033[33m [*] using group!\033[0m")
            print_green("[*] successfully!")
        else:
            error_exit("Data not found!", shell=shell)
        __out(__config['group'], _pwd)
    else:
        target = __config['target']
        if not __config['input']:
            target = __get_url(__config['input'])
        # 检查store的group字段是否生效 若生效无法更新
        find = sqlcipher.query_by_name(target)
        if len(find):
            find_all = sqlcipher.query_by_group(find[0]['_group'])
            if len(find_all) > 1:
                error_exit("failed! please using --group to update group password.", shell=shell)
        else:
            error_exit("Data not found!", shell=shell)
        if sqlcipher.update_store_pwd(_pwd, name=target):
            print_green("[*] successfully!")
        else:
            error_exit("Data not found!", shell=shell)
        __out(target, _pwd)


# shell
def _shell(sqlcipher):
    LitepwdShell(user=__config['user'], sqlcipher=sqlcipher, conf=__config).start()
    # shell.get_shell(sqlcipher)


# 获取一个随机字符串
def random():
    print(gen_password())


# 备份
def backup(sqlcipher, shell=False):
    file_name = __config['target']
    if not __config['input']:
        print(" \033[33m[*] File name is empty!")
        print(" [*] use default name:[account].txt\033[0m")
        file_name = __config['user'] if __config['user'] else "litepwd"
        file_name += ".txt"
    all_store = sqlcipher.query_all()
    try:
        with open(file_name, "w+") as f:
            for item in all_store:
                f.write(f"{item['name']}:{item['password']}\n")
    except PermissionError:
        error_exit("Permission denied!", shell=shell)
    except Exception as e:
        logger.error(e)
        error_exit(shell=shell)
    else:
        print_green(" [*] Finished!")


# 更改账户密码
def set_account_password(sqlcipher, shell=False):
    user = __config['user']
    password = __pwd_input("newpassword:")
    repeat = __pwd_input("repeat:")
    if password != repeat:
        error_exit("incorrect input! try again.", shell=shell)
    else:
        pwd_hash = gen_hash(user, password)
        sqlcipher.rekey(pwd_hash)
        print_green("[*] successfully!")


# 列出所有store
def list_store(sqlcipher):
    store_list = sqlcipher.query_all()
    format_print_store(store_list, hidden=True)


# 密码入库
def store(sqlcipher, shell=False):
    if not __config['target']:
        error_exit("Nothing input.", shell=shell)
    if not __config['input']:
        __config['target'] = __get_url(__config['target'])
    password = gen_password(__config['length'])
    if __config['group']:
        # 查询group有无记录
        res = sqlcipher.query_by_group(__config['group'])
        if len(res) > 0:
            password = res[0]['password']
    err = sqlcipher.insert(
        name=__config['target'],
        val=password,
        _group=__config['group'] if __config['group'] else __config['target'],
        create_time=int(time())
    )
    if err:
        logger.error(err)
        if "UNIQUE constraint" in err:
            error_exit("Data already existed!", shell=shell)
        error_exit(shell=shell)
    else:
        __out(__config['target'], password)


def query_password(sqlcipher, shell=False):
    key = __config['target']
    if not __config['input']:
        key = __get_url(key)
    # 先查name
    res = sqlcipher.query_by_name(key)
    size = len(res)
    if size == 1:
        __out(res[0]['name'], res[0]['password'])
        return
    # 后查group
    res = sqlcipher.query_by_group(key)
    size = len(res)
    if size > 0:
        __out(res[0]['name'], res[0]['password'])
        return
    res_find = sqlcipher.query_by_name(key, like=True)
    if not len(res_find):
        error_exit("Data not found!", shell=shell)
    # 将所有选项列出给用户选择
    else:
        choose = __user_choose([item['name'] for item in res_find])
        __out(res_find[choose]['name'], res_find[choose]['password'])


# 拿给c实现吧。。。。
# def user_choose(choose_list: list, label):


def __out(name, password):
    if __config['is_clip']:
        copy(password)
        print_green(f"[*] the password has been copied to the "
                    f"clipboard<{TERMINAL_COLORS['CYAN']}{name}{TERMINAL_COLORS['GREEN']}>.")
    else:
        print_green(f"[*] {TERMINAL_COLORS['CYAN']}{name}"
                    f"{TERMINAL_COLORS['GREEN']} -> password(disappear in 5 second):", end="")
        print(password)
        print(end="")  # fix bug...
        try:
            sleep(5)
        except KeyboardInterrupt:
            pass
        finally:
            print("\033[1A\033[2K")


def __get_url(uri: str):
    ss = uri.split("/")
    # print(ss)
    try:
        url = ss[0]
        if len(ss[0].split(".")) < 2:
            url = ss[2]
        return url
    except IndexError:
        error_exit("input is not uri!")
    # if ss[0].replace(" ", '') == '':


def action(sqlcipher):
    if __mode['list_users']:
        list_user()
    elif __mode['set_default']:
        set_default()
    elif __mode['backup']:
        backup(sqlcipher)
    elif __mode['shell']:
        _shell(sqlcipher)
    elif __mode['random']:
        random()
    elif __mode['set_account_password']:
        set_account_password(sqlcipher)
    elif __mode['generate']:
        store(sqlcipher)
    elif __mode['list_store']:
        list_store(sqlcipher)
    elif __mode['update']:
        update(sqlcipher)
    else:
        query_password(sqlcipher)


def read_default_user():
    if os.path.exists(__config['default_user_path']) is False:
        user = __config['user'] if __config['user'] else "litepwd"
        f = open(__config['default_user_path'], "w")
        f.write(user)
        f.close()
    else:
        f = open(__config['default_user_path'], "r")
        __config['user'] = f.readline()
        f.close()


class LitepwdShell:

    help_fmt = "{:16}    {:60}"
    help_msg = "show this help massage"

    def __init__(self, user, sqlcipher: SqlcipherExecutor, conf):
        self.user = user
        self.sqlcipher = sqlcipher
        self.__conf = conf
        self.sqlcipher.shell = True
        self.__PROMPT = f"\033[1;32mlitepwd@\033[1;36m{self.user}\033[1;32m:> \033[0m"

    def start(self):
        print_red(" [-] shell mode still coding. please using command.")
        while True:
            args = self.__prompt()
            if len(args) == 0:
                continue
            if args[0] == "help":
                LitepwdShell.help()
            elif args[0] == "system":
                self._system(args[1:])
            elif args[0] == "set":
                self._set(args[1:])
            elif args[0] == "get":
                self._get(args[1:])
            elif args[0] == "backup":
                pass
            elif args[0] in ("quit", "exit"):
                exit(0)
            else:
                print_red(f"command:{args[0]} not found!")

    @classmethod
    def help(cls):
        print(cls.help_fmt.format("command", "usage"))
        print(cls.help_fmt.format("help", cls.help_msg))
        print(cls.help_fmt.format("set", "Used to change content to litepwd.use set help show more."))
        print(cls.help_fmt.format("get", "To get some content to litepwd.using get help show more."))
        print(cls.help_fmt.format("system", "execute command to system"))
        print(cls.help_fmt.format("backup", "backup your stored password."))
        print(cls.help_fmt.format("quit(exit)", "quit."))

    @staticmethod
    def _system(args):
        cmd = "".join([arg + " " for arg in args])
        os.system(cmd)

    def _get(self, args):
        if not len(args):
            print_red("command:get require more argument!")
        if args[0] == "help":
            print(self.help_fmt.format("command: get", "usage"))
            print(self.help_fmt.format("help", self.help_msg))
            print(self.help_fmt.format("users", "show all registered account."))
            print(self.help_fmt.format("store", "get stored password. example: get store example.com"))
            print(self.help_fmt.format("all", "get all stored data."))
        elif args[0] == "users":
            list_user()
        elif args[0] == "store":
            self.__conf['target'] = args[1]
            self.__conf['input'] = True
            query_password(self.sqlcipher, shell=True)
        elif args[0] == "all":
            stores = self.sqlcipher.query_all()
            format_print_store(stores, hidden=False)

    def _set(self, args):
        if not len(args):
            print_red("command:set require more argument!")

    def __prompt(self):
        try:
            ipt = input(self.__PROMPT).split(" ")
            args = []
            for arg in ipt:
                if arg != '':
                    args.append(arg)
            return args
        except KeyboardInterrupt:
            print()
            exit(0)


def main():
    # 获取默认用户
    read_default_user()
    options = option_handle()
    init(options)
    # 参数检查
    if not check():
        error_exit("incorrect option!\nusage: -[l|r|s|u|b|c|-set-password|-list-users] arg", prefix=False)
    # 创建连接
    sqlcipher = connect()
    if not sqlcipher:
        error_exit()
    # 连接正常
    action(sqlcipher)


if __name__ == '__main__':
    main()
